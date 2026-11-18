import logging
import os.path

import emoji
from config import *
from data.data import *
class Router:
    def __init__(self):
        self.routes = []
    def add_route(self, path_pattern, handler_class, handler_method):
        # 将路径模式转换为正则表达式，并提取参数名
        param_pattern = re.compile(r'<(\w+)>')
        path_pattern = param_pattern.sub(r'(?P<\1>[^/]+)', path_pattern)
        path_regex = re.compile(f"^{path_pattern}$")
        param_names = param_pattern.findall(path_pattern)
        # 将路由规则存储为元组
        self.routes.append((path_regex, param_names, handler_class, handler_method))
    async def route(self, url, *args, **kwargs):
        parsed_url = urlparse(url)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        # 遍历所有路由规则，查找匹配的规则
        for path_regex, param_names, handler_class, handler_method in self.routes:
            match = path_regex.match(path)
            if not match:
                continue
            # 将路径参数存储到 query_params 参数中 中
            for param_name in param_names:
                query_params[param_name] = match.group(param_name)
            # 创建处理器实例，并调用相应方法，将查询参数和路径参数传递进去
            try:
                handler = handler_class(*args, **kwargs)
                return await getattr(handler, handler_method)(**query_params)
            except (RPCError,Exception) as e:
                raise ValueError(f"路由执行 {handler_method} 方法错误:{e}")
        raise ValueError("开发中-导航页面不存在")

class RestrictAccess:
    # 访问控制
    def __init__(self, Msg: Message = None):
        self.msg = Msg
    async def limit_check(self):
        # 检测用户是否频繁访问触发限制
        msg=self.msg
        try:
            count = redis_client.get(f"restrict{msg.chat.id}")
            print(count)
            if count is None or int(count)<int(bot_config['restrict_limit']):
                redis_client.incr(f"restrict{msg.chat.id}")
                if count is None:
                    redis_client.expire(f"restrict{msg.chat.id}", 60)
                return True
            else:
                if int(count)==int(bot_config['restrict_limit']):
                    redis_client.incr(f"restrict{msg.chat.id}")
                    redis_client.expire(f"restrict{msg.chat.id}", 60*10)
                    await msg.reply_text('访问频率过高限制访问-10')
                return False
        except Exception as e:
            logging.error(f"访问限制错误：{e}")
            return False

class UserAuth:
    # 用户认证
    def __init__(self, Msg: Message = None):
        self.msg = Msg
    async def auth(self,FromUser=None):
        '''
        用户验证系统:从redis内查询用户，有就判断权限返回，
        没有就走数据库读取，如果数据库内不存在就创建一个新用户
        :param message:
        :return:
        '''
        msg =self.msg
        try:
            name = f"user{FromUser.id}"
            redis_client.delete(name)
            user = redis_client.get(name)
            if user:
                user = json.loads(user)
            else:
                dbUser = ChatUser(Msg=msg)
                user = dbUser.get_or_create(FromUser)
                redis_client.set(name, json.dumps(user,default=str),ex=600)
            if user[4] == 1:
                await msg.reply_text("账号已被管理员封禁")
                return False
            return user
        except Exception as e:
            logging.error(f"账号访问错误{e}")
            await msg.reply_text("账号访问错误")
            return False

class Var:
    def __init__(self, Msg: Message = None):
        self.msg = Msg
    def write(self,value=None):
        msg=self.msg
        if value:
            try:
                name=f"var{msg.chat.id}"
                redis_client.set(name,json.dumps(value,default=str),ex=60*2)
                return True
            except Exception as e:
                print(e)
        return False

async def truncate_string(string, length):
    '''标题截取'''
    pattern = r":[^:]+:"
    newStr = re.sub(pattern, "", emoji.demojize(string))
    if len(newStr) > length:
        return newStr[:length] + ".."
    else:
        return newStr

async def isPrivileges(chatId,typeG):
    # 权限判断
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

def get_config():
    try:
        configData=ConfigData()
        configList = configData.get_config_list()
        if configList:
            bot_config["rejectText"]=[]
            for config in configList:
                if config[1]=="rejectText":
                    bot_config["rejectText"].append(config[2])
                else:
                    bot_config[config[1]]=config[2]
        return bot_config
    except Exception as e:
        logging.error('读取配置错误',e)

async def timeJob(arr):
    await app.delete_messages(arr.get('id'), message_ids=arr.get('message_ids'))
async def msgNotify(msg:Message,text='无',times=2):
    msgId = await msg.reply_text(text=f"{str(text)} \n({times}秒后删除)")
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
            # 报错机器人没在群
            pass
    return isBot

async def send_msg(chat_id,text):
    try:
        await app.send_message(chat_id=int(chat_id), text=text)
    except RPCError as e:
        logging.error('发送消息失败:',chat_id,'-错误:',e)
