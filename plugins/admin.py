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
from pyrogram.enums import ParseMode, ChatAction, ChatMemberStatus, ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatMemberUpdated, ChatPermissions, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, InviteHashEmpty, ChatAdminRequired, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
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
                settings_text += f"<blockquote><b>{idx}. <a href='tg://user?id={user_id}'>{name}</a> - <code>{user_id}</code></b></blockquote>\n"
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

# Function to show admin settings with admin list, buttons, and message effects
async def show_admin_settings(client: Client, chat_id: int, message_id: int = None, is_owner: bool = False):
    settings_text = "<b>›› Aᴅᴍɪɴ Sᴇᴛᴛɪɴɢꜱ:</b>\n\n"
    admin_ids = await db.get_all_admins()

    if not admin_ids:
        settings_text += "<i>Nᴏ ᴀᴅᴍɪɴꜱ ᴄᴏɴғɪɢᴜʀᴇᴅ ʏᴇᴛ. Uꜱᴇ 'ᴀᴅᴅ ᴀᴅᴍɪɴ' ᴛᴏ ᴀᴅᴅ ᴀ/ᴍᴜʟᴛɪᴘʟᴇ ᴀᴅᴍɪɴ.</i>"
    else:
        settings_text += "<blockquote><b>⚡ Cᴜʀʀᴇɴᴛ Aᴅᴍɪɴꜱ:</b></blockquote>\n\n"
        for idx, admin_id in enumerate(admin_ids[:5], 1):  # Show up to 5 admins
            try:
                admin = await client.get_users(admin_id)
                name = admin.first_name if admin.first_name else "Unknown"
                settings_text += f"<blockquote><b>{idx}. <a href='tg://user?id={admin_id}'>{name}</a> - <code>{admin_id}</code></b></blockquote>\n"
            except Exception as e:
                settings_text += f"<blockquote><b>{idx}. Unknown - <code>{admin_id}</code></b></blockquote>\n"
        if len(admin_ids) > 5:
            settings_text += f"<blockquote><i>...and {len(admin_ids) - 5} more.</i></blockquote>\n"

    # Show different buttons for owner vs non-owner
    if is_owner:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("• Aᴅᴅ Aᴅᴍɪɴ", callback_data="admin_add"),
                    InlineKeyboardButton("Rᴇᴍᴏᴠᴇ Aᴅᴍɪɴ •", callback_data="admin_remove")
                ],
                [
                    InlineKeyboardButton("Aᴅᴍɪɴ Lɪꜱᴛ", callback_data="admin_list"),
                    InlineKeyboardButton("• Rᴇꜰʀᴇꜱʜ •", callback_data="admin_refresh")
                ],
                [
                    InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="admin_close")
                ]
            ]
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Aᴅᴍɪɴ Lɪꜱᴛ", callback_data="admin_list"),
                    InlineKeyboardButton("• Rᴇꜰʀᴇꜱʜ •", callback_data="admin_refresh")
                ],
                [
                    InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="admin_close")
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
            logger.error(f"Failed to edit admin settings message: {e}")
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
            logger.error(f"Failed to send admin settings with photo: {e}")
            # Fallback to text-only message
            await client.send_message(
                chat_id=chat_id,
                text=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                message_effect_id=selected_effect
            )

# Command to show admin settings (accessible to all users)
@Bot.on_message(filters.command('admin') & filters.private)
async def admin_settings(client: Client, message: Message):
    is_owner = message.from_user.id == OWNER_ID
    await show_admin_settings(client, message.chat.id, is_owner=is_owner)

