import logging

from router import router
from views.client import *
from views.admin import *


async def start_handler(client: Client, message: Message):
    '''
    Обработчик команды запуска бота
    :param client: объект клиента
    :param message: сообщение пользователя
    :return: завершение обработки команды
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
                logging.error(f"Ошибка команды пользователя: {e}")


async def callback_query_router(client: Client, query: CallbackQuery):
    # Маршрутизация нажатий inline-кнопок обычных пользователей
    if await RestrictAccess(Msg=query.message).limit_check():
        user = await UserAuth(Msg=query.message).auth(FromUser=query.from_user)
        if user:
            try:
                print(query.data)
                logging.info(query.data)
                await router.route(query.data, client, query, Data={'user': user})
            except ValueError as E:
                logging.error(f'Ошибка пользовательского маршрута: {E}')
                await query.answer(text=f'Ошибка: {E}', show_alert=True)


async def admin_callback_query_router(client: Client, query: CallbackQuery):
    # Маршрутизация нажатий inline-кнопок администраторов
    user = await UserAuth(Msg=query.message).auth(FromUser=query.from_user)
    if user and user[5] in [1, 2] or query.message.chat.id == int(bot_config["adminGroup"]):
        try:
            print(query.data)
            logging.info(query.data)
            await router.route(query.data, client, query, Data={'user': user})
        except ValueError as E:
            print(E)
            logging.error(f'Ошибка: {E}')
            await query.answer(text=f'Ошибка: {E}', show_alert=True)
    else:
        await query.message.reply_text("⚠️ Недостаточно прав, требуется доступ администратора")


async def admii_command(client: Client, message: Message):
    # Вход в панель администратора
    user = await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        try:
            admin = Admin(Client=client, Msg=message, Data={'user': user})
            await admin.index()
        except (RPCError,Exception) as e:
            logging.error(f"Ошибка панели администратора: {e}")
    else:
        await message.reply_text("⚠️ Недостаточно прав, требуется доступ администратора")


# Отслеживание изменения статуса бота в группах и каналах
async def handle_chat_member_update(client: Client, update: ChatMemberUpdated):
    # print(update)
    if update.new_chat_member and update.new_chat_member.user.username == bot_config['botUserName'].replace('@', ''):
        user = db.select("SELECT * FROM chat_user WHERE chat_id=%s", (update.from_user.id,))
        print("Пользователь",user)
        if user:
            if  user[0][4]==0:
                    if update.new_chat_member.status.name == 'ADMINISTRATOR':
                        group = await app.get_chat(update.chat.id)
                        isPrivi = await isPrivileges(chatId=update.chat.id, typeG=group.type.name)
                        if isPrivi == 1:
                            text = f"《[{update.chat.title}]({group.invite_link})》 " \
                                   f"— у бота недостаточно прав, ресурс будет снят с подборки, проверьте права"
                            db.update("UPDATE group_list SET state=0 WHERE group_id=%s", (update.chat.id,))
                            return await client.send_message(chat_id=user[0][1], text=text)
                        groupIs = db.select("SELECT * FROM group_list WHERE group_id=%s", (update.chat.id,))
                        print(groupIs)
                        if not groupIs:
                            text = f"《[{update.chat.title}]({group.invite_link})》 успешно добавлен, проверка прав пройдена"
                            if db.insert(
                                    "INSERT INTO group_list (group_id,username,title,type,total_people,url,chat_id) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                                    (group.id, group.username or "", group.title, group.type.name, group.members_count,
                                     group.invite_link, user[0][0])):
                                return await client.send_message(chat_id=user[0][1], text=text)
                        else:
                            if groupIs[0][10] == 10:
                                text = f"《[{update.chat.title}](https://t.me/{update.chat.username})》" \
                                       f"Ваш ресурс заблокирован, обратитесь к администратору"
                                return await client.send_message(chat_id=user[0][1], text=text)
                            db.update(
                                "UPDATE group_list SET title=%s,total_people=%s,url=%s,chat_id=%s WHERE group_id=%s",
                                (group.title, group.members_count, group.invite_link, user[0][0], update.chat.id,))
                            text = f"《[{group.title}]({group.invite_link})》 уже существует, данные обновлены!"
                            return await  client.send_message(chat_id=user[0][1], text=text)
                    elif update.new_chat_member.status.name == 'MEMBER':
                        text = f"《[{update.chat.title}](https://t.me/{update.chat.username})》" \
                               f"— права администратора не обнаружены, ресурс будет снят с подборки, проверьте права!"
                        db.update("UPDATE group_list SET state=0,label='Права администратора не обнаружены' WHERE group_id=%s",
                                  (update.chat.id,))
                        return await client.send_message(chat_id=user[0][1], text=text)
            else:
                text = "Ваш аккаунт заблокирован, обратитесь к администратору"
                return await client.send_message(chat_id=update.from_user.id, text=text)
        else:
            print("Пользователь не найден",)
    elif update.old_chat_member  and update.old_chat_member.user.username == bot_config['botUserName'].replace('@', ''):
        print('Бот вышел из группы/канала')
        group = db.select("SELECT * FROM group_list WHERE group_id=%s", (update.chat.id,))
        print(group)
        if group:
            if group[0][10] == 10:
                text = f"《[{update.chat.title}](https://t.me/{update.chat.username})》" \
                       f"Ваш ресурс заблокирован, обратитесь к администратору"
                return await client.send_message(chat_id=update.old_chat_member.invited_by.id, text=text)
            else:
                db.update("UPDATE group_list SET state=0 WHERE group_id=%s",(update.chat.id,))
                text = f"《[{update.chat.title}](https://t.me/{update.chat.username})》" \
                           f"— бот вышел из группы/канала, ресурс снят с подборки!"
                return await client.send_message(chat_id=update.old_chat_member.invited_by.id, text=text)
        else:
            print("Группа ещё не добавлена в бота")

# # Обработчики удаления и редактирования сообщений
# async def delete_message(client,message):
#     print('Сообщение удалено',message)
#
# async def edited_message(client:Client,edited_message:Message):
#     print('Сообщение изменено',edited_message)
