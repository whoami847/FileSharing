#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import os
from os import environ, getenv
import logging
from logging.handlers import RotatingFileHandler
from pyrogram import filters
from database.database import db # Updated import

# MehediYT69
# --------------------------------------------
# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
#--------------------------------------------

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002170811388"))  # Your db channel Id
OWNER = os.environ.get("OWNER", "MehediYT69")  # Owner username without @
OWNER_ID = int(os.environ.get("OWNER_ID", "7328629001"))  # Owner id
#--------------------------------------------
PORT = os.environ.get("PORT", "8080")
#--------------------------------------------
DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "animelord")
# --------------------------------------------
FSUB_LINK_EXPIRY = int(getenv("FSUB_LINK_EXPIRY", "10"))  # 0 means no expiry
BAN_SUPPORT = os.environ.get("BAN_SUPPORT", "https://t.me/CodeflixSupport")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))
# --------------------------------------------
START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/ec17880d61180d3312d6a.jpg")
FORCE_PIC = os.environ.get("FORCE_PIC", "https://telegra.ph/file/e292b12890b8b4b9dcbd1.jpg")

# --------------------------------------------
# List of images for random selection in /start, /help, /about
RANDOM_IMAGES = [
    "https://i.postimg.cc/13pMdkmg/d356bdfb.jpg",
    "https://i.postimg.cc/Qt6fbcX0/b8d54419.jpg",
    "https://i.postimg.cc/yY3LmJ2y/8b9e5ade.jpg",
    "https://i.postimg.cc/wjK00qp8/49813b4a.jpg",
    "https://i.postimg.cc/qB5m6cD7/6c576e92.jpg",
    "https://i.postimg.cc/BQRwk52z/76033dd9.jpg",
    "https://i.postimg.cc/wjJbptVj/7d964bb9.jpg",
    "https://i.postimg.cc/SR3D0qY9/19b6b471.jpg",
    "https://i.postimg.cc/G23MGX14/866e109c.jpg",
    "https://i.postimg.cc/FKVWY2wt/79c62968.jpg",
    "https://i.postimg.cc/hvfp3hvg/c8da71f2.jpg",
    "https://i.postimg.cc/LsKwYkXP/a4fcfce8.jpg",
    "https://i.postimg.cc/hv53ST6f/69679b9e.jpg",
    "https://i.postimg.cc/CMm3PfPy/2042520a.jpg",
    "https://i.postimg.cc/W4GKMDFH/6d48d1b1.jpg",
    "https://i.postimg.cc/mDV550S3/4ca7b67e.jpg",
    "https://i.postimg.cc/nLJScHRY/4447ce15.jpg",
    "https://i.postimg.cc/mZXnNWkB/c5f3b6b9.jpg",
    "https://i.postimg.cc/rFDPfZRW/b537ef3d.jpg",
    "https://i.postimg.cc/vTBNF3PJ/f7cf3c04.jpg",
    "https://i.postimg.cc/8zrxzX1D/e2aab718.jpg",
    "https://i.postimg.cc/pTvw7QMv/62881630.jpg",
    "https://i.postimg.cc/2y8Pjz5X/6feaaca3.jpg",
    "https://i.postimg.cc/zXv99X6y/88ed9df7.jpg",
    "https://i.postimg.cc/cHcpNKdn/c5c90314.jpg",
    "https://i.postimg.cc/8cKxjqJk/b8a8fe75.jpg",
    "https://i.postimg.cc/ncLJp1jc/bbb0f2ae.jpg",
    "https://i.postimg.cc/W1FcJbwB/1be60ed8.jpg",
    "https://i.postimg.cc/Nj3q8qN5/4375233f.jpg",
    "https://i.postimg.cc/BZLzgwKF/ae14ca6d.jpg",
    "https://i.postimg.cc/wxCGbcXG/41f94fb2.jpg",
    "https://i.postimg.cc/YqQscG8q/d72690c2.jpg",
    "https://i.postimg.cc/htg3KD38/3853b95b.jpg",
    "https://i.postimg.cc/rwJZmBvB/71102c42.jpg",
    "https://i.postimg.cc/CKxPfv0z/a2a9b463.jpg",
    "https://i.postimg.cc/W4Y9mMpS/57a48500.jpg",
    "https://i.postimg.cc/sXBTTvvz/effd6748.jpg",
    "https://i.postimg.cc/tTL2wpxx/67483d60.jpg",
    "https://i.postimg.cc/XqdQ0mfD/f622366f.jpg",
    "https://i.postimg.cc/3w2MnS69/c4cb7967.jpg",
    "https://i.postimg.cc/bNFjJ2k0/2a4839f6.jpg",
    "https://i.postimg.cc/wjZHWsBx/acfe005d.jpg",
    "https://i.postimg.cc/mkmW7Pqs/433d7985.jpg",
    "https://i.postimg.cc/90mj4dLb/f6f20b4d.jpg",
    "https://i.postimg.cc/mDG44fM0/bbf42737.jpg",
    "https://i.postimg.cc/Xv5Wt7Zf/03d91930.jpg",
    "https://i.postimg.cc/cHMS49B6/703f1491.jpg",
    "https://i.postimg.cc/bN6qt5ct/51d7ef57.jpg",
    "https://i.postimg.cc/RFcMJV4S/a64e9d8d.jpg",
    "https://i.postimg.cc/qBxJkR1Q/c5c76509.jpg",
    "https://i.postimg.cc/KjfxQq1C/543bef60.jpg",
    "https://i.postimg.cc/c4cr5Tqx/ef20762f.jpg",
    "https://i.postimg.cc/g2nmqKmB/251e6076.jpg",
    "https://i.postimg.cc/tgqdM7vf/ec2b82f2.jpg",
    "https://i.postimg.cc/0jP9YRyp/1e732953.jpg",
    "https://i.postimg.cc/pXV2yH7v/421d28be.jpg",
    "https://i.postimg.cc/1RGtfM3G/8764426c.jpg",
    "https://i.postimg.cc/yN36ByGS/503cbd75.jpg",
    "https://i.postimg.cc/0yQ2Xsdn/6c60b12f.jpg",
    "https://i.postimg.cc/v8grjJXQ/c12da0bb.jpg",
    "https://i.postimg.cc/sXFj2ZFH/0552f2c8.jpg",
    "https://i.postimg.cc/vm07FMpm/3b557384.jpg",
    "https://i.postimg.cc/C5gxcnmn/ac7ac5cd.jpg",
    "https://i.postimg.cc/tT739wjN/97974e38.jpg",
    "https://i.postimg.cc/P5rPGZhm/2ff5d9e0.jpg",
    "https://i.postimg.cc/g2d3xnpJ/95b264c0.jpg",
    "https://i.postimg.cc/zDsC1xPT/34715973.jpg",
    "https://i.postimg.cc/PJw1wDNL/c97b2ca2.jpg",
    "https://i.postimg.cc/kXWxMWkz/25881c5f.jpg",
    "https://i.postimg.cc/nrbCNPcz/2101537a.jpg",
    "https://i.postimg.cc/L6msffJr/5a10499e.jpg",
    "https://i.postimg.cc/d0g1TxCB/382a3ccc.jpg",
    "https://i.postimg.cc/Y2WF81q0/4c9fd376.jpg",
    "https://i.postimg.cc/MpFZhF9S/308acd05.jpg",
    "https://i.postimg.cc/TPNbN0DL/0d7f49fc.jpg",
    "https://i.postimg.cc/d3jtpQxH/33fd9789.jpg",
    "https://i.postimg.cc/GpmYjVHn/651d6af3.jpg",
    "https://i.postimg.cc/NjJLQMfZ/79231686.jpg",
    "https://i.postimg.cc/qvLyy4BG/1c111b46.jpg",
    "https://i.postimg.cc/vB64qsyk/9afa42bf.jpg",
    "https://i.postimg.cc/3RpwjFCH/0e73df87.jpg",
    "https://i.postimg.cc/qqyCRdZy/99b50b8e.jpg",
    "https://i.postimg.cc/tJ3YbNYz/53d24df2.jpg",
    "https://i.postimg.cc/63DvtQzB/8f8f759b.jpg",
    "https://i.postimg.cc/2jhqnr2B/a1e31adf.jpg",
    "https://i.postimg.cc/VLPChddR/b7dcd4a1.jpg"
]