# Callback handler for admin settings buttons
@Bot.on_callback_query(filters.regex(r"^admin_"))
async def admin_callback(client: Client, callback: CallbackQuery):
    data = callback.data
    chat_id = callback.message.chat.id
    message_id = callback.message.id
    user_id = callback.from_user.id
    is_owner = user_id == OWNER_ID

    if data == "admin_add" and is_owner:
        await db.set_temp_state(chat_id, "awaiting_add_admin_input")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Gɪᴠᴇ ᴍᴇ ᴛʜᴇ ᴀᴅᴍɪɴ ID(ꜱ).</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="admin_back"),
                    InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="admin_close")
                ]
            ]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("<blockquote><b>Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴀᴅᴍɪɴ ID(ꜱ).</b></blockquote>")

    elif data == "admin_remove" and is_owner:
        await db.set_temp_state(chat_id, "awaiting_remove_admin_input")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Gɪᴠᴇ ᴍᴇ ᴛʜᴇ ᴀᴅᴍɪɴ ID(ꜱ) ᴏʀ ᴛʏᴘᴇ 'all' ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴀᴅᴍɪɴꜱ.</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="admin_back"),
                    InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="admin_close")
                ]
            ]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("<blockquote><b>Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴀᴅᴍɪɴ ID(ꜱ) ᴏʀ ᴛʏᴘᴇ '[<code>all</code>]'.</b></blockquote>")

    elif data == "admin_list":
        admin_ids = await db.get_all_admins()
        if not admin_ids:
            admin_list = "<b><blockquote>❌ Nᴏ ᴀᴅᴍɪɴꜱ ꜰᴏᴜɴᴅ.</blockquote></b>"
        else:
            admin_list = ""
            for admin_id in admin_ids:
                try:
                    admin = await client.get_users(admin_id)
                    name = admin.first_name if admin.first_name else "Unknown"
                    admin_list += f"<b><blockquote><a href='tg://user?id={admin_id}'>{name}</a> - <code>{admin_id}</code></blockquote></b>\n"
                except Exception as e:
                    admin_list += f"<b><blockquote>Unknown - <code>{admin_id}</code></blockquote></b>\n"

        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="admin_back"),
                InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="admin_close")
            ]
        ])
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"<b>⚡ Cᴜʀʀᴇɴᴛ ᴀᴅᴍɪɴ ʟɪꜱᴛ:</b>\n\n{admin_list}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("Sʜᴏᴡɪɴɢ ᴀᴅᴍɪɴ ʟɪꜱᴛ!")

    elif data == "admin_refresh":
        await show_admin_settings(client, chat_id, message_id, is_owner=is_owner)
        await callback.answer("Sᴇᴛᴛɪɴɢꜱ ʀᴇꜰʀᴇꜱʜᴇᴅ!")

    elif data == "admin_close":
        await db.set_temp_state(chat_id, "")
        await callback.message.delete()
        await callback.answer("Sᴇᴛᴛɪɴɢꜱ ᴄʟᴏꜱᴇᴅ!")

    elif data == "admin_back":
        await db.set_temp_state(chat_id, "")
        await show_admin_settings(client, chat_id, message_id, is_owner=is_owner)
        await callback.answer("Bᴀᴄᴋ ᴛᴏ ꜱᴇᴛᴛɪɴɢꜱ!")

    elif data in ["admin_add", "admin_remove"] and not is_owner:
        await callback.answer("🚫 Only the owner can perform this action!", show_alert=True)

# Callback handler for user settings buttons
@Bot.on_callback_query(filters.regex(r"^user_") & admin)
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
        if not user_ids or not isinstance(user_ids, (list, tuple)):
            user_list = "<b><blockquote>❌ Nᴏ ᴜꜱᴇʀꜱ ꜰᴏᴜɴᴅ.</blockquote></b>"
        else:
            user_list = ""
            for idx, uid in enumerate(user_ids):
                try:
                    user = await client.get_users(uid)
                    name = user.first_name if user.first_name else "Unknown"
                    user_list += f"<b><blockquote>{idx + 1}. <a href='tg://user?id={uid}'>{name}</a> - <code>{uid}</code></blockquote></b>\n"
                except Exception as e:
                    user_list += f"<b><blockquote>{idx + 1}. Unknown - <code>{uid}</code></blockquote></b>\n"

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

