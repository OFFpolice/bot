from config import *
from public.method import *


class Admin:
    def __init__(self, Client: Client, Query: CallbackQuery = None, Msg: Message = None, Data=None):
        self.client = Client
        self.query = Query
        self.msg = Msg
        self.data = Data
    async def retChat(self):
        if self.query:
            return self.query.message
        else:
            return self.msg

    async def sendMsg(self, **kwargs):
        msg = await self.retChat()
        try:
            if self.query:
                await self.client.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=kwargs['text'],
                                                    reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                                    disable_web_page_preview=True)
            else:
                if len(bot_config.get('video')) > 24:
                    await self.client.send_video(chat_id=msg.chat.id, video=bot_config.get('video'),
                                                 caption=kwargs['text'],
                                                 reply_markup=InlineKeyboardMarkup(kwargs['keyboard']))
                else:
                    await msg.reply_text(text=kwargs['text'], reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                         disable_web_page_preview=True)
        except RPCError as e:
            print(e)

    async def index(self, **kwargs):
        msg = await self.retChat()
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n\n" \
               "======**🏆 Панель управления 🏆**======\n\n" \
               "🌟**Добро пожаловать, администратор:**🌟\n" \
               "  ✅ Здесь можно управлять функциями бота"
        keyboard = [
            [InlineKeyboardButton("☸️ Настройки бота", callback_data="a/настройки"),
            InlineKeyboardButton("🅰️️ Реклама", callback_data="a/рекл")],
            [InlineKeyboardButton("🚒 Подборки", callback_data="a/подб"),
            InlineKeyboardButton("📇 Каналы и группы", callback_data="a/группы")],
            [InlineKeyboardButton("🤖 Чёрный список ботов", callback_data="a/чс_ботов"),
             InlineKeyboardButton("👨‍💻 Пользователи", callback_data="a/юзеры")],
        ]
        await self.sendMsg(text=text, keyboard=keyboard)

    async def config(self, **kwargs):
        bot_config = get_config()
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n\n" \
               "======**🏆 Настройки бота 🏆**======\n\n" \
               f"**🔸Инициализация меню:** обновление команд меню бота\n" \
               f"**🔸Имя бота:** {bot_config['botName']}\n" \
               f"**🔸Юзернейм бота:** {bot_config['botUserName']}\n" \
               f"**🔸Текст приветствия:**\n'{bot_config['indexTxt']}'\n" \
               f"**🔸Причины отказа:**\n{'|'.join(bot_config['rejectText'])}\n" \
               f"**🔸Видео-презентация:** {'🟢 Загружено' if len(bot_config['video']) > 20 else '🚫 Не загружено'}\n" \
               f"**🔸Группа админов:** {bot_config['adminGroup']}\n" \
               f"**🔸Группа уведомлений:** {bot_config['msgGroup']}\n" \
               f"**🔸Чат общения:** {bot_config['publicGroup']}\n" \
               f"**🔸Лимит запросов:** {bot_config['restrict_limit']} \n(при превышении за 60 сек. доступ ограничивается на 10 мин.)"
        keyboard = [
            [InlineKeyboardButton(f"Инициализировать меню", callback_data="a/меню")],
             [InlineKeyboardButton(f"Изменить имя бота", callback_data="a/ред_настр?k=bn"),
             InlineKeyboardButton(f"Изменить юзернейм", callback_data="a/ред_настр?k=bu")],
            [InlineKeyboardButton(f"Изменить приветствие", callback_data="a/ред_настр?k=it"),
             InlineKeyboardButton(f"Причины отказа", callback_data="a/отказы")],
            [InlineKeyboardButton(f"Изменить видео", callback_data="a/ред_настр?k=vd"),
             InlineKeyboardButton(f"Группа админов", callback_data="a/ред_настр?k=ag")],
            [InlineKeyboardButton(f"Группа уведомлений", callback_data="a/ред_настр?k=mg"),
             InlineKeyboardButton(f"Чат общения", callback_data="a/ред_настр?k=pg")],
            [InlineKeyboardButton(f"Изменить лимит", callback_data="a/ред_настр?k=rl")],
            [InlineKeyboardButton(f"↩️ Назад", callback_data="a/админ")],
        ]
        await self.sendMsg(text=text, keyboard=keyboard)

    async def modifBot(self, **kwargs):
        msg = await self.retChat()
        prompts = {
            "bn": "Введите имя бота",
            "bu": "Введите юзернейм бота (пример @xxbot)",
            "it": "Введите текст приветствия",
            "vd": "Отправьте видео-презентацию",
            "ag": "Введите ID группы админов",
            "mg": "Введите ID группы уведомлений",
            "pg": "Введите чат общения (пример @xxx)",
            "rl": "Введите лимит запросов (число от 1 до 60)",
            "ra": "Введите причину отказа",
            "re": "Введите новую причину отказа",
        }
        key = kwargs.get('k', [None])[0]
        item_id = kwargs.get('id', [None])[0]
        if key in prompts:
            prompt = f"{prompts[key]}:{item_id}" if item_id else prompts[key]
        else:
            prompt = kwargs.get('text', [''])[0]
        txt = f"📲{prompt}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def initialization(self,**kwargs):
        initial =await app.set_bot_commands([BotCommand("start", "Главная"), BotCommand("help", "Помощь")])
        print(initial)
        if initial:
            await self.query.answer(text=f'Меню команд успешно обновлено', show_alert=True)

    async def reviewRejectionWords(self, **kwargs):
        '''Список шаблонов причин отказа'''
        rejectText_list = await ConfigData().get_rejectText_list()
        text = "======**🏆 Шаблоны причин отказа 🏆**======\n" \
               "Быстрый выбор причины при отклонении заявки\n" \
               "Обозначения: ➕Добавить ❌Удалить 🖍Изменить\n\n" \
               "🚫**Список причин отказа:**\n"
        keyboard = []
        print(rejectText_list)
        if rejectText_list:
            for index, rejectText in enumerate(rejectText_list):
                text += f"{index + 1}.{rejectText[2]}\n"
                keyboard.append([InlineKeyboardButton(f"{index + 1}.{rejectText[2]}", callback_data="-"),
                                 InlineKeyboardButton(f"❌ Удалить", callback_data=f"a/уд_отказ?id={rejectText[0]}"),
                                 InlineKeyboardButton(f"🖍 Изменить",
                                                      callback_data=f"a/ред_настр?k=re&id={rejectText[0]}")])
        else:
            text += "Пусто, не задано"
            keyboard.append([InlineKeyboardButton(f"Список пуст", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"➕Добавить", callback_data="a/ред_настр?k=ra")])
        keyboard.append([InlineKeyboardButton(f"🏠 В админку", callback_data="a/админ"),
                         InlineKeyboardButton(f"↩️ Назад", callback_data="a/настройки")])
        await self.sendMsg(text=text, keyboard=keyboard)

    async def delReviewRejectionWords(self, **kwargs):
        '''Удаление шаблона причины отказа'''
        msg = await self.retChat()
        id = kwargs.get('id')[0]
        delData = await ConfigData().del_rejectText(id=id)
        if delData:
            await self.query.answer(text="✅Удалено успешно", cache_time=5)
            await self.reviewRejectionWords()
        else:
            await msgNotify(msg=msg, text="❕Не удалось удалить")

