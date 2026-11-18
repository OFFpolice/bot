from data.data import *
from public.method import *
from views.admin import *
# 配置修改
async def admin_config_reply_input(client:Client,message:Message):
    user =await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        config=ConfigData()
        admin = Admin(Client=client, Msg=message)
        msg_id=[message.id, message.reply_to_message_id,message.reply_to_message.reply_to_message_id]
        if '请输入机器人名' in reply_text[0]:
            if await config.put_config(comm=message.text,name='botName'):
                await msgNotify(msg=message, text='修改机器人名成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message, text='修改机器人名失败')
            await client.delete_messages(message.chat.id, message_ids=msg_id)
            await admin.config()
        elif "请输入机器人账号" in reply_text[0]:
            if await config.put_config(comm=message.text,name='botUserName'):
                await msgNotify(msg=message,text='修改机器人账号成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改机器人账号失败')
            await admin.config()
        elif "请输入首页欢迎词" in reply_text[0]:
            if await config.put_config(comm=message.text,name='indexTxt'):
                await msgNotify(msg=message,text='修改首页欢迎词成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改首页欢迎词失败')
            await admin.config()
        elif "请输入管理群组" in reply_text[0]:
            if await config.put_config(comm=message.text,name='adminGroup'):
                await msgNotify(msg=message,text='修改管理群组成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改管理群组失败')
            await admin.config()
        elif "请输入消息群组" in reply_text[0]:
            if await config.put_config(comm=message.text,name='msgGroup'):
                await msgNotify(msg=message,text='修改消息群组成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改消息群组失败')
            await admin.config()
        elif "请输入访问限制" in reply_text[0]:
            if await config.put_config(comm=message.text,name='restrict_limit'):
                await msgNotify(msg=message,text='修改访问限制成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改访问限制失败')
            await admin.config()
        elif "请上传视频介绍" in reply_text[0]:
            if message.video:
                if await config.put_config(comm=message.video.file_id, name='video'):
                    await msgNotify(msg=message, text="请上传视频成功")
                    await client.delete_messages(message.chat.id, message_ids=[message.reply_to_message.reply_to_message_id])
                await admin.config()
            else:
                await msgNotify(msg=message,text="请上传视频")
        elif "请输入审核拒绝词" in reply_text[0]:
            if await config.post_rejectText(text=message.text):
                await msgNotify(msg=message,text='新增审核拒绝词成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='新增审核拒绝词失败')
            await admin.reviewRejectionWords()
        elif "请输入新的审核拒绝词" in reply_text[0]:
            if await config.put_rejectText(id=reply_text[1],text=message.text):
                await msgNotify(msg=message,text='修改审核拒绝词成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改审核拒绝词失败')
            await admin.reviewRejectionWords()
        elif "请输入消息群组" in reply_text[0]:
            if await config.put_config(comm=message.text,name='msgGroup'):
                await msgNotify(msg=message,text='修改消息群组成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改消息群组失败')
            await admin.config()
        elif "请输入交流群组" in reply_text[0]:
            if await config.put_config(comm=message.text,name='publicGroup'):
                await msgNotify(msg=message,text='修改交流群组成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改交流群组失败')
            await admin.config()
    else:
        await message.reply_text("⚠️权限不足,需要管理员权限")

async def admin_advertising_input(client:Client,message:Message):
    user = await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        adData=AdvertisingData()
        advertising = Advertising(Client=client, Msg=message)
        msg_id = [message.id, message.reply_to_message_id, message.reply_to_message.reply_to_message_id]
        if "请输入广告" in reply_text[0]:
            text = message.text.split('&')
            if len(text) > 1:
                if await adData.post_advertising(titel=text[0], url=text[1]):
                    await msgNotify(msg=message, text='新增广告成功')
                    await client.delete_messages(message.chat.id, message_ids=msg_id)
                else:
                    await msgNotify(msg=message, text='新增广告失败')
                await advertising.index()
            else:
                await msgNotify(msg=message, text='格式错误：正确格式为 标题&网址')
        elif "请输入新的广告" in reply_text[0]:
            text = message.text.split('&')
            if len(text) > 1:
                if await adData.put_advertising(id=reply_text[1],titel=text[0],url=text[1]):
                    await msgNotify(msg=message,text='修改广告成功')
                    await client.delete_messages(message.chat.id, message_ids=msg_id)
                else:
                    await msgNotify(msg=message,text='修改广告失败')
                await advertising.index()
            else:
                await msgNotify(msg=message, text='格式错误：正确格式为 标题&网址')
    else:
        await message.reply_text("⚠️权限不足,需要管理员权限")

async def admin_car_input(client:Client,message:Message):
    user =await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        carData=CarData()
        car = Car(Client=client, Msg=message)
        msg_id=[message.id, message.reply_to_message_id,message.reply_to_message.reply_to_message_id]
        if "请输入频道车队标题" in reply_text[0]:
            if await carData.post_car(car_title=message.text,car_type=0):
                await msgNotify(msg=message,text='添加频道车队成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='添加频道车队失败')
            await car.channel_car()
        elif "请输入频道车队新标题" in reply_text[0]:
            if await carData.put_car_titel(text=message.text,id=reply_text[1]):
                await msgNotify(msg=message,text='修改车队标题成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改车队标题失败')
            await car.channel_fleet_info(fleet=[reply_text[1]])
        elif "请输入频道车队新介绍" in reply_text[0]:
            if await carData.put_car_introduce(text=message.text,id=reply_text[1]):
                await msgNotify(msg=message,text='修改车队介绍成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改车队介绍失败')
            await car.channel_fleet_info(fleet=[reply_text[1]])
        elif "请输入频道车队新最大成员数" in reply_text[0]:
            if await carData.put_car_total(text=message.text,id=reply_text[1]):
                await msgNotify(msg=message,text='修改车队最大成员数成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改车队最大成员数失败')
            await car.channel_fleet_info(fleet=[reply_text[1]])
        elif "请输入频道车队新最低订阅" in reply_text[0]:
            if await carData.put_car_mi_memberl(text=message.text,id=reply_text[1]):
                await msgNotify(msg=message,text='修改车队最低订阅成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改车队最小订阅失败')
            await car.channel_fleet_info(fleet=[reply_text[1]])
        elif "请输入频道车队新最低阅读" in reply_text[0]:
            if await carData.put_car_mi_mi_read(text=message.text,id=reply_text[1]):
                await msgNotify(msg=message,text='修改车队最低阅读成功')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='修改车队最低阅读失败')
            await car.channel_fleet_info(fleet=[reply_text[1]])
    else:
        await message.reply_text("⚠️权限不足,需要管理员权限")

async def admin_car_group_input(client:Client,message:Message):
    if message.chat.id==int(bot_config["adminGroup"]):
        reply_text = message.reply_to_message.text.split(':')
        carData=CarData()
        review = Review(Client=client, Msg=message)
        msg_id=[message.id, message.reply_to_message_id,message.reply_to_message.reply_to_message_id]
        if "请输入自定义拒绝原因" in reply_text[0]:
            await client.delete_messages(message.chat.id, message_ids=[message.id, message.reply_to_message_id])
            await review.rejectReason(group=[reply_text[1]], reason=[message.text])
    else:
        await message.reply_text("⚠️权限不足,需要管理群权限")

async def admin_group_input(client:Client,message:Message):
    user =await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        group = Group(Client=client, Msg=message)
        msg_id=[message.id, message.reply_to_message_id,message.reply_to_message.reply_to_message_id]
        if "请输入群|频道标题名" in reply_text[0]:
            await client.delete_messages(message.chat.id, message_ids=msg_id)
            await group.index(search=message.text)
    else:
        await message.reply_text("⚠️权限不足,需要管理员权限")

async def admin_user_input(client:Client,message:Message):
    user =await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        user = User(Client=client, Msg=message)
        msg_id=[message.id, message.reply_to_message_id,message.reply_to_message.reply_to_message_id]
        if "请输入用户名或者昵称" in reply_text[0]:
            await client.delete_messages(message.chat.id, message_ids=msg_id)
            await user.getUser(search=message.text)
    else:
        await message.reply_text("⚠️权限不足,需要管理员权限")

async def admin_bot_blacklist_input(client:Client,message:Message):
    user = await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        blacklist_date=BotBlacklistDate()
        blacklist = BotBlacklist(Client=client, Msg=message)
        msg_id = [message.id, message.reply_to_message_id, message.reply_to_message.reply_to_message_id]
        if "请输入BOT用户名" in reply_text[0]:
            if "@" in message.text :
                if await blacklist_date.post_bot_blacklist(titel=message.text):
                    await msgNotify(msg=message, text='新增机器人黑名单成功')
                else:
                    await msgNotify(msg=message, text='新增机器人黑名单失败')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
                await blacklist.index()
            else:
                await msgNotify(msg=message, text='格式错误：正确格式为 @机器人名')
        elif "请输入新的BOT用户名" in reply_text[0]:
            if "@" in message.text :
                if await blacklist_date.put_bot_blacklist(id=reply_text[1],titel=message.text):
                    await msgNotify(msg=message,text='修改广告成功')
                    await client.delete_messages(message.chat.id, message_ids=msg_id)
                else:
                    await msgNotify(msg=message,text='修改广告失败')
                await blacklist.index()
            else:
                await msgNotify(msg=message, text='格式错误：正确格式为 @机器人名')
    else:
        await message.reply_text("⚠️权限不足,需要管理员权限")