# Handle admin input for adding/removing admins and banning/unbanning users
@Bot.on_message(filters.private & filters.regex(r"^-?\d+$|^all$") & filters.user(OWNER_ID))
async def handle_admin_input(client: Client, message: Message):
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC

    try:
        if state == "awaiting_add_admin_input":
            admin_ids = message.text.split()
            pro = await message.reply("<b><i>Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</i></b>", quote=True)
            check = 0
            existing_admins = await db.get_all_admins()
            admin_list = ""

            for id in admin_ids:
                try:
                    id = int(id)
                except:
                    admin_list += f"<blockquote><b>Iɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"
                    continue

                if id in existing_admins:
                    admin_list += f"<blockquote><b>Iᴅ <code>{id}</code> ᴀʟʀᴇᴀᴅʏ ᴇхɪꜱᴛꜱ.</b></blockquote>\n"
                    continue

                id = str(id)
                if id.isdigit() and len(id) == 10:
                    admin_list += f"<b><blockquote>(Iᴅ: <code>{id}</code>) ᴀᴅᴅᴇᴅ.</blockquote></b>\n"
                    check += 1
                else:
                    admin_list += f"<blockquote><b>Iɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"

            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="admin_close")]])

            if check == len(admin_ids):
                for id in admin_ids:
                    await db.add_admin(int(id))
                await pro.edit(f"<b>✅ Aᴅᴍɪɴ(ꜱ) ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ:</b>\n\n{admin_list}", reply_markup=reply_markup)
            else:
                await pro.edit(
                    f"<b>❌ Sᴏᴍᴇ ᴇʀʀᴏʀꜱ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴀᴅᴅɪɴɢ ᴀᴅᴍɪɴꜱ:</b>\n\n{admin_list.strip()}\n\n"
                    "<b><i>Pʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.</i></b>",
                    reply_markup=reply_markup
                )
            await db.set_temp_state(chat_id, "")
            await show_admin_settings(client, chat_id, is_owner=True)

        elif state == "awaiting_remove_admin_input":
            admin_ids = await db.get_all_admins()
            if message.text.lower() == "all":
                if not admin_ids:
                    await message.reply("<blockquote><b>❌ Nᴏ ᴀᴅᴍɪɴꜱ ꜰᴏᴜɴᴅ.</b></blockquote>")
                    return
                for admin_id in admin_ids:
                    await db.del_admin(admin_id)
                await message.reply("<blockquote><b>✅ Aʟʟ ᴀᴅᴍɪɴꜱ ʀᴇᴍᴏᴠᴇᴅ.</b></blockquote>")
            else:
                try:
                    id = int(message.text)
                    if id in admin_ids:
                        await db.del_admin(id)
                        await message.reply(f"<blockquote><b>✅ Aᴅᴍɪɴ ʀᴇᴍᴏᴠᴇᴅ:</b></blockquote>\n <code>{id}</code>")
                    else:
                        await message.reply(f"<blockquote><b>❌ Aᴅᴍɪɴ ɴᴏᴛ ꜰᴏᴜɴᴅ:</b></blockquote>\n <code>{id}</code>")
                except ValueError:
                    await message.reply("<blockquote><b>Uꜱᴀɢᴇ:</b></blockquote>\n <code>/deladmin <admin_id | all</code>")
                except Exception as e:
                    logger.error(f"Error removing admin {message.text}: {e}")
                    await message.reply(f"<blockquote><b>❌ Eʀʀᴏʀ:</b></blockquote>\n <code>{e}</code>")
            await db.set_temp_state(chat_id, "")
            await show_admin_settings(client, chat_id, is_owner=True)

        elif state == "awaiting_ban_input":
            banuser_ids = await db.get_ban_users()
            banusers = message.text.split()
            pro = await message.reply("<b><i>Pʀᴏᴄᴇꜱꜱɪɴɢ ʀᴇꜱᴜᴇꜱᴛ...</i></b>", quote=True)
            report, success_count = "", 0

            for uid in banusers:
                try:
                    uid_int = int(uid)
                except:
                    report += f"<blockquote><b>⚠️ Iɴᴠᴀʟɪᴅ ID: <code>{uid}</code></b></blockquote>\n"
                    continue

                if uid_int in await db.get_all_admins() or uid_int == OWNER_ID:
                    report += f"<blockquote><b>⛔ Sᴋɪᴘᴘᴇᴅ ᴀᴅᴍɪɴ/ᴏᴡɴᴇʀ ID: <code>{uid_int}</code></b></blockquote>\n"
                    continue

                if uid_int in banuser_ids:
                    report += f"<blockquote><b>⚠️ Aʟʀᴇᴀᴅʯ: <code>{uid_int}</code></b></blockquote>\n"
                    continue

                if len(str(uid_int)) == 10:
                    await db.add_ban_user(uid_int)
                    report += f"<blockquote><b>✅ Bᴀɴɴᴇᴅ: <code>{uid_int}</code></b></blockquote>\n"
                    success_count += 1
                else:
                    report += f"<blockquote><b>⚠️ Iɴᴠᴀʟɪᴅ Tᴇʟᴇɢʀᴀᴍ ID ʟᴇɴɢᴛʜ: <code>{uid_int}</code></b></blockquote>\n"

            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="user_close")]])

            if success_count:
                await pro.edit(f"<b>✅ Bᴀɴɴᴇᴅ Uꜱᴇʀꜱ Uᴘᴅᴀᴛᴇᴅ:</b>\n\n{report}", reply_markup=reply_markup)
            else:
                await pro.edit(f"<b>❌ Nᴏ ᴜꜱᴇʀꜱ ᴡᴇʀᴇ ʙᴀɴɴᴇᴅ.</b>\n\n{report}", reply_markup=reply_markup)
            await db.set_temp_state(chat_id, "")
            await show_user_settings(client, chat_id)

        elif state == "awaiting_unban_input":
            banuser_ids = await db.get_ban_users()
            if message.text.lower() == "all":
                if not banuser_ids:
                    await message.reply("<blockquote><b>✅ Nᴏ ᴜꜱᴇʀꜱ ɪɴ ᴛʜᴇ ʙᴀɴ ʟɪꜱᴛ.</b></blockquote>")
                    return
                for uid in banuser_ids:
                    await db.del_ban_user(uid)
                listed = "\n".join([f"<blockquote><b>✅ Uɴʙᴀɴɴᴇᴅ: <code>{uid}</code></b></blockquote>" for uid in banuser_ids])
                await message.reply(f"<b>🚫 Cʟᴇᴀʀᴇᴅ Bᴀɴ Lɪꜱᴛ:</b>\n\n{listed}")
            else:
                try:
                    uid_int = int(message.text)
                    if uid_int in banuser_ids:
                        await db.del_ban_user(uid_int)
                        await message.reply(f"<blockquote><b>✅ Uɴʙᴀɴɴᴇᴅ:</b></blockquote>\n <code>{uid_int}</code>")
                    else:
                        await message.reply(f"<blockquote><b>⚠️ Nᴏᴛ ɪɴ ʙᴀɴ ʟɪꜱᴛ:</b></blockquote>\n <code>{uid_int}</code>")
                except ValueError:
                    await message.reply("<blockquote><b>Uꜱᴀɢᴇ:</b></blockquote>\n <code>/unban <user_id | all</code>")
                except Exception as e:
                    logger.error(f"Error unbanning user {message.text}: {e}")
                    await message.reply(f"<blockquote><b>❌ Eʀʀᴏʀ:</b></blockquote>\n <code>{e}</code>")
            await db.set_temp_state(chat_id, "")
            await show_user_settings(client, chat_id)

    except Exception as e:
        logger.error(f"Failed to process input {message.text}: {e}")
        await message.reply(
            f"<blockquote><b>❌ Fᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇꜱꜱ ɪɴᴘᴜᴛ:</b></blockquote>\n<code>{message.text}</code>\n\n<i>{e}</i>",
            parse_mode=ParseMode.HTML
        )
        await db.set_temp_state(chat_id, "")
        if state in ["awaiting_add_admin_input", "awaiting_remove_admin_input"]:
            await show_admin_settings(client, chat_id, is_owner=True)
        elif state in ["awaiting_ban_input", "awaiting_unban_input"]:
            await show_user_settings(client, chat_id)