class Advertising:
    def __init__(self, Client: Client, Query: CallbackQuery = None, Msg: Message = None, Data=None):
        self.client = Client
        self.query = Query
        self.msg = Msg
        self.data = Data
    async def retChat(self):
        if self.query:
            return self.query.message
        else:
            return self.msg
    async def sendMsg(self, **kwargs):
        msg = await self.retChat()
        try:
            if self.query:
                await self.client.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=kwargs['text'],
                                                    reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                                    disable_web_page_preview=True)
            else:
                if len(bot_config.get('video')) > 24:
                    await self.client.send_video(chat_id=msg.chat.id, video=bot_config.get('video'),
                                                 caption=kwargs['text'],
                                                 reply_markup=InlineKeyboardMarkup(kwargs['keyboard']))
                else:
                    await msg.reply_text(text=kwargs['text'], reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                         disable_web_page_preview=True)
        except RPCError as e:
            print(e)
    async def adInput(self, **kwargs):
        msg = await self.retChat()
        prompts = {
            "add": "Введите рекламу (пример Название&Ссылка)",
            "edit": "Введите новую рекламу",
        }
        key = kwargs.get('k', [None])[0]
        item_id = kwargs.get('id', [None])[0]
        if key in prompts:
            prompt = f"{prompts[key]}:{item_id}" if item_id else prompts[key]
        else:
            prompt = kwargs.get('text', [''])[0]
        txt = f"🗞️{prompt}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def index(self, **kwargs):
        '''Управление рекламой'''
        advertising_list = await AdvertisingData().get_advertising_list()
        text = "======**🏆 Управление рекламой 🏆**======\n" \
               "Реклама, добавляемая в сообщения рассылки\n" \
               "Пример: Взаимопиар&https://t.me/+oYUJoUkMlfphN2M1\n" \
               "Обозначения: ➕Добавить ❌Удалить 🖍Изменить\n\n" \
               "📢**Список рекламы:**\n"
        keyboard = []
        if advertising_list:
            for index, advertising in enumerate(advertising_list):
                text += f"{index + 1}.[{advertising[1]}]({advertising[2]})\n"
                keyboard.append([InlineKeyboardButton(f"{index + 1}.{advertising[1]}", callback_data="-"),
                                 InlineKeyboardButton(f"❌ Удалить", callback_data=f"a/уд_рекл?id={advertising[0]}"),
                                 InlineKeyboardButton(f"🖍 Изменить",
                                                      callback_data=f"a/ввод_рекл?k=edit&id={advertising[0]}")])
        else:
            text += "Пусто, не задано"
            keyboard.append([InlineKeyboardButton(f"Список пуст", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"➕Добавить", callback_data="a/ввод_рекл?k=add")])
        keyboard.append([InlineKeyboardButton(f"🏠 В админку", callback_data="a/админ"),
                         InlineKeyboardButton(f"↩️ Назад", callback_data="a/админ")])
        await self.sendMsg(text=text, keyboard=keyboard)
    async def delAdvertising(self, **kwargs):
        '''Удаление рекламы'''
        msg = await self.retChat()
        id = kwargs.get('id')[0]
        delData = await AdvertisingData().del_advertising(id=id)
        if delData:
            await self.query.answer(text="✅Удалено успешно", cache_time=5)
            await self.index()
        else:
            await msgNotify(msg=msg, text="❕Не удалось удалить")
