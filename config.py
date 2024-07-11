
#(©)CodeXBotz
import os
import logging
from logging.handlers import RotatingFileHandler



#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6710150455:AAEUDbI0Z6a7uWLk_p-okmyZ9zmKGhXxFMo")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "26898723"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "6b074d2c9ab42f363d22fa86284f3488")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002001799767"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "6358771146"))

#Port
PORT = os.environ.get("PORT", "8080")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://vippuniya29:YRjCh78euML5fqFg@vipstudios.kzpq3pu.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "filesharexbot1")

"""
delay for message to delete after bot sends them to user. 
default delay is 60 secs you can change it by changing the minutes i mean if u want delay of 2 mins than change 1 to 2 ans so on.
"""
DELAY = int(10 * 60)

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "𝖧𝖾𝗒 {mention} 𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝗍𝗈 𝗈𝗎𝗋 𝖬𝗈𝗏𝗂𝖾 𝖺𝗇𝖽 𝖶𝖾𝖻𝗌𝖾𝗋𝗂𝖾𝗌 𝖯𝗋𝗈𝗏𝗂𝖽𝖾𝗋 𝖡𝗈𝗍. 𝖤𝗑𝖼𝗅𝗎𝗌𝗂𝗏𝖾𝗅𝗒 𝗐𝗈𝗋𝗄 𝖿𝗈𝗋 <a href='https://t.me/Vip_studios'>𝖵𝖨𝖯 𝖲𝗍𝗎𝖽𝗂𝗈𝗌</a> !!\n\n𝖤𝗑𝖼𝗅𝗎𝗌𝗂𝗏𝖾 𝖢𝗈𝗇𝗍𝖾𝗇𝗍, 𝖵𝖨𝖯 𝖤𝗑𝗉𝖾𝗋𝗂𝖾𝗇𝖼𝖾.")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "6358771146").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "𝖧𝖾𝗅𝗅𝗈 {mention} 𝗒𝗈𝗎 𝗁𝖺𝗏𝖾 𝗍𝗈 𝗃𝗈𝗂𝗇 𝗆𝗒 𝗍𝗐𝗈 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌 𝗍𝗈 𝗀𝖾𝗍 𝗒𝗈𝗎𝗋 𝖿𝗂𝗅𝖾𝗌. 𝖪𝗂𝗇𝖽𝗅𝗒 𝗃𝗈𝗂𝗇 𝗍𝗁𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌 𝖺𝗇𝖽 𝗍𝗋𝗒 𝖺𝗀𝖺𝗂𝗇.\n\n𝖤𝗑𝖼𝗅𝗎𝗌𝗂𝗏𝖾 𝖢𝗈𝗇𝗍𝖾𝗇𝗍, 𝖵𝖨𝖯 𝖤𝗑𝗉𝖾𝗋𝗂𝖾𝗇𝖼𝖾.")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

ADMINS.append(OWNER_ID)
ADMINS.append(6358771146)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
