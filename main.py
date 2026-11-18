import logging

from pyrogram.handlers import *
from monitor.command import *
from monitor.input import *
from config import *


def command(client: Client):
    '''Команды запуска и главной страницы'''
    client.add_handler(MessageHandler(start_handler, filters.command(["start", "index"]) & filters.private))
    # Команда вызова панели администратора
    client.add_handler(
        MessageHandler(admii_command, filters.private & (filters.command("admin") | filters.regex("⚙Панель управления"))))
    # Маршрутизация обычных пользователей
    client.add_handler(CallbackQueryHandler(callback_query_router, filters.create(
        lambda _, __, query: (query.data and query.data.startswith("r/")))))
    # Маршрутизация администраторов
    client.add_handler(CallbackQueryHandler(admin_callback_query_router, filters.create(
        lambda _, __, query: (query.data and query.data.startswith("a/")))))
    # Обновление статуса участников в группах и каналах
    client.add_handler(ChatMemberUpdatedHandler(handle_chat_member_update))
    # # Отслеживание удаления сообщений
    # client.add_handler(DeletedMessagesHandler(delete_message))
    # # Отслеживание редактирования сообщений
    # client.add_handler(EditedMessageHandler(edited_message))
    # Монитор ввода настроек бота (ответ на сообщение)
    client.add_handler(MessageHandler(admin_config_reply_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("📲")
        )
    )))
    # Монитор ввода управления рекламой
    client.add_handler(MessageHandler(admin_advertising_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("🗞️")
        )
    )))
    # Монитор ввода управления подборками
    client.add_handler(MessageHandler(admin_car_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("🚒")
        )
    )))
    # Монитор группового ввода при модерации подборок
    client.add_handler(MessageHandler(admin_car_group_input, filters.group & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("💭")
        )
    )))
    # Монитор ввода управления группами и каналами
    client.add_handler(MessageHandler(admin_group_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("🏵️")
        )
    )))
    # Монитор ввода чёрного списка ботов
    client.add_handler(MessageHandler(admin_bot_blacklist_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("🤖")
        )
    )))
    # Монитор ввода поиска пользователей
    client.add_handler(MessageHandler(admin_user_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("👨‍💻")
        )
    )))


if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 47209))
    except socket.error:
        print('Бот уже запущен')
    else:
        try:
            logging.critical('Запуск успешен')
            bot_config = get_config()
            logging.critical(f"Конфигурация загружена:{bot_config}")
            scheduler.start()
            schedulerObj = scheduler.add_job(convoyDriving, "interval", seconds=60 * 30, misfire_grace_time=60)
            logging.critical(f"Таймер рассылки запущен:{schedulerObj}")
            command(app)
            app.run()
        except Exception as e:
            logging.error(e)