class Car:
    # Управление подборками
    def __init__(self, Client: Client, Query: CallbackQuery = None, Msg: Message = None, Data=None):
        self.client = Client
        self.query = Query
        self.msg = Msg
        self.data = Data
    async def retChat(self):
        if self.query:
            return self.query.message
        else:
            return self.msg
    async def sendMsg(self, **kwargs):
        msg = await self.retChat()
        try:
            if self.query:
                await self.client.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=kwargs['text'],
                                                    reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                                    disable_web_page_preview=True)
            else:
                if len(bot_config.get('video')) > 24:
                    await self.client.send_video(chat_id=msg.chat.id, video=bot_config.get('video'),
                                                 caption=kwargs['text'],
                                                 reply_markup=InlineKeyboardMarkup(kwargs['keyboard']))
                else:
                    await msg.reply_text(text=kwargs['text'], reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                         disable_web_page_preview=True)
        except RPCError as e:
            print(e)
    async def inputBot(self, **kwargs):
        msg = await self.retChat()
        prompts = {
            "add": "Введите название подборки каналов",
            "title": "Введите новое название подборки",
            "desc": "Введите новое описание подборки",
            "max": "Введите макс. участников подборки",
            "sub": "Введите мин. подписчиков подборки",
            "read": "Введите мин. просмотров подборки",
        }
        key = kwargs.get('k', [None])[0]
        item_id = kwargs.get('id', [None])[0]
        if key in prompts:
            prompt = f"{prompts[key]}:{item_id}" if item_id else prompts[key]
        else:
            prompt = kwargs.get('text', [''])[0]
        txt = f"🚒{prompt}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def index(self, **kwargs):
        '''Главная страница управления подборками'''
        msg = await self.retChat()
        user = self.data.get('user')
        try:
            if user:
                text = f"**🚀Telegram-взаимопиар:**  @{bot_config.get('botUserName')}\n\n" \
                       f"**UID {user[1]}** Администратор {user[3]}:\n\n" \
                       f"**Автоматический бот взаимопиара**\n\n" \
                       f"👇 Выберите управление подборками каналов или групп\n"
                keyboard = [
                    [InlineKeyboardButton("🏵️Подборки каналов🏵️", callback_data="a/подб_кан")],
                    [InlineKeyboardButton("🌸Подборки групп🌸", callback_data="a/подб_гр")],
                    [InlineKeyboardButton(f"↩️ Назад", callback_data="a/админ")]
                ]
                await self.sendMsg(text=text, keyboard=keyboard)
        except (RPCError, Exception) as E:
            print(E)
            await msg.reply_text(text=f'Ошибка: сделайте скриншот и обратитесь в поддержку {E}')
    # Подборки каналов
    async def channel_car(self,**kwargs):
        OFFSET, LIMIT = int(kwargs.get('page')[0]) if kwargs.get('page') else 0, 20
        fleet = CarData()
        fleetList, count =await fleet.get_fleet(OFFSET=OFFSET, LIMIT=LIMIT)
        keyboard = []
        text = f"Управление подборками каналов\n\n" \
               f"Выберите подборку ниже для настройки параметров и состава.\n\n" \
               f"Формат:\n" \
               f"🚒Запущена/🕛Ожидание Название|Участники/Макс|Мин. подписчиков\n\n" \
               f"Нажмите на нужную подборку"
        if fleetList:
            totalPages, currentPage = math.ceil(count / LIMIT), math.ceil(OFFSET / LIMIT) + 1
            upPage, dowPage = OFFSET - LIMIT, OFFSET + LIMIT
            row, step = [], 2
            for i in range(0, len(fleetList), step):
                batch = fleetList[i:i + step]
                for Cont in batch:
                    row.append(InlineKeyboardButton(
                        f"{'🚒' if Cont[4] == 1 else '🕛'} {Cont[1]}|{Cont[11]}/{Cont[6]}|{Cont[8] / 1000}K",
                        callback_data=f"a/детали_п?fleet={Cont[0]}"))
                keyboard.append(row)
                row = []
            keyboard.append([InlineKeyboardButton(f"{'⬅️Назад' if upPage >= 0 else '-'}",
                                                  callback_data=f"a/подб_кан?page={upPage}" if upPage >= 0 else '-'),
                             InlineKeyboardButton(f"{currentPage}/{totalPages} стр.", callback_data="-"),
                             InlineKeyboardButton(f"️{'➡️Далее' if currentPage != totalPages else '-'}",
                                                  callback_data=f"a/подб_кан?page={dowPage}" if currentPage != totalPages else '-')])
        else:
            keyboard.append([InlineKeyboardButton(f"Пусто / подборок не найдено", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"➕ Добавить подборку", callback_data="a/ввод_подб?k=add")])
        keyboard.append([InlineKeyboardButton(f"🏠 В админку", callback_data="a/админ"),
                         InlineKeyboardButton(f"↩️ Назад", callback_data="a/подб")])
        await self.sendMsg(text=text, keyboard=keyboard)
    async def channel_fleet_info(self,**kwargs):
        fleet_id = kwargs.get("fleet")[0]
        fleet=CarData()
        fleetInfo,group_list=await fleet.get_fleet_one(id=fleet_id),await fleet.get_fleet_group_list(id=fleet_id)
        if fleetInfo:
            text = f"**Название подборки：** {fleetInfo[1]}\n" \
                      f"**Описание：** {fleetInfo[2]}\n" \
                      f"**Участники (сейчас/макс)：** {fleetInfo[11]}/{fleetInfo[6]}\n" \
                      f"**Тип подборки：** Канал\n" \
                      f"**Мин. подписчиков：** {fleetInfo[8] / 1000} K\n" \
                      f"**Мин. просмотров：**{fleetInfo[9]}\n" \
                      f"**Статус рассылки：**{'🚒 Запущена' if fleetInfo[4] == 1 else '🕛 Остановлена'} \n\n" \
                      "**Список участников：**\n"
            keyboard=[]
            if group_list:
                group_id,row=[],1
                for index,group in enumerate(group_list):
                    text+=f"{index+1}.[{await truncate_string(group[3],20)}]({group[6]}) {round(group[5]/1000,1)}k\n"
                    group_id.append(InlineKeyboardButton(f"{index+1}", callback_data=f"a/кан_подб?fleet={fleetInfo[0]}&group={group[0]}"))
                    if index+1==8*row or ((len(group_list)-(index+1))<8 and len(group_list)==(index+1)):
                        row+=1
                        keyboard.append(group_id)
                        group_id=[]
            else:
                text+="Пока нет участников взаимопиара\n"
            if fleetInfo[6]>fleetInfo[11]:
                text+="\n✅ В подборке есть свободные места"
            else:
                text+="\n‼️ Подборка заполнена"
            keyboard.append([InlineKeyboardButton(f"=========Редактирование подборки=========", callback_data="-")])
            keyboard.append([InlineKeyboardButton(f"Название️",callback_data=f"a/ввод_подб?k=title&id={fleetInfo[0]}"),
                             InlineKeyboardButton(f"Описание️",callback_data=f"a/ввод_подб?k=desc&id={fleetInfo[0]}"),
                             InlineKeyboardButton(f"Лимит",callback_data=f"a/ввод_подб?k=max&id={fleetInfo[0]}"),
                             InlineKeyboardButton(f"Подписч.",callback_data=f"a/ввод_подб?k=sub&id={fleetInfo[0]}"),
                             InlineKeyboardButton(f"Просм.️",callback_data=f"a/ввод_подб?k=read&id={fleetInfo[0]}")])
            keyboard.append([InlineKeyboardButton(f"Статус: {'🚒 Запущена' if fleetInfo[4] == 1 else '🕛 Остановлена'}", callback_data=f"a/статус_п?fleet={fleetInfo[0]}&state={fleetInfo[4]}")])
            keyboard.append([InlineKeyboardButton(f"🏠 В админку", callback_data="a/админ"),
                             InlineKeyboardButton(f"↩️ Назад", callback_data="a/подб_кан")])
            await self.sendMsg(text=text,keyboard=keyboard)
    async def channel_fleet_state(self,**kwargs):
        msg = await self.retChat()
        fleet_id,state = kwargs.get("fleet")[0],kwargs.get("state")[0]
        carData = CarData()
        if state=='0':
            await carData.put_car_state(text=1, id=fleet_id)
            await msgNotify(msg=msg, text='Подборка запущена')
        else:
            await carData.put_car_state(text=0, id=fleet_id)
            await msgNotify(msg=msg, text='Подборка остановлена')
        await self.channel_fleet_info(fleet=[fleet_id])
    async def channel_info(self,**kwargs):
        group_id = kwargs.get('group')[0]
        car = CarData()
        group = await car.get_user_group_one(id=group_id)
        fleetInfo = await car.get_fleet_one(id=group[11])
        user = await car.get_user(id=group[12])
        notify = await car.get_notify_msg(user=user[0], group=group[0])
        text = f"**Подборка:** {fleetInfo[1]}\n" \
               f"**Тип подборки:** Канал\n" \
               f"**Описание:** {fleetInfo[2]}\n" \
               f"**Участники (сейчас/макс):** {fleetInfo[11]}/{fleetInfo[6]}\n" \
               f"**Мин. подписчиков:** {fleetInfo[8] / 1000} K\n" \
               f"**Мин. просмотров:** {fleetInfo[9]}\n\n" \
               f"**ID канала:** {group[1]}\n" \
               f"**Канал:** [{group[3]}]({group[6]})\n" \
               f"**Подписчиков:** {group[5]}\n" \
               f"**ID заявителя:** {user[1]}\n" \
               f"**Заявитель:** [{user[3]}](https://t.me/{user[2] or ''})\n"
        text += f"**Статус заявки:**  {notify[3] if notify else 'Неизвестно'} "
        keyboard=[]
        if group[10]==2:
            keyboard.append([InlineKeyboardButton("⏬ Снять с подборки", callback_data=f"a/состав_п?group={group[0]}")])
        elif group[10] in [0,1]:
            keyboard.append([InlineKeyboardButton("⏫ Включить в подборку", callback_data=f"a/состав_п?group={group[0]}")])
        if group[10] == 10:
            keyboard.append([InlineKeyboardButton("🟢 Разблокировать", callback_data=f"a/бан_п?group={group[0]}")])
        else:
            keyboard.append([InlineKeyboardButton("🚫 Заблокировать", callback_data=f"a/бан_п?group={group[0]}")])
        keyboard.append([InlineKeyboardButton(f"🏠 В админку", callback_data="a/админ"),
                         InlineKeyboardButton(f"↩️ Назад", callback_data=f"a/детали_п?fleet={fleetInfo[0]}")])
        await self.sendMsg(text=text,keyboard=keyboard)
    async def downGroup(self, **kwargs):
        '''Снятие или добавление канала в подборку'''
        print(kwargs.get('group')[0])
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        if group[10]==2:
            await car.put_car_pass_review(group=group, state=0, label=f"🔴 Канал снят с подборки администратором")
        elif group[10]==0:
            await car.put_car_pass_review(group=group, state=2, label=f"🟢 Канал добавлен в подборку администратором")
        await self.channel_info(group=[kwargs.get('group')[0]])
        await self.reviewNotify(group=[kwargs.get('group')[0]])
    async def banGroup(self,**kwargs):
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        if group[10]==10:
            await car.put_car_pass_review(group=group, state=0, label=f"🟢 Канал разблокирован")
        else:
            await car.put_car_pass_review(group=group, state=10, label=f"🚫 Канал заблокирован администратором")
        await self.channel_info(group=[kwargs.get('group')[0]])
        await self.reviewNotify(group=[kwargs.get('group')[0]])
    async def reviewNotify(self, **kwargs):
        '''Формирование и отправка уведомления пользователю'''
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        fleet = await car.get_fleet_one(id=group[11])
        toUser = await car.get_user(id=group[12])
        notify = await car.get_notify_msg(user=toUser[0], group=group[0])
        text = "**📣Системное уведомление**📣\n" \
               f"**Подборка:** {fleet[1]}\n" \
               f"**Тип подборки:** Канал\n" \
               f"**Описание:** {fleet[2]}\n" \
               f"**Участники (сейчас/макс):** {fleet[11]}/{fleet[6]}\n" \
               f"**Мин. подписчиков:** {fleet[8] / 1000} K\n" \
               f"**Мин. просмотров:** {fleet[9]}\n\n" \
               f"**ID канала:** {group[1]}\n" \
               f"**Канал:** [{group[3]}]({group[6]})\n" \
               f"**Подписчиков:** {group[5]}\n" \
               f"**ID заявителя:** {toUser[1]}\n" \
               f"**Заявитель:** [{toUser[3]}](https://t.me/{toUser[2] or ''})\n"
        text += f"**Статус заявки:** {notify[3] if notify else 'Неизвестно'} "
        try:
            await self.client.send_message(chat_id=toUser[1], text=text, disable_web_page_preview=True)
        except RPCError as e:
            msg = await self.retChat()
            await msgNotify(msg=msg, text='❗Не удалось уведомить пользователя', times=5)
        if len(bot_config["msgGroup"]) > 5:
            try:
                keyboards = [[InlineKeyboardButton("➕ Участвовать", url=f"https://t.me/{bot_config['botUserName']}")]]
                await self.client.send_message(chat_id=bot_config["msgGroup"], text=text,
                                               reply_markup=InlineKeyboardMarkup(keyboards),
                                               disable_web_page_preview=True)
            except RPCError as e:
                msg = await self.retChat()
                await msgNotify(msg=msg, text='❗Не удалось уведомить группу сообщений', times=5)
