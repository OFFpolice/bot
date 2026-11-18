from config import *
from public.method import *
from data.data import *
class Index:
    def __init__(self, Client:Client, Query:CallbackQuery=None, Msg:Message=None, Data=None):
        self.client =Client
        self.query = Query
        self.msg = Msg
        self.data= Data
    async def retChat(self):
        if self.query:
            return self.query.message
        else:
            return self.msg
    async def sendMsg(self,**kwargs):
        msg = await self.retChat()
        try:
            if self.query:
                await self.client.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=kwargs['text'],
                                                    reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                                    disable_web_page_preview=True)
            else:
                if len(bot_config.get('video'))>24:
                    await self.client.send_video(chat_id=msg.chat.id, video=bot_config.get('video'), caption=kwargs['text'],
                                                 reply_markup=InlineKeyboardMarkup(kwargs['keyboard']))
                else:
                    await msg.reply_text(text=kwargs['text'], reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                         disable_web_page_preview=True)
        except RPCError as e:
            print(e)
    async def welcome(self,**kwargs):
        msg = await self.retChat()
        user=self.data.get('user')
        Reply = [['帮助']]
        if user[5] in [1, 2]:
            Reply = [['⚙管理页面']]
        text = f"**欢迎使用:{bot_config.get('botName')}**\n\n" \
               f"{bot_config.get('indexTxt')}\n\n"
        await msg.reply_text(text, reply_markup=ReplyKeyboardMarkup(Reply, resize_keyboard=True),
                                 disable_web_page_preview=True)
    async def index(self,**kwargs):
        msg =await self.retChat()
        user=self.data.get('user')
        try:
            if user:
                text = f"======🏆 车队首页 🏆======\n\n" \
                       f"**🚀Telegram互推:**  @{bot_config.get('botUserName')}\n\n" \
                       f"**UID {user[1]}** 尊敬的 {user[3]} 你好:\n\n" \
                       f"**🔗纯中文互粉互推自助发布机器人🔗**\n\n" \
                       f"**使用说明：**请将本机器人拉入你的[群组](https://t.me/{bot_config.get('botUserName').replace('@', '')}?startgroup=true)|[频道](https://t.me/{bot_config.get('botUserName').replace('@', '')}?startchannel=true)，并赋予管理员权限🔶\n" \
                       f"**管理权限：**发布消息/编辑其他人的消息/删除其他人的消息/邀请其他人权限，缺失权限机器人不能正常工作\n\n" \
                       f"⚠️严谨发布幼童/人兽/男同/血腥/暴力/重口/政治/军火等活动的参与【[详见公告](https://t.me/hufen/3)】\n"
                keyboard=[
                    [InlineKeyboardButton("📍邀请机器人进群组",url=f"https://t.me/{bot_config['botUserName'].replace('@', '')}?startgroup=true"),
                     InlineKeyboardButton("📍邀请机器人进频道",url=f"https://t.me/{bot_config['botUserName'].replace('@', '')}?startchannel=true")],
                    [InlineKeyboardButton("⏺频道互推",callback_data="r/频道"),InlineKeyboardButton("⏺群组互推",callback_data="r/车队列表")],
                    [InlineKeyboardButton("❔车队教程", url=f"https://t.me/{bot_config['publicGroup']}"),InlineKeyboardButton("📢互推交流群",url="https://t.me/hutui")],
                ]
                await self.sendMsg(text=text,keyboard=keyboard)
        except (RPCError,Exception) as E:
            print(E)
            await msg.reply_text(text=f'错误:请截图联系客服{E}')

