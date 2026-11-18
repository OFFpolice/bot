from data.data import *
from public.method import *
from views.admin import *
# Изменение конфигурации бота
async def admin_config_reply_input(client:Client,message:Message):
    user =await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        config=ConfigData()
        admin = Admin(Client=client, Msg=message)
        msg_id=[message.id, message.reply_to_message_id,message.reply_to_message.reply_to_message_id]
        if 'Введите имя бота' in reply_text[0]:
            if await config.put_config(comm=message.text,name='botName'):
                await msgNotify(msg=message, text='Имя бота успешно изменено')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message, text='Не удалось изменить имя бота')
            await client.delete_messages(message.chat.id, message_ids=msg_id)
            await admin.config()
        elif "Введите юзернейм бота" in reply_text[0]:
            if await config.put_config(comm=message.text,name='botUserName'):
                await msgNotify(msg=message,text='Юзернейм бота успешно изменён')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить юзернейм бота')
            await admin.config()
        elif "Введите текст приветствия" in reply_text[0]:
            if await config.put_config(comm=message.text,name='indexTxt'):
                await msgNotify(msg=message,text='Текст приветствия успешно изменён')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить текст приветствия')
            await admin.config()
        elif "Введите ID группы админов" in reply_text[0]:
            if await config.put_config(comm=message.text,name='adminGroup'):
                await msgNotify(msg=message,text='Группа админов успешно изменена')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить группу админов')
            await admin.config()
        elif "Введите ID группы уведомлений" in reply_text[0]:
            if await config.put_config(comm=message.text,name='msgGroup'):
                await msgNotify(msg=message,text='Группа уведомлений успешно изменена')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить группу уведомлений')
            await admin.config()
        elif "Введите лимит запросов" in reply_text[0]:
            if await config.put_config(comm=message.text,name='restrict_limit'):
                await msgNotify(msg=message,text='Лимит запросов успешно изменён')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить лимит запросов')
            await admin.config()
        elif "Отправьте видео-презентацию" in reply_text[0]:
            if message.video:
                if await config.put_config(comm=message.video.file_id, name='video'):
                    await msgNotify(msg=message, text="Видео-презентация успешно загружена")
                    await client.delete_messages(message.chat.id, message_ids=[message.reply_to_message.reply_to_message_id])
                await admin.config()
            else:
                await msgNotify(msg=message,text="Пожалуйста, отправьте видео")
        elif "Введите причину отказа" in reply_text[0]:
            if await config.post_rejectText(text=message.text):
                await msgNotify(msg=message,text='Причина отказа успешно добавлена')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось добавить причину отказа')
            await admin.reviewRejectionWords()
        elif "Введите новую причину отказа" in reply_text[0]:
            if await config.put_rejectText(id=reply_text[1],text=message.text):
                await msgNotify(msg=message,text='Причина отказа успешно изменена')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить причину отказа')
            await admin.reviewRejectionWords()
        elif "Введите чат общения" in reply_text[0]:
            if await config.put_config(comm=message.text,name='publicGroup'):
                await msgNotify(msg=message,text='Чат общения успешно изменён')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить чат общения')
            await admin.config()
    else:
        await message.reply_text("⚠️ Недостаточно прав, требуется доступ администратора")

async def admin_advertising_input(client:Client,message:Message):
    user = await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        adData=AdvertisingData()
        advertising = Advertising(Client=client, Msg=message)
        msg_id = [message.id, message.reply_to_message_id, message.reply_to_message.reply_to_message_id]
        if "Введите рекламу" in reply_text[0]:
            text = message.text.split('&')
            if len(text) > 1:
                if await adData.post_advertising(titel=text[0], url=text[1]):
                    await msgNotify(msg=message, text='Реклама успешно добавлена')
                    await client.delete_messages(message.chat.id, message_ids=msg_id)
                else:
                    await msgNotify(msg=message, text='Не удалось добавить рекламу')
                await advertising.index()
            else:
                await msgNotify(msg=message, text='Неверный формат: используйте Название&Ссылка')
        elif "Введите новую рекламу" in reply_text[0]:
            text = message.text.split('&')
            if len(text) > 1:
                if await adData.put_advertising(id=reply_text[1],titel=text[0],url=text[1]):
                    await msgNotify(msg=message,text='Реклама успешно изменена')
                    await client.delete_messages(message.chat.id, message_ids=msg_id)
                else:
                    await msgNotify(msg=message,text='Не удалось изменить рекламу')
                await advertising.index()
            else:
                await msgNotify(msg=message, text='Неверный формат: используйте Название&Ссылка')
    else:
        await message.reply_text("⚠️ Недостаточно прав, требуется доступ администратора")

