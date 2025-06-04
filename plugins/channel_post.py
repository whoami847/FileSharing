#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
#Mehediyt69
from bot import Bot
from config import *
from helper_func import encode, admin

@Bot.on_message(filters.private & admin & filters.command('postlink'))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ...!", quote=True)
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ...!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Sʜᴀʀᴇ ᴜʀʟ", url=f'https://telegram.me/share/url?url={link}')]])

    await reply_text.edit(f"<b>Hᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʟɪɴᴋ</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#