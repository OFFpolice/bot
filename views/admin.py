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
               "======**🏆 后台管理 🏆**======\n\n" \
               "🌟**欢迎管理员:**🌟\n" \
               "  ✅可以在此管理机器人功能"
        keyboard = [
            [InlineKeyboardButton("☸️ 机器人配置", callback_data="a/机器人配置"),
            InlineKeyboardButton("🅰️️ 广告管理", callback_data="a/广告管理")],
            [InlineKeyboardButton("🚒 车队管理", callback_data="a/车队管理"),
            InlineKeyboardButton("📇 群频管理", callback_data="a/群频管理")],
            [InlineKeyboardButton("🤖 Bot黑名单", callback_data="a/Bot黑名单"),
             InlineKeyboardButton("👨‍💻 用户管理", callback_data="a/用户管理")],
        ]
        await self.sendMsg(text=text, keyboard=keyboard)

    async def config(self, **kwargs):
        bot_config = get_config()
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n\n" \
               "======**🏆 机器人配置 🏆**======\n\n" \
               f"**🔸初始化菜单:** 初始化用户菜单命令\n" \
               f"**🔸机器人名字:** {bot_config['botName']}\n" \
               f"**🔸机器人账号:** {bot_config['botUserName']}\n" \
               f"**🔸首页欢迎词:**\n'{bot_config['indexTxt']}'\n" \
               f"**🔸审核拒绝词:**\n{'|'.join(bot_config['rejectText'])}\n" \
               f"**🔸视频介绍:** {'🟢 已上传' if len(bot_config['video']) > 20 else '🚫 未上传'}\n" \
               f"**🔸管理群组:** {bot_config['adminGroup']}\n" \
               f"**🔸消息群组:** {bot_config['msgGroup']}\n" \
               f"**🔸交流群组:** {bot_config['publicGroup']}\n" \
               f"**🔸访问限制:** {bot_config['restrict_limit']} \n(60秒内访问次数超过禁用用户5分钟)"
        keyboard = [
            [InlineKeyboardButton(f"初始化菜单", callback_data="a/初始化菜单")],
             [InlineKeyboardButton(f"修改机器人名字", callback_data="a/修改配置?text=请输入机器人名"),
             InlineKeyboardButton(f"修改机器人账号", callback_data="a/修改配置?text=请输入机器人账号:例子:@xxbot")],
            [InlineKeyboardButton(f"修改首页欢迎词", callback_data="a/修改配置?text=请输入首页欢迎词"),
             InlineKeyboardButton(f"修改审核拒绝词", callback_data="a/审核拒绝词")],
            [InlineKeyboardButton(f"修改视频介绍", callback_data="a/修改配置?text=请上传视频介绍"),
             InlineKeyboardButton(f"修改管理群组", callback_data="a/修改配置?text=请输入管理群组")],
            [InlineKeyboardButton(f"修改消息群组", callback_data="a/修改配置?text=请输入消息群组"),
             InlineKeyboardButton(f"修改交流群组", callback_data="a/修改配置?text=请输入交流群组:例子@xxx")],
            [InlineKeyboardButton(f"修改访问限制", callback_data="a/修改配置?text=请输入访问限制:回复数字1到60")],
            [InlineKeyboardButton(f"↩️ 返回", callback_data="a/管理首页")],
        ]
        await self.sendMsg(text=text, keyboard=keyboard)

    async def modifBot(self, **kwargs):
        msg = await self.retChat()
        txt = f"📲{kwargs.get('text')[0]}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def initialization(self,**kwargs):
        initial =await app.set_bot_commands([BotCommand("start", "首页"), BotCommand("help", "帮助")])
        print(initial)
        if initial:
            await self.query.answer(text=f'初始化菜单成功', show_alert=True)

    async def reviewRejectionWords(self, **kwargs):
        '''审核拒绝词列表'''
        rejectText_list = await ConfigData().get_rejectText_list()
        text = "======**🏆 预设审核拒绝词 🏆**======\n" \
               "在拒绝用户提交申请时快捷选择拒绝理由\n" \
               "图示介绍：➕添加 ❌删除 🖍修改\n\n" \
               "🚫**预设拒绝审核词列表:**\n"
        keyboard = []
        print(rejectText_list)
        if rejectText_list:
            for index, rejectText in enumerate(rejectText_list):
                text += f"{index + 1}.{rejectText[2]}\n"
                keyboard.append([InlineKeyboardButton(f"{index + 1}.{rejectText[2]}", callback_data="-"),
                                 InlineKeyboardButton(f"❌ 删除", callback_data=f"a/删审核拒绝词?id={rejectText[0]}"),
                                 InlineKeyboardButton(f"🖍 修改",
                                                      callback_data=f"a/修改配置?text=请输入新的审核拒绝词:{rejectText[0]}")])
        else:
            text += "空,未设置"
            keyboard.append([InlineKeyboardButton(f"列表为空", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"➕添加", callback_data="a/修改配置?text=请输入审核拒绝词")])
        keyboard.append([InlineKeyboardButton(f"🏠 管理首页", callback_data="a/管理首页"),
                         InlineKeyboardButton(f"↩️ 返回", callback_data="a/机器人配置")])
        await self.sendMsg(text=text, keyboard=keyboard)

    async def delReviewRejectionWords(self, **kwargs):
        '''删审核拒绝词'''
        msg = await self.retChat()
        id = kwargs.get('id')[0]
        delData = await ConfigData().del_rejectText(id=id)
        if delData:
            await self.query.answer(text="✅删除成功", cache_time=5)
            await self.reviewRejectionWords()
        else:
            await msgNotify(msg=msg, text="❕删除失败")

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
        txt = f"🗞️{kwargs.get('text')[0]}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def index(self, **kwargs):
        '''广告管理'''
        advertising_list = await AdvertisingData().get_advertising_list()
        text = "======**🏆 广告管理 🏆**======\n" \
               "发车时候添加的广告\n" \
               "添加示例:互推&https://t.me/+oYUJoUkMlfphN2M1\n" \
               "图示介绍：➕添加 ❌删除 🖍修改\n\n" \
               "🚫**广告列表列表:**\n"
        keyboard = []
        if advertising_list:
            for index, advertising in enumerate(advertising_list):
                text += f"{index + 1}.[{advertising[1]}]({advertising[2]})\n"
                keyboard.append([InlineKeyboardButton(f"{index + 1}.{advertising[1]}", callback_data="-"),
                                 InlineKeyboardButton(f"❌ 删除", callback_data=f"a/删广告词?id={advertising[0]}"),
                                 InlineKeyboardButton(f"🖍 修改",
                                                      callback_data=f"a/广告输入?text=请输入新的广告:{advertising[0]}")])
        else:
            text += "空,未设置"
            keyboard.append([InlineKeyboardButton(f"列表为空", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"➕添加", callback_data=f"a/广告输入?text=请输入广告:例:XX互推&网址")])
        keyboard.append([InlineKeyboardButton(f"🏠 管理首页", callback_data="a/管理首页"),
                         InlineKeyboardButton(f"↩️ 返回", callback_data="a/管理首页")])
        await self.sendMsg(text=text, keyboard=keyboard)
    async def delAdvertising(self, **kwargs):
        '''删审核拒绝词'''
        msg = await self.retChat()
        id = kwargs.get('id')[0]
        delData = await AdvertisingData().del_advertising(id=id)
        if delData:
            await self.query.answer(text="✅删除成功", cache_time=5)
            await self.index()
        else:
            await msgNotify(msg=msg, text="❕删除失败")