async def admin_car_input(client:Client,message:Message):
    user =await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        carData=CarData()
        car = Car(Client=client, Msg=message)
        msg_id=[message.id, message.reply_to_message_id,message.reply_to_message.reply_to_message_id]
        if "Введите название подборки каналов" in reply_text[0]:
            if await carData.post_car(car_title=message.text,car_type=0):
                await msgNotify(msg=message,text='Подборка каналов успешно добавлена')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось добавить подборку каналов')
            await car.channel_car()
        elif "Введите новое название подборки" in reply_text[0]:
            if await carData.put_car_titel(text=message.text,id=reply_text[1]):
                await msgNotify(msg=message,text='Название подборки успешно изменено')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить название подборки')
            await car.channel_fleet_info(fleet=[reply_text[1]])
        elif "Введите новое описание подборки" in reply_text[0]:
            if await carData.put_car_introduce(text=message.text,id=reply_text[1]):
                await msgNotify(msg=message,text='Описание подборки успешно изменено')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить описание подборки')
            await car.channel_fleet_info(fleet=[reply_text[1]])
        elif "Введите макс. участников подборки" in reply_text[0]:
            if await carData.put_car_total(text=message.text,id=reply_text[1]):
                await msgNotify(msg=message,text='Максимум участников подборки изменён')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить максимум участников')
            await car.channel_fleet_info(fleet=[reply_text[1]])
        elif "Введите мин. подписчиков подборки" in reply_text[0]:
            if await carData.put_car_mi_memberl(text=message.text,id=reply_text[1]):
                await msgNotify(msg=message,text='Минимум подписчиков подборки изменён')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить минимум подписчиков')
            await car.channel_fleet_info(fleet=[reply_text[1]])
        elif "Введите мин. просмотров подборки" in reply_text[0]:
            if await carData.put_car_mi_mi_read(text=message.text,id=reply_text[1]):
                await msgNotify(msg=message,text='Минимум просмотров подборки изменён')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
            else:
                await msgNotify(msg=message,text='Не удалось изменить минимум просмотров')
            await car.channel_fleet_info(fleet=[reply_text[1]])
    else:
        await message.reply_text("⚠️ Недостаточно прав, требуется доступ администратора")

async def admin_car_group_input(client:Client,message:Message):
    if message.chat.id==int(bot_config["adminGroup"]):
        reply_text = message.reply_to_message.text.split(':')
        carData=CarData()
        review = Review(Client=client, Msg=message)
        msg_id=[message.id, message.reply_to_message_id,message.reply_to_message.reply_to_message_id]
        if "Введите свою причину отказа" in reply_text[0]:
            await client.delete_messages(message.chat.id, message_ids=[message.id, message.reply_to_message_id])
            await review.rejectReason(group=[reply_text[1]], reason=[message.text])
    else:
        await message.reply_text("⚠️ Недостаточно прав, требуется группа администраторов")

async def admin_group_input(client:Client,message:Message):
    user =await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        group = Group(Client=client, Msg=message)
        msg_id=[message.id, message.reply_to_message_id,message.reply_to_message.reply_to_message_id]
        if "Введите название канала или группы" in reply_text[0]:
            await client.delete_messages(message.chat.id, message_ids=msg_id)
            await group.index(search=message.text)
    else:
        await message.reply_text("⚠️ Недостаточно прав, требуется доступ администратора")

async def admin_user_input(client:Client,message:Message):
    user =await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        user = User(Client=client, Msg=message)
        msg_id=[message.id, message.reply_to_message_id,message.reply_to_message.reply_to_message_id]
        if "Введите юзернейм или имя" in reply_text[0]:
            await client.delete_messages(message.chat.id, message_ids=msg_id)
            await user.getUser(search=message.text)
    else:
        await message.reply_text("⚠️ Недостаточно прав, требуется доступ администратора")

async def admin_bot_blacklist_input(client:Client,message:Message):
    user = await UserAuth(Msg=message).auth(FromUser=message.from_user)
    if user[5] in [1, 2]:
        reply_text = message.reply_to_message.text.split(':')
        blacklist_date=BotBlacklistDate()
        blacklist = BotBlacklist(Client=client, Msg=message)
        msg_id = [message.id, message.reply_to_message_id, message.reply_to_message.reply_to_message_id]
        if "Введите юзернейм бота" in reply_text[0]:
            if "@" in message.text :
                if await blacklist_date.post_bot_blacklist(titel=message.text):
                    await msgNotify(msg=message, text='Бот добавлен в чёрный список')
                else:
                    await msgNotify(msg=message, text='Не удалось добавить бота в чёрный список')
                await client.delete_messages(message.chat.id, message_ids=msg_id)
                await blacklist.index()
            else:
                await msgNotify(msg=message, text='Неверный формат: укажите @юзернейм_бота')
        elif "Введите новый юзернейм бота" in reply_text[0]:
            if "@" in message.text :
                if await blacklist_date.put_bot_blacklist(id=reply_text[1],titel=message.text):
                    await msgNotify(msg=message,text='Запись чёрного списка изменена')
                    await client.delete_messages(message.chat.id, message_ids=msg_id)
                else:
                    await msgNotify(msg=message,text='Не удалось изменить запись')
                await blacklist.index()
            else:
                await msgNotify(msg=message, text='Неверный формат: укажите @юзернейм_бота')
    else:
        await message.reply_text("⚠️ Недостаточно прав, требуется доступ администратора")
