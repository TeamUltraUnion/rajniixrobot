import json
import os

def get_user_list(config, key):
    with open('{}/RajniiRobot/{}'.format(os.getcwd(), config), 'r') as json_file:
        return json.load(json_file)[key]

class Config(object):
    """This Config class that contains all config values that are required to run your bot.\n
    This config.py file will help you to host your bot from command line interface or local hosting.\n
    You need to fill all required values correctly.\n
    =========================================================\n
    Requirements you need to host from a cli are:
    - Command Line Interface(VPS)
    - Browser
    - Any IDE for further development, Microsoft Visual Studio Code is Recommended.
    - Should know python basics
    - Should know about telegram APIs
    - A device to save all the files for backup.
    
    Now edit the config.py file as it wants, Read the comments for perfect guide to get all necessary values.\n
    Please read the manual for more information.\n
    You can also get deploying tutorials there. [[Read Manual](https://www.itzzzyashu-cf.tk/projects#rajniiroboactive)].\n
    =========================================================\n
    This Class is seperated in six sections:
    - `Required [V-PTB]` for your Values related to your Python Telegram Bot.
    - `Required [C/S-U/I]` for required Channel and Support - Usernames/IDs.
    - `Required [V-SU]` for required Values of Support Users.
    - `Required [V-D/C]` for required Values related to Database and Cloud.
    - `Required [V-IAK]` for required Values related to IDs, APIs and KEYs.
    - `Required [V-P/D]` for required Values related to Paths and Directories.
    + Values with '+' in comments are Important for bot to run.
    
    =========================================================\n
    [Team Sanatan Raksha Network™](https://www.github.com/TeamSanatanRakshaNetwork), All rights reserved.\n
    Project [rajniiroboactive](https://www.github.com/TeamSanatanRakshaNetwork/rajniiroboactive) have © Copyright of [@itzzzyashu](https://www.github.com/itzzzyashu).
    
    =========================================================\n
    """
    LOGGER = True

    "Required [V-PTB]"
    TOKEN = '' # + Get it by @botfather on telegram after making a bot.
    BOT_NAME = "𝔯𝔞𝔧𝔫𝔦𝔦𝔯𝔬𝔟𝔬𝔱" # + Your bot name that you've chosen while making it by @botfather on telegram.
    BOT_ID = 5115748490 # + Add your bot and @MissRose_bot to a private/public group, send "/id @your-bot-username" there and copy the ID given by Rose bot.
    BOT_USERNAME = "rajniixrobot" # + Your telgram bot's username without @, get it from telegram.
    RAJNII_IMG = "https://telegra.ph/file/c7265fd25e4f2baaed8cc.jpg" # + IMAGE url that you want to display at bot's start menu
    INFOPIC = True # + True or False, do you want your bot to send user's first profile pic with User Info by execution of "/info" command?
    STRICT_GMUTE = True # + True or False, do you want 'gmuted users' muted in new groups too ?.
    STRICT_GBAN = True # + True or False, do you want 'gbanned users' get banned in new groups too?
    ALLOW_EXCL = True # + True or False, do you want users can use '!' for commands too.
    ALLOW_CHATS = True # + True or False, bot can be added into other groups?
    DEL_CMDS = True # + True or False, do you want your bot delete the commands that normal users can't use?
    DONATION_LINK = "https://telegram.me/RajniSpam" # + If you want users to donate money on your account, for any purpose.
    BAN_STICKER = "xx" # ban sticker
    LOAD = "" # Modules to be loaded, there's no need to fill it.
    NO_LOAD = "" # Modules you don't want to load in your bot. It's your choice, leave it empty if you want each module to get loaded.

    "Required [C/S-U/I]"
    SUPPORT_CHAT = "rajniixsupport" # + Create a public group on telegram, fill your support chat's username here; Make sure to add your bot to this chat as Admin.
    UPDATES_LOGS = "rajniixupdates" # + Create a public group on telegram, fill your update channel's username here; Make sure to add your bot to this chat as Admin.
    JOIN_LOGGER = "-1001615857456" # + Create a private/public channel on telegram, send anything and forward that message to @MissRose_bot and reply the forwarded message with "/id", copy the channel ID; it's for logging message when someone add your bot to a group.
    ERROR_LOGS = "rajniixsupport" # + Create a private/public group on telegram, send anything in it and forward that message to @MissRose_bot and reply the forwarded message with "/id", copy the channel ID.
    EVENT_LOGS = "-1001788668346" # + Create a private/public channel on telegram, send anything and forward that message to @MissRose_bot and reply the forwarded message with "/id", copy the channel ID; it's for logging Global Actions.
    SPAMWATCH_SUPPORT_CHAT = "SPAMWATCHSUPPORT" # + SpamWatch Support Chat username from telegram.
    BL_CHATS = "" # ID's of telegram groups, in which you don't want anyone to add your bot; (your bot can't join blacklisted groups); you can get it by sending '/id' into it, Miss Rose or any other bot should be there.

    "Required [V-SU]"
    OWNER_ID = '5365743068' # + Send "/id" to @MissRose_bot on telegram and copy your Telegram id that you get by her.
    OWNER_USERNAME = "Itzzzyashu" # + Your telegram username here without @, get it from telegram.
    DRAGONS = [1118151835] # ID's of users whom you want give Global Banning & SUDO Rights (SUDO have less rights then developers and owner), also known as sudo users.
    DEV_USERS = [5205895700, 5262453320] # ID's of users who can use shell, and test codes known as devs.
    DEMONS = [2116934109] # ID's of users who can ban and mute users globally by your bot, they can't use all sudo rights, also known as Support Staff Members.
    WOLVES = [] # ID's of users who just cannot be restricted by your bot through ban, mute, warn and global ban, mute commands, known as Immune Users.
    TIGERS = [] # ID's of users who can use warn, mute, ban and admin commands through your bot, are Immune from all restriction commands of your bot.

    "Required - [V-D/C]"
    WORKERS = 8 # + There's no need to change it.
    DB_URL = "" # + postgresql or elephantsql database link.
    
    HEROKU_APP_NAME = '' # Heroku App Name, if you're using Heroku.com for deployment of this bot.
    HEROKU_API_KEY = "" # True or False, if you are using Heroku.com for deployment, get it from heroku account info; otherwise leave it empty.
    URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/" # If you're using heroku.com, fill it with "https://your-app-name.herokuapp.com"; otherwise leave it empty.
    WEBHOOK = "" # Fill if you're using webhook.
    MONGO_DB = "" # + Copy and paste your Mongodb Cluster name here.
    MONGO_PORT = 27018 # + Google Mongo db port; copy and paste.
    MONGO_DB_URL = "" # + Signup/Login on https://www.mongodb.com create cluster and get database uri.
    ARQ_API_URL = "https://arq.hamker.in" # + ARQ API URL, don't change it.

    "Required [V-IAK]"
    API_ID = 123456 # + Login https://my.telegram.org with your telegram account, select "Api Development Tools" create an app and copy APP_ID from there.
    API_HASH = "" # + Login https://my.telegram.org with your telegram account, select "Api Development Tools" create an app and copy APP_HASH from there.
    OPENWEATHERMAP_ID = "" # + 
    REM_BG_API_KEY = "" #+ 
    CASH_API_KEY = "" # + Get it from https://...
    TIME_API_KEY = "" # + Get it from https://...
    AI_API_KEY = "" # + Ask @kukiaisupport on telegram about it.
    STRING_SESSION = "" # + Replit run 
    ARQ_API_KEY = "" # + Get it from @ARQRobot on telegram.
    WALL_API = "xyz" # Get it from https://...
    SPAMWATCH_API = "" # + Get it from @SpamWatchbot on telegram.

    "Required [V-P/D]"
    TEMP_DOWNLOAD_DIRECTORY = "./" # + Don't Change it (It can cause many errors if changed).
    CERT_PATH = "CERT_PATH" # + 
    GOOGLE_CHROME_BIN = "/usr/bin/google-chrome" # + Don't change it.
    CHROME_DRIVER = "/usr/bin/chromedriver" # + Don't change it.
    PORT = 5000 # + Needed

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