class Car:
    # 车队管理
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
        txt = f"🚒{kwargs.get('text')[0]}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def index(self, **kwargs):
        '''车队管理首页'''
        msg = await self.retChat()
        user = self.data.get('user')
        try:
            if user:
                text = f"**🚀Telegram互推:**  @{bot_config.get('botUserName')}\n\n" \
                       f"**UID {user[1]}** 尊敬的管理员 {user[3]} 你好:\n\n" \
                       f"**自动互推机器人**\n\n" \
                       f"👇点击选择频道或群组进入相应的管理页面\n"
                keyboard = [
                    [InlineKeyboardButton("🏵️频道互推管理🏵️", callback_data="a/频道车队管理")],
                    [InlineKeyboardButton("🌸群组互推管理🌸", callback_data="a/群组管理")],
                    [InlineKeyboardButton(f"↩️ 返回", callback_data="a/管理首页")]
                ]
                await self.sendMsg(text=text, keyboard=keyboard)
        except (RPCError, Exception) as E:
            print(E)
            await msg.reply_text(text=f'错误:请截图联系客服{E}')
    # 频道车队
    async def channel_car(self,**kwargs):
        OFFSET, LIMIT = int(kwargs.get('page')[0]) if kwargs.get('page') else 0, 20
        fleet = CarData()
        fleetList, count =await fleet.get_fleet(OFFSET=OFFSET, LIMIT=LIMIT)
        keyboard = []
        text = f"频道-车队大厅\n\n" \
               f"选择下方车队进入指定车队，然后选择你要申请的分组进行上车提交。\n\n" \
               f"格式介绍:\n" \
               f"🚒发车/🕛等待 车队名|队内成员数-最大成员数|最小订阅需求\n\n" \
               f"点击下方符合车队进入提交申请"
        if fleetList:
            totalPages, currentPage = math.ceil(count / LIMIT), math.ceil(OFFSET / LIMIT) + 1
            upPage, dowPage = OFFSET - LIMIT, OFFSET + LIMIT
            row, step = [], 2
            for i in range(0, len(fleetList), step):
                batch = fleetList[i:i + step]
                for Cont in batch:
                    row.append(InlineKeyboardButton(
                        f"{'🚒' if Cont[4] == 1 else '🕛'} {Cont[1]}|{Cont[11]}/{Cont[6]}|{Cont[8] / 1000}K",
                        callback_data=f"a/频道车队详情?fleet={Cont[0]}"))
                keyboard.append(row)
                row = []
            keyboard.append([InlineKeyboardButton(f"{'⬅️上一页' if upPage >= 0 else '-'}",
                                                  callback_data=f"a/频道车队管理?page={upPage}" if upPage >= 0 else '-'),
                             InlineKeyboardButton(f"{currentPage}/{totalPages}页", callback_data="-"),
                             InlineKeyboardButton(f"️{'➡️下一页' if currentPage != totalPages else '-'}",
                                                  callback_data=f"a/频道车队管理?page={dowPage}" if currentPage != totalPages else '-')])
        else:
            keyboard.append([InlineKeyboardButton(f"空/未发现车队", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"➕ 添加车队", callback_data="a/车队输入?text=请输入频道车队标题")])
        keyboard.append([InlineKeyboardButton(f"🏠 管理首页", callback_data="a/管理首页"),
                         InlineKeyboardButton(f"↩️ 返回", callback_data="a/车队管理")])
        await self.sendMsg(text=text, keyboard=keyboard)
    async def channel_fleet_info(self,**kwargs):
        fleet_id = kwargs.get("fleet")[0]
        fleet=CarData()
        fleetInfo,group_list=await fleet.get_fleet_one(id=fleet_id),await fleet.get_fleet_group_list(id=fleet_id)
        if fleetInfo:
            text = f"**车队标题：** {fleetInfo[1]}\n" \
                      f"**车队介绍：** {fleetInfo[2]}\n" \
                      f"**当前/最大(成员)：** {fleetInfo[11]}/{fleetInfo[6]}\n" \
                      f"**车队类型：** 频道\n" \
                      f"**最低订阅：** {fleetInfo[8] / 10000} W人\n" \
                      f"**最低阅读：**{fleetInfo[9]}\n" \
                      f"**开车状态：**{'🚒 已开车' if fleetInfo[4] == 1 else '🕛 未开车'} \n\n" \
                      "**成员列表：**\n"
            keyboard=[]
            if group_list:
                group_id,row=[],1
                for index,group in enumerate(group_list):
                    text+=f"{index+1}.[{await truncate_string(group[3],20)}]({group[6]}) {round(group[5]/1000,1)}k\n"
                    group_id.append(InlineKeyboardButton(f"{index+1}", callback_data=f"a/频道车队频道详细?fleet={fleetInfo[0]}&group={group[0]}"))
                    if index+1==8*row or ((len(group_list)-(index+1))<8 and len(group_list)==(index+1)):
                        row+=1
                        keyboard.append(group_id)
                        group_id=[]
            else:
                text+="当前没有互推成员\n"
            if fleetInfo[6]>fleetInfo[11]:
                text+="\n✅车队还未满员"
            else:
                text+="\n‼️车队已满"
            keyboard.append([InlineKeyboardButton(f"=========车队资料编辑=========", callback_data="-")])
            keyboard.append([InlineKeyboardButton(f"标题️",callback_data=f"a/车队输入?text=请输入频道车队新标题:{fleetInfo[0]}"),
                             InlineKeyboardButton(f"介绍️",callback_data=f"a/车队输入?text=请输入频道车队新介绍:{fleetInfo[0]}"),
                             InlineKeyboardButton(f"成员",callback_data=f"a/车队输入?text=请输入频道车队新最大成员数:{fleetInfo[0]}"),
                             InlineKeyboardButton(f"订阅",callback_data=f"a/车队输入?text=请输入频道车队新最低订阅:{fleetInfo[0]}"),
                             InlineKeyboardButton(f"阅读️",callback_data=f"a/车队输入?text=请输入频道车队新最低阅读:{fleetInfo[0]}")])
            keyboard.append([InlineKeyboardButton(f"状态: {'🚒 已开车' if fleetInfo[4] == 1 else '🕛 未开车'}", callback_data=f"a/频道管理频道状态?fleet={fleetInfo[0]}&state={fleetInfo[4]}")])
            keyboard.append([InlineKeyboardButton(f"🏠 管理首页", callback_data="a/管理首页"),
                             InlineKeyboardButton(f"↩️ 返回", callback_data="a/频道车队管理")])
            await self.sendMsg(text=text,keyboard=keyboard)
    async def channel_fleet_state(self,**kwargs):
        msg = await self.retChat()
        fleet_id,state = kwargs.get("fleet")[0],kwargs.get("state")[0]
        carData = CarData()
        if state=='0':
            await carData.put_car_state(text=1, id=fleet_id)
            await msgNotify(msg=msg, text='开车成功')
        else:
            await carData.put_car_state(text=0, id=fleet_id)
            await msgNotify(msg=msg, text='停车成功')
        await self.channel_fleet_info(fleet=[fleet_id])
    async def channel_info(self,**kwargs):
        group_id = kwargs.get('group')[0]
        car = CarData()
        group = await car.get_user_group_one(id=group_id)
        fleetInfo = await car.get_fleet_one(id=group[11])
        user = await car.get_user(id=group[12])
        notify = await car.get_notify_msg(user=user[0], group=group[0])
        text = f"**申请车队名:** {fleetInfo[1]}\n" \
               f"**车队类型:** 频道\n" \
               f"**车队介绍:** {fleetInfo[2]}\n" \
               f"**当前/最大(成员):** {fleetInfo[11]}/{fleetInfo[6]}\n" \
               f"**最低订阅:** {fleetInfo[8] / 10000} W人\n" \
               f"**最低阅读:** {fleetInfo[9]}\n\n" \
               f"**频道ID:** {group[1]}\n" \
               f"**申请频道:** [{group[3]}]({group[6]})\n" \
               f"**订阅人数:** {group[5]}\n" \
               f"**申请人ID:** {user[1]}\n" \
               f"**申请人名:** [{user[3]}](https://t.me/{user[2] or ''})\n"
        text += f"**申请状态:**  {notify[3] if notify else '未知'} "
        keyboard=[]
        if group[10]==2:
            keyboard.append([InlineKeyboardButton("⏬ 下车", callback_data=f"a/频道管理上下车?group={group[0]}")])
        elif group[10] in [0,1]:
            keyboard.append([InlineKeyboardButton("⏫ 上车", callback_data=f"a/频道管理上下车?group={group[0]}")])
        if group[10] == 10:
            keyboard.append([InlineKeyboardButton("🟢 解群", callback_data=f"a/频道管理启禁群?group={group[0]}")])
        else:
            keyboard.append([InlineKeyboardButton("🚫 禁群", callback_data=f"a/频道管理启禁群?group={group[0]}")])
        keyboard.append([InlineKeyboardButton(f"🏠 管理首页", callback_data="a/管理首页"),
                         InlineKeyboardButton(f"↩️ 返回", callback_data=f"a/频道车队详情?fleet={fleetInfo[0]}")])
        await self.sendMsg(text=text,keyboard=keyboard)
    async def downGroup(self, **kwargs):
        '''下车'''
        print(kwargs.get('group')[0])
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        if group[10]==2:
            await car.put_car_pass_review(group=group, state=0, label=f"🔴 频道已被管理员下车")
        elif group[10]==0:
            await car.put_car_pass_review(group=group, state=2, label=f"🟢 频道已被管理员上车")
        await self.channel_info(group=[kwargs.get('group')[0]])
        await self.reviewNotify(group=[kwargs.get('group')[0]])
    async def banGroup(self,**kwargs):
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        if group[10]==10:
            await car.put_car_pass_review(group=group, state=0, label=f"🟢 频道已解除禁用")
        else:
            await car.put_car_pass_review(group=group, state=10, label=f"🚫 频道已被管理员禁用")
        await self.channel_info(group=[kwargs.get('group')[0]])
        await self.reviewNotify(group=[kwargs.get('group')[0]])
    async def reviewNotify(self, **kwargs):
        '''组装消息通知用户'''
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        fleet = await car.get_fleet_one(id=group[11])
        toUser = await car.get_user(id=group[12])
        notify = await car.get_notify_msg(user=toUser[0], group=group[0])
        text = "**📣系统通知**📣\n" \
               f"**申请车队名:** {fleet[1]}\n" \
               f"**车队类型:** 频道\n" \
               f"**车队介绍:** {fleet[2]}\n" \
               f"**当前/最大(成员):** {fleet[11]}/{fleet[6]}\n" \
               f"**最低订阅:** {fleet[8] / 10000} W人\n" \
               f"**最低阅读:** {fleet[9]}\n\n" \
               f"**频道ID:** {group[1]}\n" \
               f"**申请频道:** [{group[3]}]({group[6]})\n" \
               f"**订阅人数:** {group[5]}\n" \
               f"**申请人ID:** {toUser[1]}\n" \
               f"**申请人名:** [{toUser[3]}](https://t.me/{toUser[2] or ''})\n"
        text += f"**申请状态:** {notify[3] if notify else '未知'} "
        try:
            await self.client.send_message(chat_id=toUser[1], text=text, disable_web_page_preview=True)
        except RPCError as e:
            msg = await self.retChat()
            await msgNotify(msg=msg, text='❗通知用户失败', times=5)
        if len(bot_config["msgGroup"]) > 5:
            try:
                keyboards = [[InlineKeyboardButton("➕ 参加互推", url=f"https://t.me/{bot_config['botUserName']}")]]
                await self.client.send_message(chat_id=bot_config["msgGroup"], text=text,
                                               reply_markup=InlineKeyboardMarkup(keyboards),
                                               disable_web_page_preview=True)
            except RPCError as e:
                msg = await self.retChat()
                await msgNotify(msg=msg, text='❗通知消息群失败', times=5)