# Commands for adding admins by owner
@Bot.on_message(filters.command('add_admin') & filters.private & filters.user(OWNER_ID))
async def add_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</i></b>", quote=True)
    check = 0
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="admin_close")]])

    if not admins:
        return await pro.edit(
            "<b>Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴜꜱᴇʀ ɪᴅ(ꜱ) ᴛᴏ ᴀᴅᴅ ᴀꜱ ᴀᴅᴍɪɴ.</b>\n\n"
            "<b>Uꜱᴀɢᴇ:</b>\n"
            "<code>/add_admin [user_id]</code> — Aᴅᴅ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ ᴜꜱᴇʀ ɪᴅꜱ\n\n"
            "<b>Eхᴀᴍᴘʟᴇ:</b>\n"
            "<code>/add_admin 1234567890 9876543210</code>",
            reply_markup=reply_markup
        )

    admin_list = ""
    for id in admins:
        try:
            id = int(id)
        except:
            admin_list += f"<blockquote><b>Iɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"
            continue

        if id in admin_ids:
            admin_list += f"<blockquote><b>Iᴅ <code>{id}</code> ᴀʟʀᴇᴀᴅʯ ᴇхɪꜱᴛꜱ.</b></blockquote>\n"
            continue

        id = str(id)
        if id.isdigit() and len(id) == 10:
            admin_list += f"<b><blockquote>(Iᴅ: <code>{id}</code>) ᴀᴅᴅᴇᴅ.</blockquote></b>\n"
            check += 1
        else:
            admin_list += f"<blockquote><b>Iɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"

    if check == len(admins):
        for id in admins:
            await db.add_admin(int(id))
        await pro.edit(f"<b>✅ Aᴅᴍɪɴ(ꜱ) ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʯ:</b>\n\n{admin_list}", reply_markup=reply_markup)
    else:
        await pro.edit(
            f"<b>❌ Sᴏᴍᴇ ᴇʀʀᴏʀꜱ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴀᴅᴅɪɴɢ ᴀᴅᴍɪɴꜱ:</b>\n\n{admin_list.strip()}\n\n"
            "<b><i>Pʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʯ ᴀɢᴀɪɴ.</i></b>",
            reply_markup=reply_markup
        )

