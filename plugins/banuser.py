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
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *

# Function to show user settings with user list, buttons, and message effects
async def show_user_settings(client: Client, chat_id: int, message_id: int = None):
    settings_text = "<b>›› Uꜱᴇʀ Sᴇᴛᴛɪɴɢꜱ:</b>\n\n"
    user_ids = await db.full_userbase()

    if not user_ids:
        settings_text += "<i>Nᴏ ᴜꜱᴇʀꜱ ᴄᴏɴғɪɢᴜʀᴇᴅ ʏᴇᴛ.</i>"
    else:
        settings_text += "<blockquote><b>⚡ Cᴜʀʀᴇɴᴛ Uꜱᴇʀꜱ:</b></blockquote>\n\n"
        for idx, user_id in enumerate(user_ids[:5], 1):  # Show up to 5 users
            try:
                user = await client.get_users(user_id)
                name = user.first_name if user.first_name else "Unknown"
                settings_text += f"<blockquote><b>{idx}. {name} - <code>{user_id}</code></b></blockquote>\n"
            except Exception as e:
                settings_text += f"<blockquote><b>{idx}. Unknown - <code>{user_id}</code></b></blockquote>\n"
        if len(user_ids) > 5:
            settings_text += f"<blockquote><i>...and {len(user_ids) - 5} more.</i></blockquote>\n"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Bᴀɴ Uꜱᴇʀ", callback_data="user_ban"),
                InlineKeyboardButton("Uɴʙᴀɴ Uꜱᴇʀ •", callback_data="user_unban")
            ],
            [
                InlineKeyboardButton("Uꜱᴇʀ Lɪꜱᴛ", callback_data="user_list"),
                InlineKeyboardButton("Bᴀɴ Lɪꜱᴛ", callback_data="user_banlist")
            ],
            [
                InlineKeyboardButton("• Rᴇꜰʀᴇꜱʜ •", callback_data="user_refresh"),
                InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="user_close")
            ]
        ]
    )

    # Select random image and effect
    selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC
    selected_effect = random.choice(MESSAGE_EFFECT_IDS) if MESSAGE_EFFECT_IDS else None

    if message_id:
        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Failed to edit user settings message: {e}")
    else:
        try:
            await client.send_photo(
                chat_id=chat_id,
                photo=selected_image,
                caption=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                message_effect_id=selected_effect
            )
        except Exception as e:
            logger.error(f"Failed to send user settings with photo: {e}")
            # Fallback to text-only message
            await client.send_message(
                chat_id=chat_id,
                text=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                message_effect_id=selected_effect
            )

# Command to show user settings
@Bot.on_message(filters.command('user') & filters.private & admin)
async def user_settings(client: Client, message: Message):
    await show_user_settings(client, message.chat.id)