class Channel:
    def __init__(self, Client:Client, Query:CallbackQuery=None, Msg:Message=None, Data=None):
        self.client =Client
        self.query = Query
        self.msg = Msg
        self.data= Data
    async def retChat(self):
        if self.query:
            return self.query.message
        else:
            return self.msg
    async def sendMsg(self,**kwargs):
        msg = await self.retChat()
        try:
            if self.query:
                await self.client.edit_message_text(chat_id=msg.chat.id, message_id=msg.id, text=kwargs['text'],
                                                    reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                                    disable_web_page_preview=True)
            else:
                if len(bot_config.get('video'))>24:
                    await self.client.send_video(chat_id=msg.chat.id, video=bot_config.get('video'), caption=kwargs['text'],
                                                 reply_markup=InlineKeyboardMarkup(kwargs['keyboard']))
                else:
                    await msg.reply_text(text=kwargs['text'], reply_markup=InlineKeyboardMarkup(kwargs['keyboard']),
                                         disable_web_page_preview=True)
        except RPCError as e:
            print(e)
    async def index(self,**kwargs):
        OFFSET, LIMIT = int(kwargs.get('page')[0]) if kwargs.get('page') else 0, 30
        fleet = ChannelFleetList()
        fleetList,count = fleet.get_fleet(OFFSET=OFFSET,LIMIT=LIMIT)
        group_count= fleet.get_group_count()
        keyboard = []
        text = f"频道-车队大厅\n\n" \
               f"车队数量:{len(fleetList)}\n" \
               f"频道数量:{group_count}\n" \
               f"图标介绍:\n" \
               f"🚒发车/🕛等待 车队名|队内成员数-最大成员数|最小订阅需求\n\n" \
               f"选择下方车队进入指定车队，然后选择你要申请的分组进行上车提交。" \

        if fleetList:
            totalPages, currentPage = math.ceil(count / LIMIT), math.ceil(OFFSET / LIMIT) + 1
            upPage, dowPage = OFFSET - LIMIT, OFFSET + LIMIT
            row,step = [],2
            for i in range(0, len(fleetList), step):
                batch = fleetList[i:i + step]
                for Cont in batch:
                    row.append(InlineKeyboardButton(f"{'🚒' if Cont[4] == 1 else '🕛'} {Cont[1]}|{Cont[11]}/{Cont[6]}|{Cont[8]/1000}K",callback_data=f"r/频道车厢?fleet={Cont[0]}"))
                keyboard.append(row)
                row = []
            keyboard.append([InlineKeyboardButton(f"{'⬅️上一页' if upPage >= 0 else '-'}",callback_data=f"r/频道?page={upPage}" if upPage >= 0 else '-'),
                            InlineKeyboardButton(f"{currentPage}/{totalPages}页", callback_data="-"),
                            InlineKeyboardButton(f"️{'➡️下一页' if currentPage != totalPages else '-'}",callback_data=f"r/频道?page={dowPage}" if currentPage != totalPages else '-')])
        else:
            keyboard.append([InlineKeyboardButton(f"空/未发现车队", callback_data="-")])
        keyboard.append([InlineKeyboardButton(f"返回", callback_data="r/首页")])
        await self.sendMsg(text=text,keyboard=keyboard)
    async def fleet_info(self,**kwargs):
        fleet_id = kwargs.get("fleet")[0]
        fleet=ChannelFleetList()
        fleetInfo,group_list= fleet.get_fleet_one(id=fleet_id),fleet.get_fleet_group_list(id=fleet_id)
        if fleetInfo:
            text = f"**车队标题：** {fleetInfo[1]}\n" \
                      f"**车队介绍：** {fleetInfo[2]}\n" \
                      f"**当前/最大(成员)：** {fleetInfo[11]}/{fleetInfo[6]}\n" \
                      f"**车队类型：** 频道\n" \
                      f"**最低订阅：** {fleetInfo[8] / 10000} W人\n" \
                      f"**最低阅读：**{fleetInfo[9]}\n\n" \
                      "**成员列表：**\n"
            if group_list:
                for index,group in enumerate(group_list):
                    text+=f"{index+1}.[{await truncate_string(group[3],20)}]({group[6]}) {round(group[5]/1000,1)}k\n"
            else:
                text+="当前没有互推成员\n"
            keyboard=[]
            if fleetInfo[6]>fleetInfo[11]:
                text+="\n✅车队还未满员,你可以申请!"
                keyboard.append([InlineKeyboardButton(f"➕ 申请加入",callback_data=f"r/频道申请?fleet={fleetInfo[0]}&mi_me={fleetInfo[8]}")])
            else:
                text+="\n‼️车队已满,请申请其他车队!"
            # keyboard.append([InlineKeyboardButton(f"🚨 举报", callback_data="r/频道举报")])
            keyboard.append([InlineKeyboardButton(f"首页", callback_data="r/首页"),InlineKeyboardButton(f"返回", callback_data="r/频道")])
            await self.sendMsg(text=text,keyboard=keyboard)
    async def add_fleet(self,**kwargs):
        msg =await self.retChat()
        fleet,member= kwargs.get('fleet')[0],kwargs.get('mi_me')[0]
        user = self.data.get('user')
        if user:
            CF=ChannelFleetList(Msg=msg)
            my_group =await CF.get_user_group_list(id=user[0],member=member)
            if my_group:
                text = "**选择频道**\n\n" \
                       "以下只显示您满足要求的频道列表\n\n" \
                       f"要求订阅:{round(int(member)/1000,1)}k\n" \
                       "图示：🟢空闲🟡待审核🟣已上车🔴被禁用\n" \
                       "已上车的频道再次申请会自动下车\n" \
                       "请确认是否已经将机器人拉入并设置管理员\n\n" \
                       "👇请选择一个提交"
                keyboard = []
                for group in my_group:
                    ty_emoji= "🟢"
                    if group[10] == 1:
                        ty_emoji = "🟡"
                    elif group[10]==2:
                        ty_emoji= "🟣"
                    elif group[10]==10:
                        ty_emoji="🔴"
                    keyboard.append([InlineKeyboardButton(f"{ty_emoji} {group[3]}|{round(group[5]/1000,1)}k",callback_data=f"r/频道申请提交?f={fleet}&g={group[0]}")])
                keyboard.append([InlineKeyboardButton("🏠 首页", callback_data="r/首页"),
                                 InlineKeyboardButton("↩️ 返回", callback_data=f"r/频道车厢?fleet={fleet}")])
                await self.sendMsg(text=text,keyboard=keyboard)
            else:
                return await self.client.answer_callback_query(self.query.id, text="⚠️未找到满足当前车队要求的频道，请按照相应订阅人数选择分组",show_alert=True)
    async def submit_fleet(self,**kwargs):
        msg = await self.retChat()
        fleet = ChannelFleetList()
        fleet_id,group_id=kwargs.get('f')[0],kwargs.get('g')[0]
        fleetInfo, group = fleet.get_fleet_one(id=fleet_id),await fleet.get_user_group_one(id=group_id)
        if group:
            if group[10] in [0,1,2]:
                # print(group[1])
                isPrivi = await isPrivileges(chatId=group[1],typeG=group[4])
                if isPrivi == 1:
                    return await self.client.answer_callback_query(self.query.id, text="⚠️该群没给机器人权限请检查",show_alert=True)
                elif isPrivi == 2:
                    return await self.client.answer_callback_query(self.query.id, text="⛔机器人还未加入该群组或频道",show_alert=True)
                is_botList = await isBotBlacklist(Client=self.client,group=group[1])
                if len(is_botList)>0:
                    text = f"**⚠️ 您的频道内 [{group[3]}]({group[6]}) 包含以下黑名单内的机器人**\n\n"
                    for is_bot in is_botList:
                        text += f"{is_bot[0]}-@`{is_bot[1]}`复制\n"
                    text +="\n请删除以上机器人后重新提交"
                    keyboard = [[InlineKeyboardButton("❌ 删除消息", callback_data=f"a/删除当前消息")]]
                    return await msg.reply_text(text=text,reply_markup=InlineKeyboardMarkup(keyboard))
                await self.client.answer_callback_query(self.query.id, text='🎯提交成功,等待管理员审核', show_alert=True)
                await fleet.put_group_one(id=group_id,fieet=fleet_id)
                await self.sendNotify(fleet=fleetInfo,group=group)
                await self.add_fleet(fleet=[fleetInfo[0]], mi_me=[fleetInfo[8]])
            elif group[10] ==10:
                await self.client.answer_callback_query(self.query.id, text='⚠️多次违规已被禁用,请联系客服',show_alert=True)
            else:
                await self.client.answer_callback_query(self.query.id, text='⚠️请勿重复提交,耐心等待管理审核',show_alert=True)
        else:
            await self.client.answer_callback_query(self.query.id,text="⛔错误:未找到该群/频道信息",show_alert=True)
    async def sendNotify(self,**kwargs):
        fleet,group,user=kwargs["fleet"],kwargs["group"],self.data.get("user")
        text = "**🔆收到新的入队申请**\n" \
               f"**申请车队名:** {fleet[1]}\n" \
               f"**车队类型:** 频道\n" \
               f"**车队介绍:** {fleet[2]}\n" \
               f"**当前/最大(成员):** {fleet[11]}/{fleet[6]}\n" \
               f"**最低订阅:** {fleet[8] / 10000} W人\n" \
               f"**最低阅读:** {fleet[9]}\n\n" \
               f"**频道ID:** {group[1]}\n" \
               f"**申请频道:** [{group[3]}]({group[6]})\n" \
               f"**订阅人数:** {group[5]}\n" \
               f"**申请人ID:** {user[1]}\n" \
               f"**申请人名:** [{user[3]}](https://t.me/{user[2] or ''})\n" \
               "**申请状态:**🔵 待审核"
        keyboard = [[InlineKeyboardButton("🟢 通过审核", callback_data=f"a/通过审核?group={group[0]}"),
                     InlineKeyboardButton("❌ 拒绝审核", callback_data=f"a/拒绝审核?group={group[0]}")],
                    [InlineKeyboardButton("🚫 禁群", callback_data=f"a/禁群?group={group[0]}")],
                    ]
        await CarData().post_notify_msg(group=group,label="待审核")
        if int(bot_config["notifyType"])==0:
            await self.client.send_message(chat_id=bot_config['adminGroup'], text=text,
                                           reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)
        elif int(bot_config["notifyType"])==1:
            Channel = ChannelFleetList()
            adminList =await Channel.get_admini_list()
            for admin in adminList:
                try:
                    await self.client.send_message(chat_id=admin[1], text=text,
                                                   reply_markup=InlineKeyboardMarkup(keyboard),
                                                   disable_web_page_preview=True)
                except RPCError as e:
                    print(e)

