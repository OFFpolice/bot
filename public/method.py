import logging
import os.path

import emoji
from config import *
from data.data import *
class Router:
    def __init__(self):
        self.routes = []
    def add_route(self, path_pattern, handler_class, handler_method):
        # Преобразование шаблона маршрута в регулярное выражение и извлечение имён параметров
        param_pattern = re.compile(r'<(\w+)>')
        path_pattern = param_pattern.sub(r'(?P<\1>[^/]+)', path_pattern)
        path_regex = re.compile(f"^{path_pattern}$")
        param_names = param_pattern.findall(path_pattern)
        # Сохранение правила маршрутизации
        self.routes.append((path_regex, param_names, handler_class, handler_method))
    async def route(self, url, *args, **kwargs):
        parsed_url = urlparse(url)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        # Поиск подходящего маршрута
        for path_regex, param_names, handler_class, handler_method in self.routes:
            match = path_regex.match(path)
            if not match:
                continue
            # Передача параметров пути в query_params
            for param_name in param_names:
                query_params[param_name] = match.group(param_name)
            # Создание обработчика и вызов целевого метода
            try:
                handler = handler_class(*args, **kwargs)
                return await getattr(handler, handler_method)(**query_params)
            except (RPCError,Exception) as e:
                raise ValueError(f"Ошибка выполнения метода {handler_method}: {e}")
        raise ValueError("Раздел в разработке — страница не найдена")

_rate_limit_store = {}
_var_store = {}


class RestrictAccess:
    # Ограничение частоты запросов (в памяти процесса)
    def __init__(self, Msg: Message = None):
        self.msg = Msg

    async def limit_check(self):
        # Проверка превышения лимита обращений
        msg = self.msg
        try:
            now = time.monotonic()
            key = f"restrict{msg.chat.id}"
            limit = int(bot_config['restrict_limit'])
            entry = _rate_limit_store.get(key)
            if entry is None or entry[1] <= now:
                _rate_limit_store[key] = (1, now + 60)
                return True
            count, expires_at = entry
            if count < limit:
                _rate_limit_store[key] = (count + 1, expires_at)
                return True
            if count == limit:
                _rate_limit_store[key] = (count + 1, now + 60 * 10)
                await msg.reply_text('Слишком частые запросы — доступ ограничен на 10 мин.')
            return False
        except Exception as e:
            logging.error(f"Ошибка ограничения доступа: {e}")
            return False


class UserAuth:
    # Авторизация пользователя
    def __init__(self, Msg: Message = None):
        self.msg = Msg

    async def auth(self, FromUser=None):
        '''
        Система авторизации: чтение или создание записи пользователя в БД (aiosqlite)
        '''
        msg = self.msg
        try:
            dbUser = ChatUser(Msg=msg)
            user = await dbUser.get_or_create(FromUser)
            if user and user[4] == 1:
                await msg.reply_text("Аккаунт заблокирован администратором")
                return False
            return user
        except Exception as e:
            logging.error(f"Ошибка доступа к аккаунту: {e}")
            await msg.reply_text("Ошибка доступа к аккаунту")
            return False


class Var:
    def __init__(self, Msg: Message = None):
        self.msg = Msg

    def write(self, value=None):
        msg = self.msg
        if value:
            try:
                name = f"var{msg.chat.id}"
                _var_store[name] = (json.dumps(value, default=str), time.monotonic() + 60 * 2)
                return True
            except Exception as e:
                print(e)
        return False

async def truncate_string(string, length):
    '''Обрезка заголовка до заданной длины'''
    pattern = r":[^:]+:"
    newStr = re.sub(pattern, "", emoji.demojize(string))
    if len(newStr) > length:
        return newStr[:length] + ".."
    else:
        return newStr

async def isPrivileges(chatId,typeG):
    # Проверка прав администратора бота в канале/группе
    try:
        member = await app.get_chat_member(chatId, "me")
        if member.privileges:
            privileges = member.privileges
            if typeG == 'CHANNEL':
                if privileges.can_delete_messages and privileges.can_post_messages and privileges.can_edit_messages and privileges.can_invite_users:
                    return 0
            else:
                if privileges.can_delete_messages and privileges.can_invite_users:
                    return 0
        return 1
    except (FloodWait,BadRequest,ChannelPrivate) as e:
        return 2

async def get_config():
    try:
        configData = ConfigData()
        configList = await configData.get_config_list()
        if configList:
            bot_config["rejectText"] = []
            for config in configList:
                if config[1] == "rejectText":
                    bot_config["rejectText"].append(config[2])
                else:
                    bot_config[config[1]] = config[2]
        return bot_config
    except Exception as e:
        logging.error('Ошибка чтения конфигурации: %s', e)

async def timeJob(arr):
    await app.delete_messages(arr.get('id'), message_ids=arr.get('message_ids'))
async def msgNotify(msg:Message,text='Нет',times=2):
    msgId = await msg.reply_text(text=f"{str(text)} \n(удалится через {times} сек.)")
    scheduler.add_job(timeJob, trigger='date',run_date=datetime.datetime.now() + datetime.timedelta(seconds=times),
                      args=({'id': msgId.chat.id,'message_ids':msgId.id},))

async def isBotBlacklist(Client:Client,group):
    list = await BotBlacklistDate().get_bot_blacklist_list()
    isBot = []
    for bot_name in list:
        try:
            member = await Client.get_chat_member(group, bot_name[1])
            if member.status.name=="ADMINISTRATOR":
                isBot.append([member.user.first_name,member.user.username])
                break
        except RPCError as e:
            # Бот отсутствует в чате/канале
            pass
    return isBot