@Bot.on_message(filters.command('deladmin') & filters.private & filters.user(OWNER_ID))
async def delete_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</i></b>", quote=True)
    admin_ids = await db.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="admin_close")]])

    if not admins:
        return await pro.edit(
            "<b>Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴠᴀʟɪᴅ ᴀᴅᴍɪɴ ɪᴅ(ꜱ) ᴛᴏ ʀᴇᴍᴏᴠᴇ.</b>\n\n"
            "<b>Uꜱᴀɢᴇ:</b>\n"
            "<code>/deladmin [user_id]</code> — Rᴇᴍᴏᴠᴇ ꜱᴘᴇᴄɪғɪᴄ ɪᴅꜱ\n"
            "<code>/deladmin all</code> — Rᴇᴍᴏᴠᴇ ᴀʟʟ ᴀᴅᴍɪɴꜱ",
            reply_markup=reply_markup
        )

    if len(admins) == 1 and admins[0].lower() == "all":
        if admin_ids:
            for id in admin_ids:
                await db.del_admin(id)
            ids = "\n".join(f"<blockquote><code>{admin}</code> ✅</blockquote>" for admin in admin_ids)
            return await pro.edit(f"<b>⛔ Aʟʟ ᴀᴅᴍɪɴ ɪᴅꜱ ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ:</b>\n{ids}", reply_markup=reply_markup)
        else:
            return await pro.edit("<b><blockquote>Nᴏ ᴀᴅᴍɪɴ ɪᴅꜱ ᴛᴏ ʀᴇᴍᴏᴠᴇ.</blockquote></b>", reply_markup=reply_markup)

    if admin_ids:
        passed = ''
        for admin_id in admins:
            try:
                id = int(admin_id)
            except:
                passed += f"<blockquote><b>Iɴᴠᴀʟɪᴅ ɪᴅ: <code>{admin_id}</code></b></blockquote>\n"
                continue

            if id in admin_ids:
                await db.del_admin(id)
                passed += f"<blockquote><code>{id}</code> ✅ Rᴇᴍᴏᴠᴇᴅ</blockquote>\n"
            else:
                passed += f"<blockquote><b>Iᴅ <code>{id}</code> ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ᴀᴅᴍɪɴ ʟɪꜱᴛ.</b></blockquote>\n"

        await pro.edit(f"<b>⛔ Aᴅᴍɪɴ ʀᴇᴍᴏᴠᴀʟ ʀᴇꜱᴜʟᴛ:</b>\n\n{passed}", reply_markup=reply_markup)
    else:
        await pro.edit("<b><blockquote>Nᴏ ᴀᴅᴍɪɴ ɪᴅꜱ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ.</blockquote></b>", reply_markup=reply_markup)

