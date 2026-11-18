# Библиотеки бота
from pyrogram import Client, filters, idle
from pyrogram.errors import RPCError,FloodWait,BadRequest,ChannelPrivate
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply, ReplyKeyboardMarkup, \
    Message,ChatMemberUpdated,InputMediaVideo,InputMediaPhoto, MenuButton,BotCommand
from urllib.parse import urlparse, parse_qs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os,re,time,requests,json,asyncio,uvloop,qrcode,io,socket,hashlib,math,datetime,logging
from random import randint
uvloop.install()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a',
    filename='run.log'
)

DB_PATH = os.getenv("SQLITE_DB_PATH", "hutui.db")

bot_config = {
    "botName":"Бот не настроен",
    "indexTxt":"Приветственный текст не настроен",
    "botUserName":"Бот не указан",
    "publicGroup":"Не указан",
    "adminGroup":1,
    "msgGroup":1,
    "notifyType":1,
    "rejectText":[],
    "restrict_limit":60,
    "video": ''
}
scheduler = AsyncIOScheduler(timezone='Asia/Shanghai', job_defaults={'max_instances': 1, 'coalesce': False})

cli_obj={
    "name":"HuTuiBot",
    "api_id":123,
    "api_hash":"123",
    "bot_token":"123",
    "proxy":False,
    "proxyDict":dict(scheme="socks5", hostname="127.0.0.1", port=1080),
    "session":False,
    "sessionTxt":"session.txt"
}
# cli_obj={
#     "name":"HuTuiBot",
#     "api_id":20498498,
#     "api_hash":"25db36a7408a0881455483f13a395c1d",
#     "bot_token":"6842986879:AAGr83oJP8sh4Sz1aP91U6qm2oANNaxCoZA",
#     "proxy":False,
#     "proxyDict":dict(scheme="socks5", hostname="127.0.0.1", port=1080),
#     "session":False,
#     "sessionTxt":"session.txt"
# }

def ClientObj(obj):
    if os.path.exists(obj["sessionTxt"]) and obj["session"]:
        with open(obj["sessionTxt"], "r") as f:
            content = f.read()
        if obj["proxy"]:
            return Client("HuTuiBot", session_string=content,proxy=obj["proxyDict"])
        else:
            return Client("HuTuiBot", session_string=content)
    else:
        if obj["proxy"]:
            return Client(obj["name"], api_id=obj["api_id"], api_hash=obj["api_hash"],bot_token=obj["bot_token"], proxy=obj["proxyDict"])
        else:
            return Client(obj["name"], api_id=obj["api_id"], api_hash=obj["api_hash"], bot_token=obj["bot_token"])

app = ClientObj(obj=cli_obj)