class Review:
    # Модерация заявок в группе администраторов
    def __init__(self, Client: Client, Query: CallbackQuery = None, Msg: Message = None, Data=None):
        self.client = Client
        self.query = Query
        self.msg = Msg
        self.data = Data
    async def retChat(self):
        if self.query:
            return self.query.message
        else:
            return self.msg
    async def sendMsg(self, **kwargs):
        msg = await self.retChat()
        try:
            if self.query:
                await self.client.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=kwargs['text'],
                                                    reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                                    disable_web_page_preview=True)
            else:
                if len(bot_config.get('video')) > 24:
                    await self.client.send_video(chat_id=msg.chat.id, video=bot_config.get('video'),
                                                 caption=kwargs['text'],
                                                 reply_markup=InlineKeyboardMarkup(kwargs['keyboard']))
                else:
                    await msg.reply_text(text=kwargs['text'], reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                         disable_web_page_preview=True)
        except RPCError as e:
            print(e)
    async def inputBot(self, **kwargs):
        msg = await self.retChat()
        key = kwargs.get('k', [None])[0]
        item_id = kwargs.get('id', [None])[0]
        if key == "rej" and item_id:
            prompt = f"Введите свою причину отказа:{item_id}"
        else:
            prompt = kwargs.get('text', [''])[0]
        txt = f"💭{prompt}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def passReview(self, **kwargs):
        'Одобрение заявки'
        msg = await  self.retChat()
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        fleetInfo =await car.get_fleet_one(id=group[11])
        if not fleetInfo:
            await car.put_car_pass_review(group=group, state=0, label='Отклонено: подборка не существует')
            await msgNotify(msg=msg, text='❌Подборка не существует',times=5)
        elif not fleetInfo[6]>fleetInfo[11]:
            await car.put_car_pass_review(group=group, state=0, label='Отклонено: подборка уже заполнена')
            await msgNotify(msg=msg, text='❌Подборка заполнена, автоматический отказ',times=5)
        try:
            link = await app.create_chat_invite_link(group[1])
            link = link.invite_link
            # link="https://t.me/+629C4CiltehmZjg1"
            await car.put_car_pass_review(group=group,state=2,label='Одобрено',url=link)
        except RPCError as e:
            await car.put_car_pass_review(group=group, state=0, label='Отклонено: нет прав на создание ссылки')
            await msgNotify(msg=msg, text='❌Нет прав на пригласительную ссылку — отклонено',times=5)
        text,keyboard,user = await self.reviewNotify(group=[group[0]])
        await self.sendReviewInfo(text=[text],keyboard=[keyboard],user_id=[user])
    async def rejectReview(self,**kwargs):
        rejectText = await ConfigData().get_rejectText_list()
        content = []
        if rejectText:
            for audit in rejectText:
                content.append([InlineKeyboardButton(f"{audit[2]}",callback_data=f"a/причина?group={kwargs.get('group')[0]}&reason={audit[0]}")])
        content.append([InlineKeyboardButton(f"🔡 Своя причина отказа", callback_data=f"a/своя_прич?k=rej&id={kwargs.get('group')[0]}")
                        ,InlineKeyboardButton(f"↩️ Назад", callback_data=f"a/возврат?group={kwargs.get('group')[0]}")])
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n\n" \
                   "======**🏆 Причина отказа 🏆**======\n" \
                   f"Выберите причину отказа\n" \
                   f"(шаблоны настраиваются в разделе «Настройки бота»)"
        await self.sendMsg(text=text,keyboard=content)
    async def rejectReason(self,**kwargs):
        msg = await self.retChat()
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        fleetInfo = await car.get_fleet_one(id=group[11])
        if not fleetInfo:
            await car.put_car_pass_review(group=group, state=0, label='Отклонено: подборка не существует')
            await msgNotify(msg=msg, text='❌Подборка не существует')
        if group:
            reply = {}
            if self.query:
                Text = await car.get_rejectText(id=kwargs.get('reason')[0])
                reply["Text"] = Text[2]
            else:
                reply["Text"] = kwargs.get('reason')[0]
                reply["reply_id"] = msg.reply_to_message.reply_to_message_id
            if await car.put_car_pass_review(group=group, state=0, label=f"Отклонено:{reply['Text']}"):
                text, keyboard, user = await self.reviewNotify(group=[group[0]])
                await self.sendReviewInfo(text=[text], keyboard=[keyboard], user_id=[user],reply_id=[reply.get("reply_id")])
    async def rejectBack(self,**kwargs):
        '''Возврат к карточке заявки'''
        text,keyboard,user = await self.reviewNotify(group=[kwargs.get("group")[0]])
        await self.sendMsg(text=text,keyboard=keyboard)
    async def reviewNotify(self,**kwargs):
        '''Формирование карточки заявки'''
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        fleet = await car.get_fleet_one(id=group[11])
        toUser=  await car.get_user(id=group[12])
        notify =await car.get_notify_msg(user=toUser[0],group=group[0])
        text = "**📣Системное уведомление**📣\n" \
               f"**Подборка:** {fleet[1]}\n" \
               f"**Тип подборки:** Канал\n" \
               f"**Описание:** {fleet[2]}\n" \
               f"**Участники (сейчас/макс):** {fleet[11]}/{fleet[6]}\n" \
               f"**Мин. подписчиков:** {fleet[8] / 1000} K\n" \
               f"**Мин. просмотров:** {fleet[9]}\n\n" \
               f"**ID канала:** {group[1]}\n" \
               f"**Канал:** [{group[3]}]({group[6]})\n" \
               f"**Подписчиков:** {group[5]}\n" \
               f"**ID заявителя:** {toUser[1]}\n" \
               f"**Заявитель:** [{toUser[3]}](https://t.me/{toUser[2] or ''})\n"
        keyboard=[]
        if group[10]==1:
            text+=f"**Статус заявки:** 🔵 {notify[3] if notify else 'Неизвестно'} "
            keyboard.append([InlineKeyboardButton("🟢 Одобрить", callback_data=f"a/одобрить?group={group[0]}"),
                     InlineKeyboardButton("❌ Отклонить", callback_data=f"a/отклонить?group={group[0]}")])
            keyboard.append([InlineKeyboardButton("🚫 Заблокировать", callback_data=f"a/бан_мод?group={group[0]}")])
        elif group[10]==2:
            text+=f"**Статус заявки:** 🟢 {notify[3] if notify else 'Неизвестно'} "
            keyboard.append([InlineKeyboardButton("⏬ Снять с подборки", callback_data=f"a/снять_мод?group={group[0]}")])
            keyboard.append([InlineKeyboardButton("🚫 Заблокировать", callback_data=f"a/бан_мод?group={group[0]}")])
        elif group[10]==10:
            text+=f"**Статус заявки:** 🚫 {notify[3] if notify else 'Неизвестно'}"
            keyboard.append([InlineKeyboardButton("🟢 Разблокировать", callback_data=f"a/бан_мод?group={group[0]}")])
        else:
            text+=f"**Статус заявки:** ⚪ {notify[3] if notify else 'Неизвестно'}"
            keyboard.append([InlineKeyboardButton("🚫 Заблокировать", callback_data=f"a/бан_мод?group={group[0]}")])
        return text,keyboard,toUser
    async def sendReviewInfo(self,**kwargs):
        '''Отправка результата модерации'''
        text,keyboard,user_id=kwargs.get("text")[0],kwargs.get("keyboard")[0],kwargs.get("user_id")[0]
        msg = await self.retChat()
        if kwargs.get("reply_id") and kwargs.get("reply_id")[0]:
            await self.client.edit_message_text(chat_id=msg.chat.id, message_id=kwargs.get("reply_id")[0],
                                                text=text,reply_markup=InlineKeyboardMarkup(keyboard),
                                                disable_web_page_preview=True)
        else:
            await self.sendMsg(text=text, keyboard=keyboard)
        try:
            await self.client.send_message(chat_id=user_id[1], text=text, disable_web_page_preview=True)
        except RPCError as e:
            await msgNotify(msg=msg, text='❗Не удалось уведомить пользователя', times=5)
        if len(bot_config["msgGroup"]) > 5:
            try:
                keyboards = [[InlineKeyboardButton("➕ Участвовать", url=f"https://t.me/{bot_config['botUserName']}")]]
                await self.client.send_message(chat_id=bot_config["msgGroup"], text=text,
                                               reply_markup=InlineKeyboardMarkup(keyboards),
                                               disable_web_page_preview=True)
            except RPCError as e:
                await msgNotify(msg=msg, text='❗Не удалось уведомить группу сообщений', times=5)
    # Изменение статуса канала
    async def banGroup(self,**kwargs):
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        if group[10]==10:
            await car.put_car_pass_review(group=group, state=0, label=f"Ваш канал разблокирован")
        else:
            await car.put_car_pass_review(group=group, state=10, label=f"Ваш канал заблокирован администратором")
        text, keyboard, user = await self.reviewNotify(group=kwargs.get('group'))
        await self.sendReviewInfo(text=[text], keyboard=[keyboard], user_id=[user])
    async def downGroup(self, **kwargs):
        '''Снятие канала с подборки'''
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        if group:
            await car.put_car_pass_review(group=group, state=0, label=f"Ваш канал снят с подборки администратором")
        text, keyboard, user = await self.reviewNotify(group=kwargs.get('group'))
        await self.sendReviewInfo(text=[text], keyboard=[keyboard], user_id=[user])
