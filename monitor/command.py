import logging

from router import router
from views.client import *
from views.admin import *


async def start_handler(client: Client, message: Message):
    '''
    用户开始命令监听函数
    :param client:客户端对象
    :param message:小题体
    :return:执行完结束一轮访问
    '''
    if await RestrictAccess(Msg=message).limit_check():
        user = await UserAuth(Msg=message).auth(FromUser=message.from_user)
        if user:
            try:
                index = Index(Client=client, Msg=message, Data={'user': user})
                if message.command[0] == "start":
                    await index.welcome()
                await index.index()
            except (RPCError,Exception) as e:
                logging.error(f"用户命令错误：{e}")


async def callback_query_router(client: Client, query: CallbackQuery):
    # 按钮点击进来进行路由
    if await RestrictAccess(Msg=query.message).limit_check():
        user = await UserAuth(Msg=query.message).auth(FromUser=query.from_user)
        if user:
            try:
                print(query.data)
                logging.info(query.data)
                await router.route(query.data, client, query, Data={'user': user})
            except ValueError as E:
                logging.error(f'普通路由错误:{E}')
                await query.answer(text=f'错误:{E}', show_alert=True)


async def admin_callback_query_router(client: Client, query: CallbackQuery):
    # 按钮点击进来进行路由
    user = await UserAuth(Msg=query.message).auth(FromUser=query.from_user)
    if user and user[5] in [1, 2] or query.message.chat.id == int(bot_config["adminGroup"]):
        try:
            print(query.data)
            logging.info(query.data)
            await router.route(query.data, client, query, Data={'user': user})
        except ValueError as E:
            print(E)
            logging.error(f'错误:{E}')
            await query.answer(text=f'错误:{E}', show_alert=True)
    else:
        await query.message.reply_text("⚠️权限不足,需要管理员权限")


async def admii_command(client: Client, message: Message):
    # 管理页面入口
    user = await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        try:
            admin = Admin(Client=client, Msg=message, Data={'user': user})
            await admin.index()
        except (RPCError,Exception) as e:
            logging.error(f"后台管理错误:{e}")
    else:
        await message.reply_text("⚠️权限不足,需要管理员权限")


# 用户状态监控
async def handle_chat_member_update(client: Client, update: ChatMemberUpdated):
    # print(update)
    if update.new_chat_member and update.new_chat_member.user.username == bot_config['botUserName'].replace('@', ''):
        user = db.select("SELECT * FROM chat_user WHERE chat_id=%s", (update.from_user.id,))
        print("用户",user)
        if user:
            if  user[0][4]==0:
                    if update.new_chat_member.status.name == 'ADMINISTRATOR':
                        group = await app.get_chat(update.chat.id)
                        isPrivi = await isPrivileges(chatId=update.chat.id, typeG=group.type.name)
                        if isPrivi == 1:
                            text = f"《[{update.chat.title}]({group.invite_link})》 " \
                                   f"中机器人权限不足,此群即将下车请检查"
                            db.update("UPDATE group_list SET state=0 WHERE group_id=%s", (update.chat.id,))
                            return await client.send_message(chat_id=user[0][1], text=text)
                        groupIs = db.select("SELECT * FROM group_list WHERE group_id=%s", (update.chat.id,))
                        print(groupIs)
                        if not groupIs:
                            text = f"添加《[{update.chat.title}]({group.invite_link})》成功,权限检测正常"
                            if db.insert(
                                    "INSERT INTO group_list (group_id,username,title,type,total_people,url,chat_id) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                                    (group.id, group.username or "", group.title, group.type.name, group.members_count,
                                     group.invite_link, user[0][0])):
                                return await client.send_message(chat_id=user[0][1], text=text)
                        else:
                            if groupIs[0][10] == 10:
                                text = f"《[{update.chat.title}](https://t.me/{update.chat.username})》" \
                                       f"您的群已被禁用请联系管理员"
                                return await client.send_message(chat_id=user[0][1], text=text)
                            db.update(
                                "UPDATE group_list SET title=%s,total_people=%s,url=%s,chat_id=%s WHERE group_id=%s",
                                (group.title, group.members_count, group.invite_link, user[0][0], update.chat.id,))
                            text = f"《[{group.title}]({group.invite_link})》已存在,数据已更新！！"
                            return await  client.send_message(chat_id=user[0][1], text=text)
                    elif update.new_chat_member.status.name == 'MEMBER':
                        text = f"《[{update.chat.title}](https://t.me/{update.chat.username})》" \
                               f"中未检测到管理员权限,此群即将下车请检查！！"
                        db.update("UPDATE group_list SET state=0,label='未检测到管理员权限' WHERE group_id=%s",
                                  (update.chat.id,))
                        return await client.send_message(chat_id=user[0][1], text=text)
            else:
                text = "您的账号已被禁用请联系管理员"
                return await client.send_message(chat_id=update.from_user.id, text=text)
        else:
            print("用户不存在",)
    elif update.old_chat_member  and update.old_chat_member.user.username == bot_config['botUserName'].replace('@', ''):
        print('退出了群组')
        group = db.select("SELECT * FROM group_list WHERE group_id=%s", (update.chat.id,))
        print(group)
        if group:
            if group[0][10] == 10:
                text = f"《[{update.chat.title}](https://t.me/{update.chat.username})》" \
                       f"您的群已被禁用请联系管理员"
                return await client.send_message(chat_id=update.old_chat_member.invited_by.id, text=text)
            else:
                db.update("UPDATE group_list SET state=0 WHERE group_id=%s",(update.chat.id,))
                text = f"《[{update.chat.title}](https://t.me/{update.chat.username})》" \
                           f"退出了群组,此群即将下车请检查！！"
                return await client.send_message(chat_id=update.old_chat_member.invited_by.id, text=text)
        else:
            print("群还没加入机器人")

# # 消息删除处理程序
# async def delete_message(client,message):
#     print('删除了消息',message)
#
# async def edited_message(client:Client,edited_message:Message):
#     print('修改了消息',edited_message)