MESSAGE_EFFECT_IDS = [
    5104841245755180586,  # 🔥
    5107584321108051014,  # 👍
    5044134455711629726,  # ❤️
    5046509860389126442,  # 🎉
    5104858069142078462,  # 👎
    5046589136895476101,  # 💩
]


SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "linkshortify.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/hwdownload/3")
SHORT_MSG = "<b>⌯ Here is Your Download Link, Must Watch Tutorial Before Clicking On Download...</b>"

SHORTENER_PIC = os.environ.get("SHORTENER_PIC", "https://telegra.ph/file/ec17880d61180d3312d6a.jpg")
# --------------------------------------------

# --------------------------------------------
HELP_TXT = os.environ.get("HELP_TXT","<blockquote><b>ʜᴇʟʟᴏ {first}<b/></blockquote>\n\n<b><blockquote>◈ ᴛʜɪs ɪs ᴀɴ ғɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ ᴡᴏʀᴋ ғᴏʀ @MehediYT69\n\n❏ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs\n├/start : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n├/about : ᴏᴜʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ\n├/commands : ꜰᴏʀ ɢᴇᴛ ᴀʟʟ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs ʟɪꜱᴛ\n└/help : ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ʙᴏᴛ\n\n sɪᴍᴘʟʏ ᴄʟɪᴄᴋ ᴏɴ ʟɪɴᴋ ᴀɴᴅ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜᴀᴛs ɪᴛ.....!\n\n ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ <a href=https://t.me/Anime_Lord_Bots>Aɴɪᴍᴇ Lᴏʀᴅ</a></blockquote></b>")
ABOUT_TXT = os.environ.get("ABOUT_TXT","<blockquote><b>ʜᴇʟʟᴏ {first}<b/></blockquote>\n\n<b><blockquote>◈ ᴄʀᴇᴀᴛᴏʀ: <a href=https://t.me/Anime_Lord_Bots>MehediYT</a>\n◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=@who_am_i_69>WHO-AM-I</a>\n◈ ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/Anime_Lord_Official>Aɴɪᴍᴇ Lᴏʀᴅ</a>\n◈ sᴇʀɪᴇs ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/Anime_Lord_Series>Aɴɪᴍᴇ Lᴏʀᴅ sᴇʀɪᴇs ғʟɪx</a>\n◈ ᴀᴅᴜʟᴛ ᴍᴀɴʜᴡᴀ : <a href=https://t.me/Anime_Lord_Hentai>Aɴɪᴍᴇ Lᴏʀᴅ Pᴏʀɴʜᴡᴀs</a>\n◈ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/Anime_Lord_Bots>Aɴɪᴍᴇ Lᴏʀᴅ</a></blockquote></b>")
# --------------------------------------------
START_MSG = os.environ.get("START_MESSAGE", "<blockquote><b>ʜᴇʟʟᴏ {first}</b></blockquote>\n\n<blockquote><b> ɪ ᴀᴍ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ ᴄʀᴇᴀᴛᴇᴅ ʙʏ  <a href=https://t.me/Anime_Lord_Official>Aɴɪᴍᴇ Lᴏʀᴅ</a>, ɪ ᴄᴀɴ sᴛᴏʀᴇ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇs ɪɴ sᴘᴇᴄɪғɪᴇᴅ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴏᴛʜᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ɪᴛ ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ.</blockquote></b>")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<blockquote><b>ʜᴇʟʟᴏ {first}</b></blockquote>\n\n<blockquote><b>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ꜰɪʟᴇ.</b></blockquote>")

