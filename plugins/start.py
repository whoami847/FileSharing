#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved
#

import random
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode
from bot import Bot
from config import OWNER_ID, START_PIC, RANDOM_IMAGES, MESSAGE_EFFECT_IDS
from database.database import db
from helper_func import is_subscribed

logger = logging.getLogger(__name__)

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command."""
    user_id = message.from_user.id
    logger.info(f"Received /start command from user {user_id}")

    # Check if user exists in database, add if not
    if not await db.present_user(user_id):
        await db.add_user(user_id)

    # Check subscription status
    subscribed, not_subscribed = await is_subscribed(client, user_id)

    if not subscribed:
        buttons = []
        text = "<b>⚠️ You must join the following channel(s) to use this bot:</b>\n\n"
        for ch_id, title, username in not_subscribed:
            try:
                link = f"https://t.me/{username}" if username else await client.export_chat_invite_link(ch_id)
                text += f"➤ <a href='{link}'>{title}</a> (<code>{ch_id}</code>)\n"
                buttons.append([InlineKeyboardButton(f"Join {title}", url=link)])
            except Exception as e:
                logger.error(f"Failed to generate link for channel {ch_id}: {e}")
                text += f"➤ {title} (<code>{ch_id}</code>) — <i>Unavailable</i>\n"

        buttons.append([InlineKeyboardButton("✅ I've Joined", callback_data="start_check")])
        await message.reply(
            text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            message_effect_id=random.choice(MESSAGE_EFFECT_IDS) if MESSAGE_EFFECT_IDS else None
        )
        return

    # User is subscribed, send welcome message
    selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC
    text = (
        f"<b>Hello {message.from_user.mention}!</b>\n\n"
        "<i>Welcome to the bot. Use the commands to get started.</i>"
    )
    try:
        await message.reply_photo(
            photo=selected_image,
            caption=text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📚 Help", callback_data="help")]
            ]),
            parse_mode=ParseMode.HTML,
            message_effect_id=random.choice(MESSAGE_EFFECT_IDS) if MESSAGE_EFFECT_IDS else None
        )
        logger.info(f"Sent welcome message to user {user_id} with image {selected_image}")
    except Exception as e:
        logger.error(f"Failed to send photo message to {user_id}: {e}")
        await message.reply(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📚 Help", callback_data="help")]
            ]),
            parse_mode=ParseMode.HTML,
            message_effect_id=random.choice(MESSAGE_EFFECT_IDS) if MESSAGE_EFFECT_IDS else None
        )
        logger.info(f"Sent text-only welcome message to user {user_id} as fallback")

@Bot.on_callback_query(filters.regex(r"^start_check"))
async def start_callback(client: Client, callback: CallbackQuery):
    """Handle callback for checking subscription status."""
    user_id = callback.from_user.id
    message = callback.message
    logger.info(f"Received start_check callback from user {user_id}")

    subscribed, not_subscribed = await is_subscribed(client, user_id)

    if not subscribed:
        text = "<b>⚠️ You still haven't joined all required channels:</b>\n\n"
        buttons = []
        for ch_id, title, username in not_subscribed:
            try:
                link = f"https://t.me/{username}" if username else await client.export_chat_invite_link(ch_id)
                text += f"➤ <a href='{link}'>{title}</a> (<code>{ch_id}</code>)\n"
                buttons.append([InlineKeyboardButton(f"Join {title}", url=link)])
            except Exception as e:
                logger.error(f"Failed to generate link for channel {ch_id}: {e}")
                text += f"➤ {title} (<code>{ch_id}</code>) — <i>Unavailable</i>\n"

        buttons.append([InlineKeyboardButton("✅ I've Joined", callback_data="start_check")])
        await message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("Please join all channels and try again!")
        return

    # User is subscribed, send welcome message
    selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC
    text = (
        f"<b>Hello {callback.from_user.mention}!</b>\n\n"
        "<i>Welcome to the bot. Use the commands to get started.</i>"
    )
    try:
        await message.edit_media(
            media=types.InputMediaPhoto(selected_image, caption=text, parse_mode=ParseMode.HTML),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📚 Help", callback_data="help")]
            ])
        )
        logger.info(f"Edited message to welcome user {user_id} with image {selected_image}")
    except Exception as e:
        logger.error(f"Failed to edit media for user {user_id}: {e}")
        await message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📚 Help", callback_data="help")]
            ]),
            parse_mode=ParseMode.HTML
        )
        logger.info(f"Edited message to text-only welcome for user {user_id} as fallback")

    await callback.answer("Welcome to the bot!")

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved
#