@Bot.on_message(filters.command('admins') & filters.private)
async def get_admins(client: Client, message: Message):
    pro = await message.reply("<b><i>Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</i></b>", quote=True)
    admin_ids = await db.get_all_admins()

    if not admin_ids:
        admin_list = "<b><blockquote>❌ Nᴏ ᴀᴅᴍɪɴꜱ ꜰᴏᴜɴᴅ.</blockquote></b>"
    else:
        admin_list = "\n".join(f"<b><blockquote>Iᴅ: <code>{id}</code></blockquote></b>" for id in admin_ids)

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="admin_back"),
            InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="admin_close")
        ]
    ])
    await pro.edit(f"<b>⚡ Cᴜʀʳᴇɴᴛ ᴀᴅᴍɪɴ ʟɪꜱᴛ:</b>\n\n{admin_list}", reply_markup=reply_markup)

# BAN-USER-SYSTEM
@Bot.on_message(filters.private & filters.command('ban') & admin)
async def add_banuser(client: Client, message: Message):        
    pro = await message.reply("⏳ <i>Pʀᴏᴄᴇꜱꜱɪɴɢ ʀᴇꜱᴜᴇꜱᴛ...</i>", quote=True)
    banuser_ids = await db.get_ban_users()
    banusers = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cʟᴏꜱᴇ", callback_data="user_close")]])

    if not banusers:
        return await pro.edit(
            "<b>❗ Yᴏᴜ ᴍᴜꜱᴛ ᴘʀᴏᴠɪᴅᴇ ᴜꜱᴇʀ IDs ᴛᴏ ʙᴀɴ.</b>\n\n"
            "<b>📌 Uꜱᴀɢᴇ:</b>\n"
            "<code>/ban [user_id]</code> — Bᴀɴ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ ᴜꜱᴇʀꜱ ʙʯ ID.",
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
            report += f"⚠️ Aʟʳᴇᴀᴅʯ: <code>{uid_int}</code>\n"
            continue

        if len(str(uid_int)) == 10:
            await db.add_ban_user(uid_int)
            report += f"✅ Bᴀɴɴᴇᴅ: <code>{uid_int}</code>\n"
            success_count += 1
        else:
            report += f"⚠️ Iɴᴠᴀʟɪᴅ Tᴇʟᴇɢʳᴀᴍ ID ʟᴇɴɢᴛʜ: <code>{uid_int}</code>\n"

    if success_count:
        await pro.edit(f"<b>✅ Bᴀɴɴᴇᴅ Uꜱᴇʳꜱ Uᴘᴅᴀᴛᴇᴅ:</b>\n\n{report}", reply_markup=reply_markup)
    else:
        await pro.edit(f"<b>❌ Nᴏ ᴜꜱᴇʳꜱ ᴡᴇʳᴇ ʙᴀɴɴᴇᴅ.</b>\n\n{report}", reply_markup=reply_markup)

@Bot.on_message(filters.private & filters.command('unban') & admin)
async def delete_banuser(client: Client, message: Message):        
    pro = await message.reply("⏳ <i>Pʳᴏᴄᴇꜱꜱɪɴɢ ʳᴇꜱᴜᴇꜱᴛ...</i>", quote=True)
    banuser_ids = await db.get_ban_users()
    banusers = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cʟᴏꜱᴇ", callback_data="user_close")]])

    if not banusers:
        return await pro.edit(
            "<b>❗ Pʟᴇᴀꜱᴇ ᴘʳᴏᴠɪᴅᴇ ᴜꜱᴇʳ IDs ᴛᴏ ᴜɴʙᴀɴ.</b>\n\n"
            "<b>📌 Uꜱᴀɢᴇ:</b>\n"
            "<code>/unban [user_id]</code> — Uɴʙᴀɴ ꜱᴘᴇᴄɪғɪᴄ ᴜꜱᴇʳ(ꜱ)\n"
            "<code>/unban all</code> — Rᴇᴍᴏᴠᴇ ᴀʟʟ ʙᴀɴɴᴇᴅ ᴜꜱᴇʳꜱ",
            reply_markup=reply_markup
        )

    if banusers[0].lower() == "all":
        if not banuser_ids:
            return await pro.edit("<b>✅ Nᴏ ᴜꜱᴇʳꜱ ɪɴ ᴛʜᴇ ʙᴀɴ ʟɪꜱᴛ.</b>", reply_markup=reply_markup)
        for uid in banuser_ids:
            await db.del_ban_user(uid)
        listed = "\n".join([f"✅ Uɴʙᴀɴɴᴇᴅ: <code>{uid}</code>" for uid in banuser_ids])
        return await pro.edit(f"<b>🚫 Cʟᴇᴀʳᴇᴅ Bᴀɴ Lɪꜱᴛ:</b>\n\n{listed}", reply_markup=reply_markup)

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

    await pro.edit(f"<b>🚫 Uɴʙᴀɴ Rᴇᴘᴏʳᴛ:</b>\n\n{report}", reply_markup=reply_markup)

@Bot.on_message(filters.private & filters.command('banlist') & admin)
async def get_banuser_list(client: Client, message: Message):        
    pro = await message.reply("⏳ <i>Fᴇᴛᴄʜɪɴɢ Bᴀɴ Lɪꜱᴛ...</i>", quote=True)
    banuser_ids = await db.get_ban_users()

    if not banuser_ids:
        return await pro.edit(
            "<b>✅ Nᴏ ᴜꜱᴇʳꜱ ɪɴ ᴛʜᴇ ʙᴀɴ Lɪꜱᴛ.</b>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Bᴀᴄᴋ •", callback_data="user_back"),
                    InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="user_close")
                ]
            ])
        )

    result = "<b>🚫 Bᴀɴɴᴇᴅ Uꜱᴇʳꜱ:</b>\n\n"
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

@Bot.on_message(filters.command('user') & filters.private & admin)
async def user_settings(client: Client, message: Message):
    await show_user_settings(client, message.chat.id)

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