# Callback handler for user settings buttons
@Bot.on_callback_query(filters.regex(r"^user_"))
async def user_callback(client: Client, callback: CallbackQuery):
    data = callback.data
    chat_id = callback.message.chat.id
    message_id = callback.message.id

    if data == "user_ban":
        await db.set_temp_state(chat_id, "awaiting_ban_input")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Gɪᴠᴇ ᴍᴇ ᴛʜᴇ ᴜꜱᴇʀ ID(ꜱ) ᴛᴏ ʙᴀɴ.</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="user_back"),
                    InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="user_close")
                ]
            ]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("<blockquote><b>Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴜꜱᴇʀ ID(ꜱ).</b></blockquote>")

    elif data == "user_unban":
        await db.set_temp_state(chat_id, "awaiting_unban_input")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Gɪᴠᴇ ᴍᴇ ᴛʜᴇ ᴜꜱᴇʀ ID(ꜱ) ᴏʀ ᴛʏᴘᴇ 'all' ᴛᴏ ᴜɴʙᴀɴ ᴀʟʟ ᴜꜱᴇʀꜱ.</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="user_back"),
                    InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="user_close")
                ]
            ]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("<blockquote><b>Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴜꜱᴇʀ ID(ꜱ) ᴏʀ ᴛʏᴘᴇ '[<code>all</code>]'.</b></blockquote>")

    elif data == "user_list":
        user_ids = await db.full_userbase()
        if not user_ids:
            user_list = "<b><blockquote>❌ Nᴏ ᴜꜱᴇʀꜱ ꜰᴏᴜɴᴅ.</blockquote></b>"
        else:
            user_list = "\n".join(f"<b><blockquote>{idx + 1}. {user.first_name if (user := await client.get_users(uid)) else 'Unknown'} - <code>{uid}</code></blockquote></b>" 
                                for idx, uid in enumerate(user_ids))

        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="user_back"),
                InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="user_close")
            ]
        ])
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"<b>⚡ Cᴜʀʀᴇɴᴛ ᴜꜱᴇʀ ʟɪꜱᴛ:</b>\n\n{user_list}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("Sʜᴏᴡɪɴɢ ᴜꜱᴇʀ ʟɪꜱᴛ!")

    elif data == "user_banlist":
        banuser_ids = await db.get_ban_users()
        if not banuser_ids:
            result = "<b>✅ Nᴏ ᴜꜱᴇʀꜱ ɪɴ ᴛʜᴇ ʙᴀɴ Lɪꜱᴛ.</b>"
        else:
            result = "<b>🚫 Bᴀɴɴᴇᴅ Uꜱᴇʀꜱ:</b>\n\n"
            for uid in banuser_ids:
                try:
                    user = await client.get_users(uid)
                    user_link = f'<a href="tg://user?id={uid}">{user.first_name}</a>'
                    result += f"• {user_link} — <code>{uid}</code>\n"
                except:
                    result += f"• <code>{uid}</code> — <i>Cᴏᴜʟᴅ ɴᴏᴛ ꜰᴇᴛᴄʜ ɴᴀᴍᴇ</i>\n"

        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="user_back"),
                InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="user_close")
            ]
        ])
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=result,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("Sʜᴏᴡɪɴɢ ʙᴀɴ ʟɪꜱᴛ!")

    elif data == "user_refresh":
        await show_user_settings(client, chat_id, message_id)
        await callback.answer("Sᴇᴛᴛɪɴɢꜱ ʀᴇꜰʀᴇꜱʜᴇᴅ!")

    elif data == "user_close":
        await db.set_temp_state(chat_id, "")
        await callback.message.delete()
        await callback.answer("Sᴇᴛᴛɪɴɢꜱ ᴄʟᴏꜱᴇᴅ!")

    elif data == "user_back":
        await db.set_temp_state(chat_id, "")
        await show_user_settings(client, chat_id, message_id)
        await callback.answer("Bᴀᴄᴋ ᴛᴏ ꜱᴇᴛᴛɪɴɢꜱ!")

# BAN-USER-SYSTEM
@Bot.on_message(filters.private & filters.command('ban') & admin)
async def add_banuser(client: Client, message: Message):        
    pro = await message.reply("⏳ <i>Pʀᴏᴄᴇꜱꜱɪɴɢ ʀᴇꜱᴜᴇꜱᴛ...</i>", quote=True)
    banuser_ids = await db.get_ban_users()
    banusers = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cʟᴏꜱᴇ", callback_data="close")]])

    if not banusers:
        return await pro.edit(
            "<b>❗ Yᴏᴜ ᴍᴜꜱᴛ ᴘʀᴏᴠɪᴅᴇ ᴜꜱᴇʀ IDs ᴛᴏ ʙᴀɴ.</b>\n\n"
            "<b>📌 Uꜱᴀɢᴇ:</b>\n"
            "<code>/ban [user_id]</code> — Bᴀɴ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ ᴜꜱᴇʀꜱ ʙʏ ID.",
            reply_markup=reply_markup
        )

    report, success_count = "", 0
    for uid in banusers:
        try:
            uid_int = int(uid)
        except:
            report += f"⚠️ Iɴᴠᴀʟɪᴅ ID: <code>{uid}</code>\n"
            continue

        if uid_int in await db.get_all_admins() or uid_int == OWNER_ID:
            report += f"⛔ Sᴋɪᴘᴘᴇᴅ ᴀᴅᴍɪɴ/ᴏᴡɴᴇʀ ID: <code>{uid_int}</code>\n"
            continue

        if uid_int in banuser_ids:
            report += f"⚠️ Aʟʀᴇᴀᴅʏ: <code>{uid_int}</code>\n"
            continue

        if len(str(uid_int)) == 10:
            await db.add_ban_user(uid_int)
            report += f"✅ Bᴀɴɴᴇᴅ: <code>{uid_int}</code>\n"
            success_count += 1
        else:
            report += f"⚠️ Iɴᴠᴀʟɪᴅ Tᴇʟᴇɢʀᴀᴍ ID ʟᴇɴɢᴛʜ: <code>{uid_int}</code>\n"

    if success_count:
        await pro.edit(f"<b>✅ Bᴀɴɴᴇᴅ Uꜱᴇʀꜱ Uᴘᴅᴀᴛᴇᴅ:</b>\n\n{report}", reply_markup=reply_markup)
    else:
        await pro.edit(f"<b>❌ Nᴏ ᴜꜱᴇʀꜱ ᴡᴇʀᴇ ʙᴀɴɴᴇᴅ.</b>\n\n{report}", reply_markup=reply_markup)

