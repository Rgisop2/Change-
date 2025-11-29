# +++ Modified By [telegram username: @Codeflix_Bots]
import os
from os import environ
import logging
import re
from logging.handlers import RotatingFileHandler

# Regex for integer check
id_pattern = re.compile(r'^-?\d+$')

# ---------- SAFE INT GETTER ----------
def safe_int(value, default=None, required=False, varname=""):
    if value is None or value.strip() == "":
        if required:
            raise RuntimeError(f"❌ ENV ERROR: '{varname}' is required but missing!")
        return default
    if not id_pattern.match(value):
        raise RuntimeError(f"❌ ENV ERROR: '{varname}' must be integer. Got: {value}")
    return int(value)

# ---------- RECOMMENDED ----------
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8258328792:AAGwI72WIXwCKJNMua-6ZMC0vskl-V809Pc")
APP_ID = safe_int(os.environ.get("APP_ID", "23715627"), required=True, varname="APP_ID")
API_HASH = os.environ.get("API_HASH", "26c335fe953856eb72845e02c6c44930")

# ---------- MAIN ----------
OWNER_ID = safe_int(os.environ.get("OWNER_ID", "1327021082"), required=True, varname="OWNER_ID")
PORT = safe_int(os.environ.get("PORT", "8080"), default=8080, varname="PORT")

# ---------- DATABASE ----------
DB_URI = os.environ.get(
    "DB_URI",
    "mongodb+srv://rj5706603:O95nvJYxapyDHfkw@cluster0.fzmckei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
DB_NAME = os.environ.get("DB_NAME", "linkchange")

# ---------- AUTO APPROVE ----------
CHAT_ID = [
    int(app_chat_id) if id_pattern.search(app_chat_id) else app_chat_id
    for app_chat_id in environ.get("CHAT_ID", "").split()
]

TEXT = environ.get(
    "APPROVED_WELCOME_TEXT",
    "<b>{mention},\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {title} ɪs ᴀᴘᴘʀᴏᴠᴇᴅ.\n‣ Powered by @Codeflix_Bots</b>"
)
APPROVED = environ.get("APPROVED_WELCOME", "on").lower()

# ---------- DEFAULT ----------
TG_BOT_WORKERS = safe_int(os.environ.get("TG_BOT_WORKERS", "40"), default=40, varname="TG_BOT_WORKERS")

# ---------- START PICS ----------
START_PIC = "https://telegra.ph/file/f3d3aff9ec422158feb05-d2180e3665e0ac4d32.jpg"
START_IMG = "https://telegra.ph/file/f3d3aff9ec422158feb05-d2180e3665e0ac4d32.jpg"

# ---------- MESSAGES ----------
START_MSG = os.environ.get(
    "START_MESSAGE",
    "<b>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴀᴅᴠᴀɴᴄᴇᴅ ʟɪɴᴋs sʜᴀʀɪɴɢ ʙᴏᴛ."
    "<blockquote>Maintained by: <a href='https://t.me/codeflix_bots'>ʏᴀᴛᴏ</a></blockquote></b>"
)

HELP = os.environ.get(
    "HELP_MESSAGE",
    "<b><blockquote expandable>» Creator: <a href=https://t.me/proyato>Yato</a>\n"
    "» Our Community: <a href=https://t.me/otakuflix_network>Flix Network</a>\n"
    "» Anime Channel: <a href=https://t.me/animes_cruise>Anime Cruise</a>\n"
    "» Ongoing Anime: <a href=https://t.me/Ongoing_cruise>Ongoing cruise</a>\n"
    "» Developer: <a href=https://t.me/onlyyuji>Yuji</a></b>"
)

ABOUT = os.environ.get(
    "ABOUT_MESSAGE",
    "<b><blockquote expandable>This bot is developed by Yato (@ProYato) to securely share Telegram links.</b>"
)

ABOUT_TXT = """<b>›› ᴄᴏᴍᴍᴜɴɪᴛʏ: <a href='https://t.me/otakuflix_network'>ᴏᴛᴀᴋᴜғʟɪx</a>
<blockquote expandable>›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/codeflix_bots'>Click Here</a>
›› ᴏᴡɴᴇʀ: <a href='https://t.me/cosmic_freak'>Yato</a>
›› ʟᴀɴɢᴜᴀɢᴇ: Python 3
›› ʟɪʙʀᴀʀʏ: Pyrogram v2
›› ᴅᴀᴛᴀʙᴀsᴇ: MongoDB
›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @ProYato</b></blockquote>"""

CHANNELS_TXT = """<b>›› Anime: <a href='https://t.me/animes_cruise'>Anime Cruise</a>
<blockquote expandable>›› Movies: <a href='https://t.me/movieflixspot'>MovieFlix Spot</a>
›› Webseries: <a href='https://t.me/webseries_flix'>Webseries Flix</a>
›› Adult: <a href='https://t.me/hanime_arena'>CornHub</a>
›› Manhwa: <a href='https://t.me/pornhwa_flix'>PornHwa</a>
›› Community: <a href='https://t.me/otakuflix_network'>Otakuflix</a>
›› Developer: @ProYato</b></blockquote>"""

# ---------- BOT STATS & REPLY (ADDED BACK) ----------
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "⚠️ ғᴜᴄᴋ ʏᴏᴜ, ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ᴍᴀsᴛᴇʀ. ɢᴏ ᴀᴡᴀʏ, ʙɪᴛᴄʜ 🙃!"

# ---------- REQUIRED DATABASE CHANNEL ----------
DATABASE_CHANNEL = safe_int("-1001918476761", required=True, varname="DATABASE_CHANNEL")

# ---------- ADMINS ----------
try:
    ADMINS = []
    for x in os.environ.get("ADMINS", "1327021082").split():
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Admins must be integers.")

ADMINS.append(OWNER_ID)
ADMINS.append(1327021082)

# ---------- LOGGING ----------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("links-sharingbot.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
