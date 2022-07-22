"""
This __init__.py file takes input from config.py file and changes variables.
It also creates other different instances which are needed by bot to run all modules correctly.

=========================================================\n

© [TeamUltraUnion/rajniixrobot](https://www.github.com/TeamUltraUnion) \n
© [itzzzyashu/rajniixrobot](https://www.github.com/itzzzyashu/rajniixrobot) \n
© [AnimeKaizoku/SaitamaRobot](https://www.github.com/AnimeKaizoku/SaitamaRobot) \n
© [PaulSonOfLars/tgbot](https://www.github.com/PaulSonOfLars/tgbot) \n
All rights reserved.

=========================================================\n
"""

import logging
import os
import sys
import time
import httpx
import spamwatch
import aiohttp
import telegram.ext as tg

from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from ptbcontrib.postgres_persistence import PostgresPersistence
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.sessions import StringSession
from pymongo import MongoClient
from motor import motor_asyncio
from pymongo.errors import ServerSelectionTimeoutError
from odmantic import AIOEngine
from Python_ARQ import ARQ
from aiohttp import ClientSession
from telegraph import Telegraph
from telegram import Chat

__version__ = "5.0"

StartTime = time.time()

# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO)


LOGGER = logging.getLogger(__name__)
# logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)


# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', '')

    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', ''))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get('JOIN_LOGGER', '')
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", '')

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split())
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")


    INFOPIC = bool(os.environ.get("INFOPIC", True))
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", "") # From:- https://openweathermap.org/api
    HEROKU_APP_NAME = (os.environ.get("HEROKU_APP_NAME", False))
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./") # Don't Change
    ERROR_LOGS = os.environ.get("ERROR_LOGS", '')
    HEROKU_API_KEY = (os.environ.get("HEROKU_API_KEY", False))
    EVENT_LOGS = os.environ.get("EVENT_LOGS")
    STRICT_GMUTE = bool(os.environ.get("STRICT_GMUTE", True))
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", '')
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")
    BOT_ID = int(os.environ.get("BOT_ID", ''))
    BOT_NAME = os.environ.get("BOT_NAME", '')
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = int(os.environ.get("API_ID", ''))
    API_HASH = os.environ.get("API_HASH", '')
    DB_URL = os.environ.get("DATABASE_URL")
    MONGO_DB_URL = os.environ.get("MONGO_DB_URI","")
    MONGO_DB = "Rajnii"
    MONGO_PORT = int(os.environ.get("MONGO_PORT", 'None'))
    ARQ_API_URL = "https://thearq.tech"
    GOOGLE_CHROME_BIN = "/usr/bin/google-chrome"
    CHROME_DRIVER = "/usr/bin/chromedriver"
    ARQ_API_KEY = os.environ.get("ARQ_API")
    STRING_SESSION = os.environ.get("STRING_SESSION", '')
    DONATION_LINK = os.environ.get("DONATION_LINK")
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", True))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", True)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", '')
    TIME_API_KEY = os.environ.get("TIME_API_KEY", '')
    AI_API_KEY = os.environ.get("AI_API_KEY", '')
    WALL_API = os.environ.get("WALL_API", '')
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", '')
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", '')
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", '')
    try:
        BL_CHATS = set(int(x) for x in os.environ.get('BL_CHATS', "").split())
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

else:
    from RajniiRobot.config1 import Config
    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        DRAGONS = set(int(x) for x in Config.DRAGONS or [])
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in Config.DEMONS or [])
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in Config.WOLVES or [])
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in Config.TIGERS or [])
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")
    INFOPIC = Config.INFOPIC
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    HEROKU_APP_NAME = Config.HEROKU_APP_NAME
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    ERROR_LOGS = Config.ERROR_LOGS
    HEROKU_API_KEY = Config.HEROKU_API_KEY
    PORT = Config.PORT
    EVENT_LOGS = Config.EVENT_LOGS
    STRICT_GMUTE = Config.STRICT_GMUTE
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    BOT_USERNAME = Config.BOT_USERNAME
    BOT_ID = Config.BOT_ID
    BOT_NAME = Config.BOT_NAME
    RAJNII_IMG = Config.RAJNII_IMG
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    DB_URL = Config.DB_URL
    MONGO_DB_URL = Config.MONGO_DB_URL
    MONGO_DB = Config.MONGO_DB
    MONGO_PORT = Config.MONGO_PORT
    ARQ_API_URL = Config.ARQ_API_URL
    GOOGLE_CHROME_BIN = Config.GOOGLE_CHROME_BIN
    CHROME_DRIVER = Config.CHROME_DRIVER
    ARQ_API_KEY = Config.ARQ_API_KEY
    STRING_SESSION = Config.STRING_SESSION
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    AI_API_KEY = Config.AI_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    UPDATES_LOGS = Config.UPDATES_LOGS
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API

    try:
        BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning(f"[{BOT_NAME} ERROR] SpamWatch API key Is Missing! Recheck Your Config.")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning(f"[{BOT_NAME} ERROR] Can't connect to SpamWatch!")


print("=========================================================================================================")
# Credits Logger
print(f"[{BOT_NAME}] Activating {BOT_NAME}. | SRN • Project C437 | Licensed Under GPLv3.")

print(f"[{BOT_NAME}] [C437 ACTIVATING: Initializing Required Clients]")

print(f"[{BOT_NAME}] Project Maintained By: [github.com/TeamUltraUnion] (telegram.me/TeamUltraUnion)")

from RajniiRobot.modules.sql import SESSION

print(f"[{BOT_NAME}] Installing Telegraph")
telegraph = Telegraph()

print(f"[{BOT_NAME}] Creating Updater, Dispatcher")
updater = tg.Updater(TOKEN, workers=WORKERS, request_kwargs={"read_timeout": 10, "connect_timeout": 10}, use_context=True)
dispatcher = updater.dispatcher

print(f"[{BOT_NAME}] TELETHON CLIENT STARTING")
telethn = TelegramClient(f"{BOT_NAME}", API_ID, API_HASH)

print(f"[{BOT_NAME}] PYROGRAM CLIENT STARTING")
session_name = TOKEN.split(":")[0]
pgram = Client(session_name, api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

print(f"[{BOT_NAME}] Connecting To TUU • Data Center • Mumbai • MongoDB Database")
mongodb = MongoClient(MONGO_DB_URL, MONGO_PORT)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
db = motor[MONGO_DB]
engine = AIOEngine(motor, MONGO_DB)

print(f"[{BOT_NAME}] Connecting To TUU • Data Center • Mumbai • PostgreSQL Database")

print(f"[{BOT_NAME}] INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()

# ARQ Client
print(f"[{BOT_NAME}] INITIALIZATION ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

print(f"[{BOT_NAME}] Connecting To TUU • {BOT_NAME}'s Userbot. (telegram.me/itzzzyashu)")
ubot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
print("\n=========================================================================================================")

timeout = httpx.Timeout(40, pool=None)
http = httpx.AsyncClient(http2=True, timeout=timeout)

async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for pgram in apps:
                if pgram != client:
                    try:
                        entity = await pgram.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = pgram
                        break
            else:
                entity = await pgram.get_chat(entity)
                entity_client = pgram
    return entity, entity_client

apps = [pgram]
DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from RajniiRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