CMD_TXT = """<blockquote><b>» ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:</b></blockquote>

<b>›› /start :</b> sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ & ɢᴇᴛ ᴘᴏsᴛs
<b>›› /batch :</b> ᴄʀᴇᴀᴛᴇ ʟɪɴᴋs ғᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ᴘᴏsᴛs
<b>›› /custom_batch :</b> ᴄʀᴇᴀᴛᴇ ᴄᴜsᴛᴏᴍ ʙᴀᴛᴄʜ ғʀᴏᴍ ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ
<b>›› /genlink :</b> ᴄʀᴇᴀᴛᴇ ʟɪɴᴋ ғᴏʀ ᴀ sɪɴɢʟᴇ ᴘᴏsᴛ
<b>›› /flink :</b> ꜱᴇᴛ ᴀᴜᴛᴏ ʙᴀᴛᴄʜ ꜰᴏʀᴍᴀᴛ
<b>›› /forcesub :</b> ɢᴇᴛ ᴀʟʟ ғᴏʀᴄᴇ sᴜʙ sᴇᴛᴛɪɴɢs
<b>›› /admin :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴀᴅᴍɪɴs (ᴀᴅᴅ/ʀᴇᴍᴏᴠᴇ/ʟɪsᴛ)
<b>›› /user :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɢᴇᴛ ᴜsᴇʀ-ʀᴇʟᴀᴛᴇᴅ ᴛᴏᴏʟs
<b>›› /auto_delete :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ sᴇᴛ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ
<b>›› /fsettings :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴍᴀɴᴀɢᴇ ғᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴs
<b>›› /premium_cmd :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs
<b>›› /broadcast_cmd :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇs
<b>›› /myplan :</b> ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ sᴛᴀᴛᴜs & ᴅᴇᴛᴀɪʟs
<b>›› /count :</b> ᴛʀᴀᴄᴋ sʜᴏʀᴛɴᴇʀ ᴄʟɪᴄᴋs & ᴀɴᴀʟʏᴛɪᴄs"""

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>• ʙʏ @Anime_Lord_Official</b>")
# --------------------------------------------
# Set true if you want Disable your Channel Posts Share button
# --------------------------------------------
BOT_STATS_TEXT = "<b>BOT FUCKTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!"