class Review:
    # 审核群组内审核
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
        txt = f"💭{kwargs.get('text')[0]}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def passReview(self, **kwargs):
        '审核通过'
        msg = await  self.retChat()
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        fleetInfo =await car.get_fleet_one(id=group[11])
        if not fleetInfo:
            await car.put_car_pass_review(group=group, state=0, label='审核失败:车队不存在')
            await msgNotify(msg=msg, text='❌车队不存在',times=5)
        elif not fleetInfo[6]>fleetInfo[11]:
            await car.put_car_pass_review(group=group, state=0, label='审核失败:队列已满自动拒绝')
            await msgNotify(msg=msg, text='❌队列已满自动拒绝',times=5)
        try:
            link = await app.create_chat_invite_link(group[1])
            link = link.invite_link
            # link="https://t.me/+629C4CiltehmZjg1"
            await car.put_car_pass_review(group=group,state=2,label='审核成功',url=link)
        except RPCError as e:
            await car.put_car_pass_review(group=group, state=0, label='审核失败:无邀请权限')
            await msgNotify(msg=msg, text='❌无生成链接权限已拒绝',times=5)
        text,keyboard,user = await self.reviewNotify(group=[group[0]])
        await self.sendReviewInfo(text=[text],keyboard=[keyboard],user_id=[user])
    async def rejectReview(self,**kwargs):
        rejectText = await ConfigData().get_rejectText_list()
        content = []
        if rejectText:
            for audit in rejectText:
                content.append([InlineKeyboardButton(f"{audit[2]}",callback_data=f"a/拒绝原因?group={kwargs.get('group')[0]}&reason={audit[0]}")])
        content.append([InlineKeyboardButton(f"🔡 自定义拒绝原因", callback_data=f"a/自定义原因?text=请输入自定义拒绝原因:{kwargs.get('group')[0]}")
                        ,InlineKeyboardButton(f"↩️ 返回", callback_data=f"a/拒绝返回?group={kwargs.get('group')[0]}")])
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n\n" \
                   "======**🏆 拒绝原因 🏆**======\n" \
                   f"请选择拒绝原因" \
                   f"拒绝审核词在机器人配置内设置"
        await self.sendMsg(text=text,keyboard=content)
    async def rejectReason(self,**kwargs):
        msg = await self.retChat()
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        fleetInfo = await car.get_fleet_one(id=group[11])
        if not fleetInfo:
            await car.put_car_pass_review(group=group, state=0, label='审核失败:车队不存在')
            await msgNotify(msg=msg, text='❌车队不存在')
        if group:
            reply = {}
            if self.query:
                Text = await car.get_rejectText(id=kwargs.get('reason')[0])
                reply["Text"] = Text[2]
            else:
                reply["Text"] = kwargs.get('reason')[0]
                reply["reply_id"] = msg.reply_to_message.reply_to_message_id
            if await car.put_car_pass_review(group=group, state=0, label=f"审核失败:{reply['Text']}"):
                text, keyboard, user = await self.reviewNotify(group=[group[0]])
                await self.sendReviewInfo(text=[text], keyboard=[keyboard], user_id=[user],reply_id=[reply.get("reply_id")])
    async def rejectBack(self,**kwargs):
        '''返回审核信息详情'''
        text,keyboard,user = await self.reviewNotify(group=[kwargs.get("group")[0]])
        await self.sendMsg(text=text,keyboard=keyboard)
    async def reviewNotify(self,**kwargs):
        '''组装申请消息'''
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        fleet = await car.get_fleet_one(id=group[11])
        toUser=  await car.get_user(id=group[12])
        notify =await car.get_notify_msg(user=toUser[0],group=group[0])
        text = "**📣系统通知**📣\n" \
               f"**申请车队名:** {fleet[1]}\n" \
               f"**车队类型:** 频道\n" \
               f"**车队介绍:** {fleet[2]}\n" \
               f"**当前/最大(成员):** {fleet[11]}/{fleet[6]}\n" \
               f"**最低订阅:** {fleet[8] / 10000} W人\n" \
               f"**最低阅读:** {fleet[9]}\n\n" \
               f"**频道ID:** {group[1]}\n" \
               f"**申请频道:** [{group[3]}]({group[6]})\n" \
               f"**订阅人数:** {group[5]}\n" \
               f"**申请人ID:** {toUser[1]}\n" \
               f"**申请人名:** [{toUser[3]}](https://t.me/{toUser[2] or ''})\n"
        keyboard=[]
        if group[10]==1:
            text+=f"**申请状态:** 🔵 {notify[3] if notify else '未知'} "
            keyboard.append([InlineKeyboardButton("🟢 通过审核", callback_data=f"a/通过审核?group={group[0]}"),
                     InlineKeyboardButton("❌ 拒绝审核", callback_data=f"a/拒绝审核?group={group[0]}")])
            keyboard.append([InlineKeyboardButton("🚫 禁群", callback_data=f"a/审核禁群?group={group[0]}")])
        elif group[10]==2:
            text+=f"**申请状态:** 🟢 {notify[3] if notify else '未知'} "
            keyboard.append([InlineKeyboardButton("⏬ 下车", callback_data=f"a/审核下车?group={group[0]}")])
            keyboard.append([InlineKeyboardButton("🚫 禁群", callback_data=f"a/审核禁群?group={group[0]}")])
        elif group[10]==10:
            text+=f"**申请状态:** 🚫 {notify[3] if notify else '未知'}"
            keyboard.append([InlineKeyboardButton("🟢 解群", callback_data=f"a/审核禁群?group={group[0]}")])
        else:
            text+=f"**申请状态:** ⚪ {notify[3] if notify else '未知'}"
            keyboard.append([InlineKeyboardButton("🚫 禁群", callback_data=f"a/审核禁群?group={group[0]}")])
        return text,keyboard,toUser
    async def sendReviewInfo(self,**kwargs):
        '''发送审核消息'''
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
            await msgNotify(msg=msg, text='❗通知用户失败', times=5)
        if len(bot_config["msgGroup"]) > 5:
            try:
                keyboards = [[InlineKeyboardButton("➕ 参加互推", url=f"https://t.me/{bot_config['botUserName']}")]]
                await self.client.send_message(chat_id=bot_config["msgGroup"], text=text,
                                               reply_markup=InlineKeyboardMarkup(keyboards),
                                               disable_web_page_preview=True)
            except RPCError as e:
                await msgNotify(msg=msg, text='❗通知消息群失败', times=5)
    # 状态操作
    async def banGroup(self,**kwargs):
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        if group[10]==10:
            await car.put_car_pass_review(group=group, state=0, label=f"您的频道已解除禁用")
        else:
            await car.put_car_pass_review(group=group, state=10, label=f"您的频道已被管理员禁用")
        text, keyboard, user = await self.reviewNotify(group=kwargs.get('group'))
        await self.sendReviewInfo(text=[text], keyboard=[keyboard], user_id=[user])
    async def downGroup(self, **kwargs):
        '''下车'''
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        if group:
            await car.put_car_pass_review(group=group, state=0, label=f"您的频道已被管理员下车")
        text, keyboard, user = await self.reviewNotify(group=kwargs.get('group'))
        await self.sendReviewInfo(text=[text], keyboard=[keyboard], user_id=[user])
