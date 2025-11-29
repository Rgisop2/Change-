# +++ Modified By Yato [telegram username: @i_killed_my_clan & @ProYato] +++ 
# aNDI BANDI SANDI JISNE BHI CREDIT HATAYA USKI BANDI RAndi 

import os
import logging
import re
from logging.handlers import RotatingFileHandler

id_pattern = re.compile(r'^-?\d+$')

# ------------ SAFE GETTERS ------------
def to_int(val, varname):
    if val is None or val == "":
        raise RuntimeError(f"{varname} is required but missing!")
    if not id_pattern.match(str(val)):
        raise RuntimeError(f"{varname} must be an integer. Got: {val}")
    return int(val)

# ============ FIXED VALUES FROM YOU ==========

TG_BOT_TOKEN = "8258328792:AAGwI72WIXwCKJNMua-6ZMC0vskl-V809Pc"
APP_ID = to_int("23715627", "APP_ID")
API_HASH = "26c335fe953856eb72845e02c6c44930"

OWNER_ID = to_int("6901339051", "OWNER_ID")
PORT = to_int("8080", "PORT")

DB_URI = "mongodb+srv://rj5706603:O95nvJYxapyDHfkw@cluster0.fzmckei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "linkchange"

START_PIC = "https://i.ibb.co/DPJzGSKj/7700112188-fac05ef4.jpg"
START_IMG = "https://i.ibb.co/FbvfM8Mh/7700112188-6e9c9c7a.jpg"

START_MSG = "<b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴀᴅᴠᴀɴᴄᴇᴅ ʟɪɴᴋs sʜᴀʀɪɴɢ ʙᴏᴛ. ᴡɪᴛʜ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ ᴄᴀɴ sʜᴀʀᴇ ʟɪɴᴋs ᴀɴᴅ ᴋᴇᴇᴘ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs sᴀғᴇ ғʀᴏᴍ ᴄʜᴀᴘʀɪɢʜᴛ ɪssᴜᴇs.\n\n<blockquote>‣ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <a href='https://t.me/Apni_aukat_me_raho786'>ʏᴀᴛᴏ</a></blockquote></b>"

HELP = "<b><blockquote expandable>» Creator: <a href=https://t.me/Apni_aukat_me_raho786>Yato</a>\n» Our Community: <a href=https://t.me/Apni_aukat_me_raho786>Flix Network</a>\n» Anime Channel: <a href=https://t.me/animes_cruise>Anime Cruise</a>\n» Ongoing Anime: <a href=https://t.me/Ongoing_cruise>Ongoing cruise</a>\n» Developer: <a href=https://t.me/onlyyuji>Yuji</a></b>"

ABOUT = "<b><blockquote expandable>This bot is developed by Yato (@ProYato) to securely share Telegram channel links with temporary invite links, protecting your channels from copyright issues.</b>"

ABOUT_TXT = "<b>›› ᴄᴏᴍᴍᴜɴɪᴛʏ: <a href='https://t.me/otakuflix_network'>ᴏᴛᴀᴋᴜғʟɪx</a>\n<blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/codeflix_bots'>Cʟɪᴄᴋ ʜᴇʀᴇ</a>\n›› ᴏᴡɴᴇʀ: <a href='https://t.me/cosmic_freak'>ʏᴀᴛᴏ</a>\n›› ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a>\n›› ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a>\n›› ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a>\n›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @ProYato</b></blockquote>"

# ------------ REQUIRED: YOU MUST CHANGE THIS ----------
# If you leave it blank, bot will CRASH.
DATABASE_CHANNEL = to_int("-1001918476761", "DATABASE_CHANNEL")  
# ↑ Replace with your real channel ID

TG_BOT_WORKERS = 40

TEXT = "<b>{mention},\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {title} ɪs ᴀᴘᴘʀᴏᴠᴇᴅ.\n‣ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Codeflix_Bots</b>"
APPROVED = "on"

CHAT_ID = []

# -------- Admins ----------
ADMINS = [1327021082, OWNER_ID]

# -------- Logging ----------
LOG_FILE_NAME = "links-sharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