async def send_msg(chat_id,text):
    try:
        await app.send_message(chat_id=int(chat_id), text=text)
    except RPCError as e:
        logging.error('Не удалось отправить сообщение:',chat_id,'-Ошибка:',e)
async def convoyDriving():
    fleet_list = await db.select("SELECT * FROM fleet_list WHERE state = 1")
    print('Запуск рассылки подборок')
    if fleet_list:
        for fleet in fleet_list:
            print('Подборка в рассылке:',fleet)
            group_list = await db.select("SELECT * FROM group_list WHERE fleet_list=? AND state=2", (fleet[0],))
            print('Участников в подборке:', len(group_list))
            if group_list and len(group_list)>=1:
                for group in group_list:
                    user = await db.select("SELECT * FROM chat_user WHERE id=?", (group[12],))
                    if not user:
                        continue
                    isPrivi = await isPrivileges(chatId=group[1], typeG=group[4])
                    if isPrivi == 1:
                        print('Проверка рассылки: у бота отозваны права -',group[3])
                        await db.update("UPDATE group_list SET state=0 WHERE id=?", (group[0],))
                        text = f"Проверка рассылки:《[{group[3]}]({group[6]})》 " \
                               f"— у бота недостаточно прав, ресурс снят с подборки, проверьте права"
                        await send_msg(chat_id=user[0][1], text=text)
                        continue
                    elif isPrivi == 2:
                        print('Проверка рассылки: бот отсутствует в группе -',group[3])
                        await db.update("UPDATE group_list SET state=0 WHERE id=?", (group[0],))
                        text = f"Проверка рассылки:《[{group[3]}]({group[6]})》 " \
                               f"— бот не найден в группе/канале, ресурс снят с подборки"
                        await send_msg(chat_id=user[0][1], text=text)
                        continue
                    if group[7] !=0:
                        getMsg = await app.get_messages(chat_id=group[1], message_ids=int(group[7]))
                        if not getMsg.text:
                            await db.update("UPDATE group_list SET state=0 WHERE id=?", (group[0],))
                            text = f"Проверка рассылки:《[{group[3]}]({group[6]})》 " \
                                   f"— предыдущее сообщение не найдено, ресурс снят с подборки"
                            await send_msg(chat_id=user[0][1], text=text)
                            continue
                    text_list = await marshalling(group_chat=group,fleet=fleet)
                    print('Сформированный список:',text_list)
                    if len(text_list)>2:
                        keyboard = [
                            [
                                InlineKeyboardButton("➕ Участвовать", url=f"https://t.me/{bot_config.get('botUserName').replace('@', '')}"),
                                InlineKeyboardButton("📣 Биржа рекламы", url=f"https://t.me/jindun")
                            ]
                        ]
                        msg = await app.send_message(chat_id=group[1], text=''.join(text_list),
                                                     reply_markup=InlineKeyboardMarkup(keyboard),
                                                     disable_web_page_preview=True, disable_notification=True)
                        if msg.id:
                            await db.update("UPDATE group_list SET msg_id=? WHERE group_id=?", (msg.id, str(group[1])))
                            try:
                                if group[7] !=0:
                                    await app.delete_messages(chat_id=group[1], message_ids=int(group[7]))
                            except RPCError as e:
                                print('Ошибка удаления предыдущего сообщения -',group[2])
async def marshalling(group_chat=None, fleet=None):
        new_car_list, index = [], 1
        new_car_list.append(f"**⛩️[{fleet[1]}|{bot_config['botName']}](https://t.me/{bot_config.get('botUserName').replace('@', '')}/)⛩️**\n")
        advertising_list = await AdvertisingData().get_advertising_list()
        if len(advertising_list) >= 1:
            new_car_list.append(f"**РЕКЛАМА:[{advertising_list[0][1]}]({advertising_list[0][2]})**\n\n")
        group_list = await db.select("SELECT * FROM group_list WHERE fleet_list=? AND state=2", (fleet[0],))
        for group in group_list:
            if group[0] != group_chat[0]:
                try:
                    link_group = await app.edit_chat_invite_link(group[1],group[6])
                    print(link_group.invite_link)
                    if link_group and link_group.is_revoked==False:
                        new_car_list.append(
                            f"{index}: [{await truncate_string(group[3], 20)}]({link_group.invite_link}) \n")
                        index += 1
                    else:
                        await db.update("UPDATE group_list SET state=0 WHERE id=?", (group[0],))
                        print('Ссылка удалена')
                        continue
                except RPCError as e:
                    print('Ошибка редактирования ссылки',e)
                    await db.update("UPDATE group_list SET state=0 WHERE id=?", (group[0],))
                    continue
            else:
                continue
        try:
            link_group = await app.edit_chat_invite_link(int(group_chat[1]), group_chat[6])
            print(link_group.member_count)
            if link_group and link_group.is_revoked == False:
                await db.update("UPDATE group_list SET input_fan=? WHERE id=?",
                              (link_group.member_count or 0, group_chat[0]))
        except RPCError as e:
            print('Ошибка обновления числа вступивших по ссылке', e)
        if len(advertising_list) >=2:
            new_car_list.append(f"\n**РЕКЛАМА:[{advertising_list[1][1]}]({advertising_list[1][2]})**")
        if len(advertising_list) >= 3:
            new_car_list.append(f"\n**РЕКЛАМА:[{advertising_list[2][1]}]({advertising_list[2][2]})**")
        new_car_list.append(f"**\nЧат взаимопиара: {bot_config.get('publicGroup')}**")
        return new_car_list