class Group:
    # Управление каналами и группами
    def __init__(self, Client: Client, Query: CallbackQuery = None, Msg: Message = None, Data=None):
        self.client = Client
        self.query = Query
        self.msg = Msg
        self.data = Data
    async def retChat(self):
        if self.query:
            return self.query.message
        else:
            return self.msg
    async def sendMsg(self, **kwargs):
        msg = await self.retChat()
        try:
            if self.query:
                await self.client.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=kwargs['text'],
                                                    reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                                    disable_web_page_preview=True)
            else:
                if len(bot_config.get('video')) > 24:
                    await self.client.send_video(chat_id=msg.chat.id, video=bot_config.get('video'),
                                                 caption=kwargs['text'],
                                                 reply_markup=InlineKeyboardMarkup(kwargs['keyboard']))
                else:
                    await msg.reply_text(text=kwargs['text'], reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                         disable_web_page_preview=True)
        except RPCError as e:
            print(e)
    async def inputBot(self, **kwargs):
        msg = await self.retChat()
        key = kwargs.get('k', [None])[0]
        prompt = "Введите название канала или группы" if key == "s" else kwargs.get('text', [''])[0]
        txt = f"🏵️‍{prompt}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def index(self,**kwargs):
        OFFSET, LIMIT = int(kwargs.get('page')[0]) if kwargs.get('page') else 0, 20
        search=kwargs.get('search')
        groupData = GroupData()
        group  = await groupData.get_group_list(OFFSET=OFFSET, LIMIT=LIMIT,search=search)
        group_count = await groupData.get_group_index_count()
        keyboard = []
        text = f"Каналы и группы — Управление\n\n" \
               f"Всего ресурсов:{group_count[0]}\n" \
               f"Каналы:{group_count[1]}|В подборке {group_count[2]}|Свободно {group_count[1]-group_count[2]}\n" \
               f"Группы:{group_count[3]}|В подборке {group_count[4]}|Свободно {group_count[3]-group_count[4]}\n" \
               f"Обозначения:\n" \
               f"🏵️‍Канал/🌸Группа — Название\n\n" \
               f"Нажмите на нужную запись для управления"
        if group and group_count:
            totalPages, currentPage = math.ceil(group_count[0] / LIMIT), math.ceil(OFFSET / LIMIT) + 1
            upPage, dowPage = OFFSET - LIMIT, OFFSET + LIMIT
            for key in group:
                keyboard.append([InlineKeyboardButton(f"{'🏵️‍' if key[4] == 'CHANNEL' else '🌸'}-{key[3]} ",callback_data=f"a/инфо_гр?group={key[0]}")])
            keyboard.append([InlineKeyboardButton(f"{'⬅️Назад' if upPage >= 0 else '-'}",
                                                  callback_data=f"a/группы?page={upPage}" if upPage >= 0 else '-'),
                             InlineKeyboardButton(f"{currentPage}/{totalPages} стр.", callback_data="-"),
                             InlineKeyboardButton(f"️{'➡️Далее' if currentPage != totalPages else '-'}",
                                                  callback_data=f"a/группы?page={dowPage}" if currentPage != totalPages else '-')])
        else:
            keyboard.append([InlineKeyboardButton(f"Пусто / не найдено", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"🔎 Поиск", callback_data="a/ввод_гр?k=s")])
        keyboard.append([InlineKeyboardButton(f"🏠 В админку", callback_data="a/админ"),
                         InlineKeyboardButton(f"↩️ Назад", callback_data="a/админ")])
        await self.sendMsg(text=text, keyboard=keyboard)
    async def groupInfo(self,**kwargs):
        group_id = kwargs.get('group')[0]
        groupData =GroupData()
        group_info =await groupData.get_group_info(id=group_id)
        user = await groupData.get_user(id=group_info[12])
        fleet = await groupData.get_fleet_one(id=group_info[11])
        if group_info:
            group_type ='Канал' if group_info[4]=='CHANNEL' else 'Группа'
            group_fleet_state = "⚪ Свободен" if group_info[10]==0 else "🟡 На проверке" if group_info[10]==1 else "🟢 В подборке" if group_info[10]==2 else "🚫 Заблокирован" if group_info[10]==10 else "Неизвестный статус"
            text = "✨✨✨✨✨✨✨✨✨✨✨✨\n" \
                   f"💡**Данные: {group_type}**💡\n\n" \
                   f"〖ID〗{group_info[1]}\n" \
                   f"〖Юзернейм〗{'@'+group_info[2] if group_info[2] else 'Не указан'}\n" \
                   f"〖Название〗{group_info[3]}\n" \
                   f"〖Подписчики〗{group_info[5]}\n" \
                   f"〖ID сообщения рассылки〗{group_info[7]}\n" \
                   f"〖Привлечено подписчиков〗{group_info[9]}\n" \
                   f"〖Статус〗{group_fleet_state}\n" \
                   f"〖Подборка〗{fleet[1]}\n\n" \
                   f"〖ID владельца〗{user[1]}\n" \
                   f"〖Владелец〗{user[3]}\n"
            keyboard = []
            if group_info[10] == 10:
                keyboard.append([InlineKeyboardButton("🟢 Разблокировать", callback_data=f"a/бан_гр?group={group_info[0]}")])
            else:
                keyboard.append([InlineKeyboardButton("🚫 Заблокировать", callback_data=f"a/бан_гр?group={group_info[0]}")])
            keyboard.append([InlineKeyboardButton(f"🏠 В админку", callback_data="a/админ"),
                             InlineKeyboardButton(f"↩️ Назад", callback_data=f"a/группы")])
            await self.sendMsg(text=text, keyboard=keyboard)
        else:
            await self.query.answer("Ошибка: ресурс не найден или был удалён")
    async def banGroup(self,**kwargs):
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        if group[10]==10:
            await car.put_car_pass_review(group=group, state=0, label=f"🟢 Канал разблокирован")
        else:
            await car.put_car_pass_review(group=group, state=10, label=f"🚫 Канал заблокирован администратором")
        await self.groupInfo(group=[kwargs.get('group')[0]])
        await self.reviewNotify(group=[kwargs.get('group')[0]])
    async def reviewNotify(self, **kwargs):
        '''Отправка системного уведомления владельцу'''
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        toUser = await car.get_user(id=group[12])
        notify = await car.get_notify_msg(user=toUser[0], group=group[0])
        text = "**📣Системное уведомление**📣\n" \
               f"**ID канала:** {group[1]}\n" \
               f"**Канал:** [{group[3]}]({group[6]})\n" \
               f"**Подписчиков:** {group[5]}\n" \
               f"**ID заявителя:** {toUser[1]}\n" \
               f"**Заявитель:** [{toUser[3]}](https://t.me/{toUser[2] or ''})\n"
        text += f"**Статус заявки:** {notify[3] if notify else 'Неизвестно'} "
        try:
            await self.client.send_message(chat_id=toUser[1], text=text, disable_web_page_preview=True)
        except RPCError as e:
            msg = await self.retChat()
            await msgNotify(msg=msg, text='❗Не удалось уведомить пользователя', times=5)
        if len(bot_config["msgGroup"]) > 5:
            try:
                keyboards = [[InlineKeyboardButton("➕ Участвовать", url=f"https://t.me/{bot_config['botUserName']}")]]
                await self.client.send_message(chat_id=bot_config["msgGroup"], text=text,
                                               reply_markup=InlineKeyboardMarkup(keyboards),
                                               disable_web_page_preview=True)
            except RPCError as e:
                msg = await self.retChat()
                await msgNotify(msg=msg, text='❗Не удалось уведомить группу сообщений', times=5)