class Group:
    # 群频道管理
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
        txt = f"🏵️‍{kwargs.get('text')[0]}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def index(self,**kwargs):
        OFFSET, LIMIT = int(kwargs.get('page')[0]) if kwargs.get('page') else 0, 20
        search=kwargs.get('search')
        groupData = GroupData()
        group  = await groupData.get_group_list(OFFSET=OFFSET, LIMIT=LIMIT,search=search)
        group_count = await groupData.get_group_index_count()
        keyboard = []
        text = f"群频道-管理首页\n\n" \
               f"群频总数:{group_count[0]}\n" \
               f"频道总数:{group_count[1]}|上车{group_count[2]}|下车{group_count[1]-group_count[2]}\n" \
               f"群组总数:{group_count[3]}|上车{group_count[4]}|下车{group_count[3]-group_count[4]}\n" \
               f"图示介绍:\n" \
               f"🏵️‍频道/🌸群组-群｜频道名字\n\n" \
               f"点击下方按钮进行更多操作"
        if group and group_count:
            totalPages, currentPage = math.ceil(group_count[0] / LIMIT), math.ceil(OFFSET / LIMIT) + 1
            upPage, dowPage = OFFSET - LIMIT, OFFSET + LIMIT
            for key in group:
                keyboard.append([InlineKeyboardButton(f"{'🏵️‍' if key[4] == 'CHANNEL' else '🌸'}-{key[3]} ",callback_data=f"a/群频详情?group={key[0]}")])
            keyboard.append([InlineKeyboardButton(f"{'⬅️上一页' if upPage >= 0 else '-'}",
                                                  callback_data=f"a/群频管理?page={upPage}" if upPage >= 0 else '-'),
                             InlineKeyboardButton(f"{currentPage}/{totalPages}页", callback_data="-"),
                             InlineKeyboardButton(f"️{'➡️下一页' if currentPage != totalPages else '-'}",
                                                  callback_data=f"a/群频管理?page={dowPage}" if currentPage != totalPages else '-')])
        else:
            keyboard.append([InlineKeyboardButton(f"空/未发现", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"🔎 查询", callback_data="a/群频管理输入?text=请输入群|频道标题名:")])
        keyboard.append([InlineKeyboardButton(f"🏠 管理首页", callback_data="a/管理首页"),
                         InlineKeyboardButton(f"↩️ 返回", callback_data="a/管理首页")])
        await self.sendMsg(text=text, keyboard=keyboard)
    async def groupInfo(self,**kwargs):
        group_id = kwargs.get('group')[0]
        groupData =GroupData()
        group_info =await groupData.get_group_info(id=group_id)
        user = await groupData.get_user(id=group_info[12])
        fleet = await groupData.get_fleet_one(id=group_info[11])
        if group_info:
            group_type ='频道' if group_info[4]=='CHANNEL' else '群组'
            group_fleet_state = "⚪ 空闲" if group_info[10]==0 else "🟡 申请中" if group_info[10]==1 else "🟢 已上车" if group_info[10]==2 else "🚫 已禁用" if group_info[10]==10 else "未知状态"
            text = "✨✨✨✨✨✨✨✨✨✨✨✨\n" \
                   f"💡**{group_type}详情**💡\n\n" \
                   f"〖{group_type}ID〗{group_info[1]}\n" \
                   f"〖{group_type}用户名〗{'@'+group_info[2] if group_info[2] else '未设置'}\n" \
                   f"〖{group_type}标题〗{group_info[3]}\n" \
                   f"〖{group_type}订阅数〗{group_info[5]}\n" \
                   f"〖互推消息ID〗{group_info[7]}\n" \
                   f"〖进粉人数〗{group_info[9]}\n" \
                   f"〖{group_type}状态〗{group_fleet_state}\n" \
                   f"〖{group_type}车队〗{fleet[1]}\n\n" \
                   f"〖所属用户ID〗{user[1]}\n" \
                   f"〖所属用户名〗{user[3]}\n"
            keyboard = []
            if group_info[10] == 10:
                keyboard.append([InlineKeyboardButton("🟢 解群", callback_data=f"a/群频管理启禁群?group={group_info[0]}")])
            else:
                keyboard.append([InlineKeyboardButton("🚫 禁群", callback_data=f"a/群频管理启禁群?group={group_info[0]}")])
            keyboard.append([InlineKeyboardButton(f"🏠 管理首页", callback_data="a/管理首页"),
                             InlineKeyboardButton(f"↩️ 返回", callback_data=f"a/群频管理")])
            await self.sendMsg(text=text, keyboard=keyboard)
        else:
            await self.query.answer("err:群/频不存在或已被删除")
    async def banGroup(self,**kwargs):
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        if group[10]==10:
            await car.put_car_pass_review(group=group, state=0, label=f"🟢 频道已解除禁用")
        else:
            await car.put_car_pass_review(group=group, state=10, label=f"🚫 频道已被管理员禁用")
        await self.groupInfo(group=[kwargs.get('group')[0]])
        await self.reviewNotify(group=[kwargs.get('group')[0]])
    async def reviewNotify(self, **kwargs):
        '''组装消息通知用户'''
        car = CarData()
        group = await car.get_user_group_one(id=kwargs.get('group')[0])
        toUser = await car.get_user(id=group[12])
        notify = await car.get_notify_msg(user=toUser[0], group=group[0])
        text = "**📣系统通知**📣\n" \
               f"**频道ID:** {group[1]}\n" \
               f"**申请频道:** [{group[3]}]({group[6]})\n" \
               f"**订阅人数:** {group[5]}\n" \
               f"**申请人ID:** {toUser[1]}\n" \
               f"**申请人名:** [{toUser[3]}](https://t.me/{toUser[2] or ''})\n"
        text += f"**申请状态:** {notify[3] if notify else '未知'} "
        try:
            await self.client.send_message(chat_id=toUser[1], text=text, disable_web_page_preview=True)
        except RPCError as e:
            msg = await self.retChat()
            await msgNotify(msg=msg, text='❗通知用户失败', times=5)
        if len(bot_config["msgGroup"]) > 5:
            try:
                keyboards = [[InlineKeyboardButton("➕ 参加互推", url=f"https://t.me/{bot_config['botUserName']}")]]
                await self.client.send_message(chat_id=bot_config["msgGroup"], text=text,
                                               reply_markup=InlineKeyboardMarkup(keyboards),
                                               disable_web_page_preview=True)
            except RPCError as e:
                msg = await self.retChat()
                await msgNotify(msg=msg, text='❗通知消息群失败', times=5)
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
        txt = f"👨‍💻{kwargs.get('text')[0]}"
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
                                                     callback_data=f"a/用户详情?user={user[0]}")])
            content.append([InlineKeyboardButton(f"{'上一页' if upPage >= 0 else '-'}",
                                                 callback_data=f"a/用户管理?page={upPage}&type={userType}" if upPage >= 0 else '-'),
                            InlineKeyboardButton(f"{currentPage}/{totalPages}", callback_data="-"),
                            InlineKeyboardButton(f"{'下一页' if currentPage != totalPages else '-'}",
                                                 callback_data=f"a/用户管理?page={dowPage}&type={userType}" if currentPage != totalPages else '-')])
        else:
            content = [[InlineKeyboardButton(f"空/么有用户", callback_data="-")]]
        keyboard = [
            [InlineKeyboardButton(f"{'🟢' if userType == 0 else ''}普通用户", callback_data=f"a/用户管理?type=0"),
             InlineKeyboardButton(f"{'🟢' if userType == 1 else ''}管理员", callback_data=f"a/用户管理?type=1"),
             ],[InlineKeyboardButton(f"查询用户", callback_data="a/用户输入?text=请输入用户名或者昵称:")],
            [InlineKeyboardButton(f"↩️ 返回", callback_data="a/管理首页")]]
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n\n" \
               "======**🏆 用户查询 🏆**======\n" \
               f"〖用户数〗{userS[0][0]}人\n" \
               f"👮‍管理员:{userS[0][2]}\n" \
               f"👳用户:{userS[0][1]}\n"
        await self.sendMsg(text=text, keyboard=content+keyboard)
    async def userInfo(self, **kwargs):
        msg = await  self.retChat()
        userID = kwargs.get('user')[0]
        user = db.select(f"SELECT * FROM chat_user WHERE id = {userID}")
        print(user)
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n" \
               f"💡**用户资料**💡\n\n" \
               f"〖用户ID〗`{user[0][1] or '无'}`(点击复制)\n" \
               f"〖用户账号〗`{user[0][2] or '无'}`(点击复制)\n" \
               f"〖用户昵称〗`{user[0][3] or '无'}`(点击复制)\n" \
               f"〖用户状态〗{'🟢正常' if user[0][4] == 0 else '🔴禁用'}\n" \
               f"〖用户权限〗{'👮‍管理员' if user[0][5] == 1 else '👳‍用户'}\n"
        keyboard = []
        if user[0][5] == 0:
            keyboard.append([InlineKeyboardButton("🔐设置管理员", callback_data=f"a/设置管理员?user={user[0][0]}&p=0")])
        elif user[0][5] == 1:
            keyboard.append([InlineKeyboardButton("🔓取消管理员", callback_data=f"a/设置管理员?user={user[0][0]}&p=1")])
        if user[0][4]==0:
            keyboard.append([InlineKeyboardButton("🚷 禁用户", callback_data=f"a/禁用户?user={user[0][0]}")])
        else:
            keyboard.append([InlineKeyboardButton("✅ 解禁用户", callback_data=f"a/禁用户?user={user[0][0]}")])
        keyboard.append([InlineKeyboardButton("↩️ 返回", callback_data="a/用户管理")])
        await self.sendMsg(text=text, keyboard=keyboard)
    async def setAdmin(self, **kwargs):
        msg = await  self.retChat()
        if kwargs.get('user'):
            user = db.select(f"SELECT * FROM chat_user WHERE chat_id = {msg.chat.id}")
            if user and user[0][5] == 2:
                pa = 1 if kwargs.get('p')[0] == '0' else 0
                if db.update(f"UPDATE chat_user SET admin={pa} WHERE id={kwargs.get('user')[0]}"):
                    await self.client.answer_callback_query(self.query.id, text='设置管理员成功', show_alert=True)
                    await self.backReview()
                    await self.userInfo(chat=kwargs.get('user'))
                else:
                    await self.client.answer_callback_query(self.query.id, text='数据异常', show_alert=True)
            elif user[0][5] == 1:
                await self.client.answer_callback_query(self.query.id, text='设置失败:你没权限添加管理员',
                                                        show_alert=True)
            else:
                await self.client.answer_callback_query(self.query.id, text='设置管理员失败:用户不存在',
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
        # 删除当前消息或者媒体消息返回
        msg =await  self.retChat()
        await self.client.delete_messages(msg.chat.id, message_ids=msg.id)
    async def reviewNotify(self, **kwargs):
        '''组装消息通知用户'''
        car = CarData()
        toUser = await car.get_user(id=kwargs.get('user')[0])
        text = "✨✨✨✨✨✨✨✨✨✨✨✨\n" \
               f"💡**用户资料**💡\n\n" \
               f"〖用户ID〗`{toUser[1] or '无'}`(点击复制)\n" \
               f"〖用户账号〗`{toUser[2] or '无'}`(点击复制)\n" \
               f"〖用户昵称〗`{toUser[3] or '无'}`(点击复制)\n" \
               f"〖用户状态〗{'🟢正常' if toUser[4] == 0 else '🔴禁用'}\n"
        text += f"〖通知消息〗** {'🟢 您已被管理员解除禁用' if toUser[4]==0 else '🔴 您已被管理员禁用'} "
        try:
            await self.client.send_message(chat_id=toUser[1], text=text, disable_web_page_preview=True)
        except RPCError as e:
            msg = await self.retChat()
            await msgNotify(msg=msg, text='❗通知用户失败', times=5)
        if len(bot_config["msgGroup"]) > 5:
            try:
                keyboards = [[InlineKeyboardButton("➕ 参加互推", url=f"https://t.me/{bot_config['botUserName']}")]]
                await self.client.send_message(chat_id=bot_config["msgGroup"], text=text,
                                               reply_markup=InlineKeyboardMarkup(keyboards),
                                               disable_web_page_preview=True)
            except RPCError as e:
                msg = await self.retChat()
                await msgNotify(msg=msg, text='❗通知消息群失败', times=5)
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
        txt = f"🤖{kwargs.get('text')[0]}"
        await msg.reply_text(text=txt, reply_to_message_id=msg.id, reply_markup=ForceReply())
    async def index(self, **kwargs):
        '''黑名单'''
        list = await BotBlacklistDate().get_bot_blacklist_list()
        text = "======**🏆 机器人黑名单 🏆**======\n" \
               "申请时和发车时检测是否存在黑名单内机器人提示用户并下车\n" \
               "添加说明：输入 带@xxxbot 机器人账号\n" \
               "图示介绍：➕添加 ❌删除 🖍修改\n\n" \
               "🚫**机器人黑名单列表:**\n"
        keyboard = []
        if list:
            for index, advertising in enumerate(list):
                text += f"{index + 1}.[{advertising[1]}]({advertising[2]})\n"
                keyboard.append([InlineKeyboardButton(f"{index + 1}.{advertising[1]}", callback_data="-"),
                                 InlineKeyboardButton(f"❌ 删除", callback_data=f"a/删Bot黑名单?id={advertising[0]}"),
                                 InlineKeyboardButton(f"🖍 修改",
                                                      callback_data=f"a/Bot输入?text=请输入新的BOT用户名:{advertising[0]}")])
        else:
            text += "空,未设置"
            keyboard.append([InlineKeyboardButton(f"列表为空", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"➕添加", callback_data=f"a/Bot输入?text=请输入BOT用户名:例:@Xxbot")])
        keyboard.append([InlineKeyboardButton(f"🏠 管理首页", callback_data="a/管理首页"),
                         InlineKeyboardButton(f"↩️ 返回", callback_data="a/管理首页")])
        await self.sendMsg(text=text, keyboard=keyboard)
    async def delBotBlacklist(self, **kwargs):
        '''删审核拒绝词'''
        msg = await self.retChat()
        id = kwargs.get('id')[0]
        delData = await BotBlacklistDate().del_bot_blacklist(id=id)
        if delData:
            await self.query.answer(text="✅删除成功", cache_time=5)
            await self.index()
        else:
            await msgNotify(msg=msg, text="❕删除失败")