# ==========================(BUY PREMIUM)====================#
OWNER_TAG = os.environ.get("OWNER_TAG", "Aɴɪᴍᴇ Lᴏʀᴅ")
UPI_ID = os.environ.get("UPI_ID", "yourname@upi")  # Replace with your valid UPI ID
QR_PIC = os.environ.get("QR_PIC", "https://telegra.ph/file/3e83c69804826b3cba066.jpg")
SCREENSHOT_URL = os.environ.get("SCREENSHOT_URL", "t.me/mehediyt69")
# --------------------------------------------
# Time and its price
# 7 Days
PRICE1 = os.environ.get("PRICE1", "0 rs")
# 1 Month
PRICE2 = os.environ.get("PRICE2", "60 rs")
# 3 Month
PRICE3 = os.environ.get("PRICE3", "150 rs")
# 6 Month
PRICE4 = os.environ.get("PRICE4", "280 rs")
# 1 Year
PRICE5 = os.environ.get("PRICE5", "550 rs")

# ====================(END)========================#

# Default settings (loaded dynamically in bot.py)
PROTECT_CONTENT = False
HIDE_CAPTION = False
DISABLE_CHANNEL_BUTTON = True
BUTTON_NAME = None
BUTTON_LINK = None

# Function to update settings (used by file_settings.py)
async def update_setting(setting_name, value):
    await db.update_setting(setting_name, value)
    # Update local variables (optional, for immediate use)
    global PROTECT_CONTENT, HIDE_CAPTION, DISABLE_CHANNEL_BUTTON, BUTTON_NAME, BUTTON_LINK
    if setting_name == "PROTECT_CONTENT":
        PROTECT_CONTENT = value
    elif setting_name == "HIDE_CAPTION":
        HIDE_CAPTION = value
    elif setting_name == "DISABLE_CHANNEL_BUTTON":
        DISABLE_CHANNEL_BUTTON = value
    elif setting_name == "BUTTON_NAME":
        BUTTON_NAME = value
    elif setting_name == "BUTTON_LINK":
        BUTTON_LINK = value

# Function to get all settings (used to display in /fsettings)
def get_settings():
    return {
        "PROTECT_CONTENT": PROTECT_CONTENT,
        "HIDE_CAPTION": HIDE_CAPTION,
        "DISABLE_CHANNEL_BUTTON": DISABLE_CHANNEL_BUTTON,
        "BUTTON_NAME": BUTTON_NAME,
        "BUTTON_LINK": BUTTON_LINK
    }

LOG_FILE_NAME = "animelordbot.txt"

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

# Admin filter to check if user is an admin or owner
async def admin_filter(_, __, message):
    admin_ids = await db.get_all_admins()
    return message.from_user.id in admin_ids or message.from_user.id == OWNER_ID

admin = filters.create(admin_filter)

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