class User:
    def __init__(self, Client: Client, Query: CallbackQuery = None, Msg: Message = None, Data=None):
        self.client = Client
        self.query = Query
        self.msg = Msg
        self.data = Data
    async def retChat(self):
        if self.query:
            return self.query.message
        else:
            return self.msg
    async def sendMsg(self, **kwargs):
        msg = await self.retChat()
        try:
            if self.query:
                await self.client.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=kwargs['text'],
                                                    reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                                    disable_web_page_preview=True)
            else:
                if len(bot_config.get('video')) > 24:
                    await self.client.send_video(chat_id=msg.chat.id, video=bot_config.get('video'),
                                                 caption=kwargs['text'],
                                                 reply_markup=InlineKeyboardMarkup(kwargs['keyboard']))
                else:
                    await msg.reply_text(text=kwargs['text'], reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                         disable_web_page_preview=True)
        except RPCError as e:
            print(e)
    async def inputBot(self, **kwargs):
        msg = await self.retChat()
        key = kwargs.get('k', [None])[0]
        prompt = "Введите юзернейм или имя" if key == "s" else kwargs.get('text', [''])[0]
        txt = f"👨‍💻{prompt}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def getUser(self, **kwargs):
        msg = await  self.retChat()
        WHERE, OFFSET, LIMIT = "", 0, 20
        if kwargs.get('page'):
            OFFSET = int(kwargs.get('page')[0])
        if kwargs.get('search'):
            WHERE += f"AND BINARY full_name LIKE '%{kwargs.get('search')}%' OR BINARY username LIKE '%{kwargs.get('search')}%' "
        userType = int(kwargs.get('type')[0]) if kwargs.get('type') else 0
        userS = db.select(f"SELECT (SELECT COUNT(*) FROM chat_user WHERE admin={userType}) AS total_count,"
                          f"(SELECT COUNT(*) FROM chat_user WHERE admin=0) AS state_count,"
                          f"(SELECT COUNT(*) FROM chat_user WHERE admin=1) AS admin_count")
        userList = db.select(
            f"SELECT * FROM chat_user WHERE admin IN ({userType}) " + WHERE + " ORDER BY id DESC LIMIT %s  OFFSET %s",
            (LIMIT, OFFSET))
        if userList and len(userList) > 0:
            totalPages, currentPage = math.ceil(userS[0][0] / LIMIT), int(OFFSET / LIMIT) + 1
            upPage, dowPage = OFFSET - LIMIT, OFFSET + LIMIT
            content = []
            for user in userList:
                content.append([InlineKeyboardButton(f"{'👮‍' if user[5] == 1 else '👳‍'}{user[3]}",
                                                     callback_data=f"a/инфо_юз?user={user[0]}")])
            content.append([InlineKeyboardButton(f"{'Назад' if upPage >= 0 else '-'}",
                                                 callback_data=f"a/юзеры?page={upPage}&type={userType}" if upPage >= 0 else '-'),
                            InlineKeyboardButton(f"{currentPage}/{totalPages}", callback_data="-"),
                            InlineKeyboardButton(f"{'Далее' if currentPage != totalPages else '-'}",
                                                 callback_data=f"a/юзеры?page={dowPage}&type={userType}" if currentPage != totalPages else '-')])
        else:
            content = [[InlineKeyboardButton(f"Пусто / нет пользователей", callback_data="-")]]
        keyboard = [
            [InlineKeyboardButton(f"{'🟢' if userType == 0 else ''}Пользователи", callback_data=f"a/юзеры?type=0"),
             InlineKeyboardButton(f"{'🟢' if userType == 1 else ''}Админы", callback_data=f"a/юзеры?type=1"),
             ],[InlineKeyboardButton(f"Поиск пользователя", callback_data="a/ввод_юз?k=s")],
            [InlineKeyboardButton(f"↩️ Назад", callback_data="a/админ")]]
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n\n" \
               "======**🏆 Поиск пользователей 🏆**======\n" \
               f"〖Всего〗{userS[0][0]} чел.\n" \
               f"👮‍Админов:{userS[0][2]}\n" \
               f"👳Пользователей:{userS[0][1]}\n"
        await self.sendMsg(text=text, keyboard=content+keyboard)
    async def userInfo(self, **kwargs):
        msg = await  self.retChat()
        userID = kwargs.get('user')[0]
        user = db.select(f"SELECT * FROM chat_user WHERE id = {userID}")
        print(user)
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n" \
               f"💡**Профиль пользователя**💡\n\n" \
               f"〖ID пользователя〗`{user[0][1] or 'Нет'}`(копировать)\n" \
               f"〖Юзернейм〗`{user[0][2] or 'Нет'}`(копировать)\n" \
               f"〖Имя〗`{user[0][3] or 'Нет'}`(копировать)\n" \
               f"〖Статус〗{'🟢Активен' if user[0][4] == 0 else '🔴Заблокирован'}\n" \
               f"〖Роль〗{'👮‍Администратор' if user[0][5] == 1 else '👳‍Пользователь'}\n"
        keyboard = []
        if user[0][5] == 0:
            keyboard.append([InlineKeyboardButton("🔐Назначить админом", callback_data=f"a/адм_юз?user={user[0][0]}&p=0")])
        elif user[0][5] == 1:
            keyboard.append([InlineKeyboardButton("🔓Снять админа", callback_data=f"a/адм_юз?user={user[0][0]}&p=1")])
        if user[0][4]==0:
            keyboard.append([InlineKeyboardButton("🚷 Заблокировать", callback_data=f"a/бан_юз?user={user[0][0]}")])
        else:
            keyboard.append([InlineKeyboardButton("✅ Разблокировать", callback_data=f"a/бан_юз?user={user[0][0]}")])
        keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data="a/юзеры")])
        await self.sendMsg(text=text, keyboard=keyboard)
    async def setAdmin(self, **kwargs):
        msg = await  self.retChat()
        if kwargs.get('user'):
            user = db.select(f"SELECT * FROM chat_user WHERE chat_id = {msg.chat.id}")
            if user and user[0][5] == 2:
                pa = 1 if kwargs.get('p')[0] == '0' else 0
                if db.update(f"UPDATE chat_user SET admin={pa} WHERE id={kwargs.get('user')[0]}"):
                    await self.client.answer_callback_query(self.query.id, text='Права администратора обновлены', show_alert=True)
                    await self.backReview()
                    await self.userInfo(user=kwargs.get('user'))
                else:
                    await self.client.answer_callback_query(self.query.id, text='Ошибка данных', show_alert=True)
            elif user[0][5] == 1:
                await self.client.answer_callback_query(self.query.id, text='Ошибка: у вас нет прав на назначение администраторов',
                                                        show_alert=True)
            else:
                await self.client.answer_callback_query(self.query.id, text='Ошибка: пользователь не найден',
                                                        show_alert=True)
    async def banUser(self,**kwargs):
        user = db.select("SELECT * FROM chat_user WHERE id=%s", (kwargs.get('user')[0],))
        if user[0][4]==1:
            db.update("UPDATE chat_user SET state=0 WHERE id=%s", (user[0][0],))
            await self.reviewNotify(user=[user[0][0]])
        else:
            db.update("UPDATE chat_user SET state=1 WHERE id=%s", (user[0][0],))
            await self.reviewNotify(user=[user[0][0]])
        await self.userInfo(user=[kwargs.get('user')[0]])
    async def backReview(self,**kwargs):
        # Удаление текущего сообщения
        msg =await  self.retChat()
        await self.client.delete_messages(msg.chat.id, message_ids=msg.id)
    async def reviewNotify(self, **kwargs):
        '''Отправка уведомления об изменении статуса аккаунта'''
        car = CarData()
        toUser = await car.get_user(id=kwargs.get('user')[0])
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n" \
               f"💡**Профиль пользователя**💡\n\n" \
               f"〖ID пользователя〗`{toUser[1] or 'Нет'}`(копировать)\n" \
               f"〖Юзернейм〗`{toUser[2] or 'Нет'}`(копировать)\n" \
               f"〖Имя〗`{toUser[3] or 'Нет'}`(копировать)\n" \
               f"〖Статус〗{'🟢Активен' if toUser[4] == 0 else '🔴Заблокирован'}\n"
        text += f"〖Уведомление〗** {'🟢 Ваш аккаунт разблокирован администратором' if toUser[4]==0 else '🔴 Ваш аккаунт заблокирован администратором'} "
        try:
            await self.client.send_message(chat_id=toUser[1], text=text, disable_web_page_preview=True)
        except RPCError as e:
            msg = await self.retChat()
            await msgNotify(msg=msg, text='❗Не удалось уведомить пользователя', times=5)
        if len(bot_config["msgGroup"]) > 5:
            try:
                keyboards = [[InlineKeyboardButton("➕ Участвовать", url=f"https://t.me/{bot_config['botUserName']}")]]
                await self.client.send_message(chat_id=bot_config["msgGroup"], text=text,
                                               reply_markup=InlineKeyboardMarkup(keyboards),
                                               disable_web_page_preview=True)
            except RPCError as e:
                msg = await self.retChat()
                await msgNotify(msg=msg, text='❗Не удалось уведомить группу сообщений', times=5)