@Bot.on_message(filters.private & filters.command('unban') & admin)
async def delete_banuser(client: Client, message: Message):        
    pro = await message.reply("⏳ <i>Pʀᴏᴄᴇꜱꜱɪɴɢ ʀᴇꜱᴜᴇꜱᴛ...</i>", quote=True)
    banuser_ids = await db.get_ban_users()
    banusers = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cʟᴏꜱᴇ", callback_data="close")]])

    if not banusers:
        return await pro.edit(
            "<b>❗ Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴜꜱᴇʀ IDs ᴛᴏ ᴜɴʙᴀɴ.</b>\n\n"
            "<b>📌 Uꜱᴀɢᴇ:</b>\n"
            "<code>/unban [user_id]</code> — Uɴʙᴀɴ ꜱᴘᴇᴄɪғɪᴄ ᴜꜱᴇʀ(ꜱ)\n"
            "<code>/unban all</code> — Rᴇᴍᴏᴠᴇ ᴀʟʟ ʙᴀɴɴᴇᴅ ᴜꜱᴇʀꜱ",
            reply_markup=reply_markup
        )

    if banusers[0].lower() == "all":
        if not banuser_ids:
            return await pro.edit("<b>✅ Nᴏ ᴜꜱᴇʀꜱ ɪɴ ᴛʜᴇ ʙᴀɴ ʟɪꜱᴛ.</b>", reply_markup=reply_markup)
        for uid in banuser_ids:
            await db.del_ban_user(uid)
        listed = "\n".join([f"✅ Uɴʙᴀɴɴᴇᴅ: <code>{uid}</code>" for uid in banuser_ids])
        return await pro.edit(f"<b>🚫 Cʟᴇᴀʀᴇᴅ Bᴀɴ Lɪꜱᴛ:</b>\n\n{listed}", reply_markup=reply_markup)

    report = ""
    for uid in banusers:
        try:
            uid_int = int(uid)
        except:
            report += f"⚠️ Iɴᴠᴀʟɪᴅ ID: <code>{uid}</code>\n"
            continue

        if uid_int in banuser_ids:
            await db.del_ban_user(uid_int)
            report += f"✅ Uɴʙᴀɴɴᴇᴅ: <code>{uid_int}</code>\n"
        else:
            report += f"⚠️ Nᴏᴛ ɪɴ ʙᴀɴ ʟɪꜱᴛ: <code>{uid_int}</code>\n"

    await pro.edit(f"<b>🚫 Uɴʙᴀɴ Rᴇᴘᴏʀᴛ:</b>\n\n{report}", reply_markup=reply_markup)

@Bot.on_message(filters.private & filters.command('banlist') & admin)
async def get_banuser_list(client: Client, message: Message):        
    pro = await message.reply("⏳ <i>Fᴇᴛᴄʜɪɴɢ Bᴀɴ Lɪꜱᴛ...</i>", quote=True)
    banuser_ids = await db.get_ban_users()

    if not banuser_ids:
        return await pro.edit(
            "<b>✅ Nᴏ ᴜꜱᴇʀꜱ ɪɴ ᴛʜᴇ ʙᴀɴ Lɪꜱᴛ.</b>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="user_back"),
                    InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="user_close")
                ]
            ])
        )

    result = "<b>🚫 Bᴀɴɴᴇᴅ Uꜱᴇʀꜱ:</b>\n\n"
    for uid in banuser_ids:
        await message.reply_chat_action(ChatAction.TYPING)
        try:
            user = await client.get_users(uid)
            user_link = f'<a href="tg://user?id={uid}">{user.first_name}</a>'
            result += f"• {user_link} — <code>{uid}</code>\n"
        except:
            result += f"• <code>{uid}</code> — <i>Cᴏᴜʟᴅ ɴᴏᴛ ꜰᴇᴛᴄʜ ɴᴀᴍᴇ</i>\n"

    await pro.edit(
        result,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="user_back"),
                InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="user_close")
            ]
        ])
    )

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