async def convoyDriving():
    fleet_list = db.select(f"SELECT * FROM fleet_list WHERE state = 1 ")
    print('开始发车')
    if fleet_list:
        for fleet in fleet_list:
            print('发车车次',fleet)
            group_list = db.select(f"SELECT * FROM group_list WHERE fleet_list=%s AND state=2", (fleet[0],))
            print('车内群组:', len(group_list))
            if group_list and len(group_list)>=1:
                for group in group_list:
                    user = db.select("SELECT * FROM chat_user WHERE id=%s", (group[12],))
                    if not user:
                        continue
                    isPrivi = await isPrivileges(chatId=group[1], typeG=group[4])
                    if isPrivi == 1:
                        print('发车检查:机器人被取消了权限-',group[3])
                        db.update("UPDATE group_list SET state=0, WHERE id=%s", (group[0],))
                        text = f"发车检查:《[{group[3]}]({group[6]})》 " \
                               f"中机器人权限不足,此群即将下车请检查"
                        await send_msg(chat_id=user[0][1], text=text)
                        continue
                    elif isPrivi == 2:
                        print('发车检查:机器人未入群-',group[3])
                        db.update("UPDATE group_list SET state=0 WHERE id=%s", (group[0],))
                        text = f"发车检查:《[{group[3]}]({group[6]})》 " \
                               f"中未检测到机器人,此群即将下车请检查"
                        await send_msg(chat_id=user[0][1], text=text)
                        continue
                    if group[7] !=0:
                        getMsg = await app.get_messages(chat_id=group[1], message_ids=int(group[7]))
                        if not getMsg.text:
                            db.update("UPDATE group_list SET state=0 WHERE id=%s", (group[0],))
                            text = f"发车检查:《[{group[3]}]({group[6]})》 " \
                                   f"中未检测到上一次发送的消息,已做下车处理"
                            await send_msg(chat_id=user[0][1], text=text)
                            continue
                    text_list = await marshalling(group_chat=group,fleet=fleet)
                    print('组装的列表',text_list)
                    if len(text_list)>2:
                        keyboard = [
                            [
                                InlineKeyboardButton("➕ 参加互推", url=f"https://t.me/{bot_config.get('botUserName').replace('@', '')}"),
                                InlineKeyboardButton("📣 供需发布", url=f"https://t.me/jindun")
                            ]
                        ]
                        msg = await app.send_message(chat_id=group[1], text=''.join(text_list),
                                                     reply_markup=InlineKeyboardMarkup(keyboard),
                                                     disable_web_page_preview=True, disable_notification=True)
                        if msg.id:
                            db.update("UPDATE group_list SET msg_id=%s WHERE group_id=%s", (msg.id, group[1]))
                            try:
                                if group[7] !=0:
                                    await app.delete_messages(chat_id=group[1], message_ids=int(group[7]))
                            except RPCError as e:
                                print('删除上一条消息失败-',group[2])
async def marshalling(group_chat=None, fleet=None):
        new_car_list, index = [], 1
        new_car_list.append(f"**⛩️[{fleet[1]}|{bot_config['botName']}](https://t.me/{bot_config.get('botUserName').replace('@', '')}/)⛩️**\n")
        advertising_list = await AdvertisingData().get_advertising_list()
        if len(advertising_list) >= 1:
            new_car_list.append(f"**AD:[{advertising_list[0][1]}]({advertising_list[0][2]})**\n\n")
        group_list = db.select(f"SELECT * FROM group_list WHERE fleet_list=%s AND state=2", (fleet[0],))
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
                        db.update("UPDATE group_list SET state=0 WHERE id=%s", (group[0],))
                        print('删除了链接')
                        continue
                except RPCError as e:
                    print('编辑链接失败',e)
                    db.update("UPDATE group_list SET state=0 WHERE id=%s", (group[0],))
                    continue
            else:
                continue
        try:
            link_group = await app.edit_chat_invite_link(int(group_chat[1]), group_chat[6])
            print(link_group.member_count)
            if link_group and link_group.is_revoked == False:
                db.update("UPDATE group_list SET input_fan=%s WHERE id=%s",
                              (link_group.member_count or 0, group_chat[0]))
        except RPCError as e:
            print('更新群链接入群人数错误', e)
        if len(advertising_list) >=2:
            new_car_list.append(f"\n**AD:[{advertising_list[1][1]}]({advertising_list[1][2]})**")
        if len(advertising_list) >= 3:
            new_car_list.append(f"\n**AD:[{advertising_list[2][1]}]({advertising_list[2][2]})**")
        new_car_list.append(f"**\n互推交流: {bot_config.get('publicGroup')}**")
        return new_car_list