class BotBlacklist:
    def __init__(self, Client: Client, Query: CallbackQuery = None, Msg: Message = None, Data=None):
        self.client = Client
        self.query = Query
        self.msg = Msg
        self.data = Data
    async def retChat(self):
        if self.query:
            return self.query.message
        else:
            return self.msg
    async def sendMsg(self, **kwargs):
        msg = await self.retChat()
        try:
            if self.query:
                await self.client.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=kwargs['text'],
                                                    reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                                    disable_web_page_preview=True)
            else:
                if len(bot_config.get('video')) > 24:
                    await self.client.send_video(chat_id=msg.chat.id, video=bot_config.get('video'),
                                                 caption=kwargs['text'],
                                                 reply_markup=InlineKeyboardMarkup(kwargs['keyboard']))
                else:
                    await msg.reply_text(text=kwargs['text'], reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                         disable_web_page_preview=True)
        except RPCError as e:
            print(e)
    async def botInput(self, **kwargs):
        msg = await self.retChat()
        prompts = {
            "add": "Введите юзернейм бота (пример @Xxbot)",
            "edit": "Введите новый юзернейм бота",
        }
        key = kwargs.get('k', [None])[0]
        item_id = kwargs.get('id', [None])[0]
        if key in prompts:
            prompt = f"{prompts[key]}:{item_id}" if item_id else prompts[key]
        else:
            prompt = kwargs.get('text', [''])[0]
        txt = f"🤖{prompt}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def index(self, **kwargs):
        '''Чёрный список ботов'''
        list = await BotBlacklistDate().get_bot_blacklist_list()
        text = "======**🏆 Чёрный список ботов 🏆**======\n" \
               "При подаче заявки и перед рассылкой проверяется наличие запрещённых ботов\n" \
               "Формат: юзернейм бота с @ (например @xxxbot)\n" \
               "Обозначения: ➕Добавить ❌Удалить 🖍Изменить\n\n" \
               "🚫**Список запрещённых ботов:**\n"
        keyboard = []
        if list:
            for index, advertising in enumerate(list):
                text += f"{index + 1}.[{advertising[1]}]({advertising[2]})\n"
                keyboard.append([InlineKeyboardButton(f"{index + 1}.{advertising[1]}", callback_data="-"),
                                 InlineKeyboardButton(f"❌ Удалить", callback_data=f"a/уд_чс?id={advertising[0]}"),
                                 InlineKeyboardButton(f"🖍 Изменить",
                                                      callback_data=f"a/ввод_чс?k=edit&id={advertising[0]}")])
        else:
            text += "Пусто, не задано"
            keyboard.append([InlineKeyboardButton(f"Список пуст", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"➕Добавить", callback_data="a/ввод_чс?k=add")])
        keyboard.append([InlineKeyboardButton(f"🏠 В админку", callback_data="a/админ"),
                         InlineKeyboardButton(f"↩️ Назад", callback_data="a/админ")])
        await self.sendMsg(text=text, keyboard=keyboard)
    async def delBotBlacklist(self, **kwargs):
        '''Удаление бота из чёрного списка'''
        msg = await self.retChat()
        id = kwargs.get('id')[0]
        delData = await BotBlacklistDate().del_bot_blacklist(id=id)
        if delData:
            await self.query.answer(text="✅Удалено успешно", cache_time=5)
            await self.index()
        else:
            await msgNotify(msg=msg, text="❕Не удалось удалить")
