import logging

from pyrogram.handlers import *
from monitor.command import *
from monitor.input import *
from config import *


def command(client: Client):
    '''开始命令或者首页命令'''
    client.add_handler(MessageHandler(start_handler, filters.command(["start", "index"]) & filters.private))
    # 呼叫管理员页面命令
    client.add_handler(
        MessageHandler(admii_command, filters.private & (filters.command("admin") | filters.regex("⚙管理页面"))))
    # 普通用户路由
    client.add_handler(CallbackQueryHandler(callback_query_router, filters.create(
        lambda _, __, query: (query.data and query.data.startswith("r/")))))
    # 管理员路由
    client.add_handler(CallbackQueryHandler(admin_callback_query_router, filters.create(
        lambda _, __, query: (query.data and query.data.startswith("a/")))))
    # 用户群组消息更新
    client.add_handler(ChatMemberUpdatedHandler(handle_chat_member_update))
    # # 用户删除消息监控
    # client.add_handler(DeletedMessagesHandler(delete_message))
    # # 用户修改了消息
    # client.add_handler(EditedMessageHandler(edited_message))
    # 回复机器人配置消息输入监视器
    client.add_handler(MessageHandler(admin_config_reply_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("📲")
        )
    )))
    # 广告管理输入监视器
    client.add_handler(MessageHandler(admin_advertising_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("🗞️")
        )
    )))
    # 车队管理输入监视器
    client.add_handler(MessageHandler(admin_car_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("🚒")
        )
    )))
    # 车队管理群组输入监视器
    client.add_handler(MessageHandler(admin_car_group_input, filters.group & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("💭")
        )
    )))
    # 群频道管理输入监视器
    client.add_handler(MessageHandler(admin_group_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("🏵️")
        )
    )))
    # 机器人黑名单输入监视器
    client.add_handler(MessageHandler(admin_bot_blacklist_input, filters.private & filters.reply & filters.create(
        lambda _, __, query: (
                query.reply_to_message.text and query.reply_to_message.text.startswith("🤖")
        )
    )))
    # 用户管理输入
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
        print('已经启动过')
    else:
        try:
            logging.critical('启动成功')
            bot_config = get_config()
            logging.critical(f"读取配置文件:{bot_config}")
            scheduler.start()
            schedulerObj = scheduler.add_job(convoyDriving, "interval", seconds=60 * 30, misfire_grace_time=60)
            logging.critical(f"定时器执行时间:{schedulerObj}")
            command(app)
            app.run()
        except Exception as e:
            logging.error(e)
