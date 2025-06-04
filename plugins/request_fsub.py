#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved
#

import asyncio
import os
import random
import sys
import time
import logging
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction, ChatMemberStatus, ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatMemberUpdated, ChatPermissions
from bot import Bot
from helper_func import *
from database.database import *
from config import OWNER_ID

# Set up logging for this module
logger = logging.getLogger(__name__)

# Define message effect IDs
MESSAGE_EFFECT_IDS = [
    5104841245755180586,  # 🔥
    5107584321108051014,  # 👍
    5044134455711629726,  # ❤️
    5046509860389126442,  # 🎉
    5104858069142078462,  # 👎
    5046589136895476101,  # 💩
]

# Function to show force-sub settings with channels list, buttons, image, and message effects
async def show_force_sub_settings(client: Client, chat_id: int, message_id: int = None):
    """Show the force-sub settings menu with channel list and controls."""
    settings_text = "<b>›› Request Fsub Settings:</b>\n\n"
    fsub_system_status = await db.get_fsub_system_status()
    status_text = "🟢 Enabled" if fsub_system_status else "🔴 Disabled"
    settings_text += f"<blockquote><b>⚡ Force-sub System Status: {status_text}</b></blockquote>\n\n"
    
    channels = await db.show_channels()
    if not channels:
        settings_text += "<blockquote><i>No channels configured yet. Use 𖤓 Add Channels 𖤓 to add a channel.</i></blockquote>"
    else:
        settings_text += "<blockquote><b>⚡ Force-sub Channels:</b></blockquote>\n"
        for ch_id in channels:
            try:
                chat = await client.get_chat(ch_id)
                link = await client.export_chat_invite_link(ch_id) if not chat.username else f"https://t.me/{chat.username}"
                mode = await db.get_channel_mode(ch_id)
                visibility = await db.get_channel_visibility(ch_id)
                settings_text += f"<blockquote><b><a href='{link}'>{chat.title}</a> - <code>{ch_id}</code> [{'🟢' if mode == 'on' else '🔴'} Mode, {'👁️' if visibility == 'show' else '🙈'} Visibility]</b></blockquote>\n"
            except Exception as e:
                logger.error(f"Failed to fetch chat {ch_id}: {e}")
                settings_text += f"<blockquote><b><code>{ch_id}</code> — <i>Unavailable</i></b></blockquote>\n"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Add Channels ", callback_data="fsub_add_channel"),
                InlineKeyboardButton(" Remove Channels •", callback_data="fsub_remove_channel")
            ],
            [
                InlineKeyboardButton("• Toggle Mode •", callback_data="fsub_toggle_mode"),
                InlineKeyboardButton("• Channels List •", callback_data="fsub_channels_list")
            ],
            [
                InlineKeyboardButton("• Single Off •", callback_data="fsub_single_off"),
                InlineKeyboardButton("• Fully Off •", callback_data="fsub_fully_off")
            ],
            [
                InlineKeyboardButton("• Refresh ", callback_data="fsub_refresh"),
                InlineKeyboardButton(" Close •", callback_data="fsub_close")
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
            logger.info("Edited message as text-only")
        except Exception as e:
            logger.error(f"Failed to edit message: {e}")
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
            logger.info(f"Sent photo message with image {selected_image} and effect {selected_effect}")
        except Exception as e:
            logger.error(f"Failed to send photo message with image {selected_image}: {e}")
            # Fallback to text-only message
            try:
                await client.send_message(
                    chat_id=chat_id,
                    text=settings_text,
                    reply_markup=buttons,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                    message_effect_id=selected_effect
                )
                logger.info(f"Sent text-only message with effect {selected_effect} as fallback")
            except Exception as e:
                logger.error(f"Failed to send text-only message with effect {selected_effect}: {e}")
                # Final fallback without effect
                await client.send_message(
                    chat_id=chat_id,
                    text=settings_text,
                    reply_markup=buttons,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                logger.info("Sent text-only message without effect as final fallback")

# Function to show the list of force-sub channels
async def show_channels_list(client: Client, chat_id: int, message_id: int = None):
    """Show the list of force-sub channels (like /listchanl)."""
    settings_text = "<b>›› Force-sub Channels List:</b>\n\n"
    channels = await db.show_channels()
    
    if not channels:
        settings_text += "<blockquote><i>No channels configured.</i></blockquote>"
    else:
        for ch_id in channels:
            try:
                chat = await client.get_chat(ch_id)
                link = await client.export_chat_invite_link(ch_id) if not chat.username else f"https://t.me/{chat.username}"
                settings_text += f"<blockquote><b><a href='{link}'>{chat.title}</a> - <code>{ch_id}</code></b></blockquote>\n"
            except Exception as e:
                logger.error(f"Failed to fetch chat {ch_id}: {e}")
                settings_text += f"<blockquote><b><code>{ch_id}</code> — <i>Unavailable</i></b></blockquote>\n"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Back •", callback_data="fsub_back"),
                InlineKeyboardButton("• Close •", callback_data="fsub_close")
            ]
        ]
    )

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
            logger.info("Edited channels list message")
        except Exception as e:
            logger.error(f"Failed to edit channels list message: {e}")
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
            logger.info(f"Sent channels list photo message with image {selected_image}")
        except Exception as e:
            logger.error(f"Failed to send channels list photo message: {e}")
            await client.send_message(
                chat_id=chat_id,
                text=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            logger.info("Sent channels list text-only message as fallback")

# Function to show single off menu
async def show_single_off_menu(client: Client, chat_id: int, message_id: int):
    """Show menu to toggle visibility for individual channels."""
    temp = await client.send_message(chat_id, "<b><i>Checking channels...</i></b>", parse_mode=ParseMode.HTML)
    channels = await db.show_channels()

    if not channels:
        await temp.edit("<blockquote><b>❌ No force-sub channels found.</b></blockquote>")
        return

    buttons = []
    for ch_id in channels:
        try:
            chat = await client.get_chat(ch_id)
            visibility = await db.get_channel_visibility(ch_id)
            status = "👁️ Show" if visibility == "show" else "🙈 Hide"
            buttons.append([InlineKeyboardButton(f"{status} | {chat.title}", callback_data=f"fsub_vis_{ch_id}")])
        except Exception as e:
            logger.error(f"Failed to fetch chat {ch_id}: {e}")
            buttons.append([InlineKeyboardButton(f"⚠️ {ch_id} (Unavailable)", callback_data=f"fsub_vis_{ch_id}")])

    buttons.append([InlineKeyboardButton("• Back •", callback_data="fsub_back")])

    await temp.edit(
        "<blockquote><b>⚡ Select a channel to toggle visibility (Show/Hide):</b></blockquote>",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.HTML
    )

# Function to show fully off menu
async def show_fully_off_menu(client: Client, chat_id: int, message_id: int = None):
    """Show menu to toggle the entire force-sub system (like /auto_delete)."""
    fsub_system_status = await db.get_fsub_system_status()
    status_text = "🟢 Enabled" if fsub_system_status else "🔴 Disabled"
    
    settings_text = (
        "<b>›› Force-sub System:</b>\n\n"
        f"<blockquote><b>⚡ Status: {status_text}</b></blockquote>\n"
        "<b>Toggle the system below:</b>"
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Disable ❌" if fsub_system_status else "• Enable ✅", callback_data="fsub_system_toggle"),
            ],
            [
                InlineKeyboardButton("• Refresh ", callback_data="fsub_system_refresh"),
                InlineKeyboardButton("• Back •", callback_data="fsub_back")
            ]
        ]
    )

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
            logger.info("Edited fully off menu message")
        except Exception as e:
            logger.error(f"Failed to edit fully off menu message: {e}")
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
            logger.info(f"Sent fully off menu photo message with image {selected_image}")
        except Exception as e:
            logger.error(f"Failed to send fully off menu photo message: {e}")
            await client.send_message(
                chat_id=chat_id,
                text=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            logger.info("Sent fully off menu text-only message as fallback")

@Bot.on_message(filters.command('forcesub') & filters.private & admin)
async def force_sub_settings(client: Client, message: Message):
    """Handle /forcesub command to show settings."""
    logger.info(f"Received /forcesub command from chat {message.chat.id}")
    await show_force_sub_settings(client, message.chat.id)

@Bot.on_callback_query(filters.regex(r"^fsub_"))
async def force_sub_callback(client: Client, callback: CallbackQuery):
    """Handle callback queries for force-sub settings."""
    data = callback.data
    chat_id = callback.message.chat.id
    message_id = callback.message.id

    logger.info(f"Received callback query with data: {data} in chat {chat_id}")

    if data == "fsub_add_channel":
        await db.set_temp_state(chat_id, "awaiting_add_channel_input")
        logger.info(f"Set state to 'awaiting_add_channel_input' for chat {chat_id}")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Give me the channel ID.</b>\n<b>Add only one channel at a time.</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("•Back•", callback_data="fsub_back"),
                    InlineKeyboardButton("•Close•", callback_data="fsub_close")
                ]
            ]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("Give me the channel ID.\nAdd only one channel at a time.")

    elif data == "fsub_remove_channel":
        await db.set_temp_state(chat_id, "awaiting_remove_channel_input")
        logger.info(f"Set state to 'awaiting_remove_channel_input' for chat {chat_id}")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Give me the channel ID or type '<code>all</code>' to remove all channels.</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("•Back•", callback_data="fsub_back"),
                    InlineKeyboardButton("•Close•", callback_data="fsub_close")
                ]
            ]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("Please provide the channel ID or type 'all'.")

    elif data == "fsub_toggle_mode":
        temp = await callback.message.reply("<b><i>Wait a sec...</i></b>", quote=True)
        channels = await db.show_channels()

        if not channels:
            await temp.edit("<blockquote><b>❌ No force-sub channels found.</b></blockquote>")
            await callback.answer()
            return

        buttons = []
        for ch_id in channels:
            try:
                chat = await client.get_chat(ch_id)
                mode = await db.get_channel_mode(ch_id)
                status = "🟢" if mode == "on" else "🔴"
                title = f"{status} {chat.title}"
                buttons.append([InlineKeyboardButton(title, callback_data=f"rfs_ch_{ch_id}")])
            except Exception as e:
                logger.error(f"Failed to fetch chat {ch_id}: {e}")
                buttons.append([InlineKeyboardButton(f"⚠️ {ch_id} (Unavailable)", callback_data=f"rfs_ch_{ch_id}")])

        buttons.append([InlineKeyboardButton("Close ✖️", callback_data="close")])

        await temp.edit(
            "<blockquote><b>⚡ Select a channel to toggle force-sub mode:</b></blockquote>",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        await callback.answer()

    elif data == "fsub_channels_list":
        await show_channels_list(client, chat_id, message_id)
        await callback.answer("Channels list displayed!")

    elif data == "fsub_single_off":
        await show_single_off_menu(client, chat_id, message_id)
        await callback.answer("Select a channel to toggle visibility!")

    elif data == "fsub_fully_off":
        await show_fully_off_menu(client, chat_id, message_id)
        await callback.answer("Force-sub system settings displayed!")

    elif data == "fsub_system_toggle":
        current_status = await db.get_fsub_system_status()
        await db.set_fsub_system_status(not current_status)
        await show_fully_off_menu(client, chat_id, message_id)
        await callback.answer(f"Force-sub system {'enabled' if not current_status else 'disabled'}!")

    elif data == "fsub_system_refresh":
        await show_fully_off_menu(client, chat_id, message_id)
        await callback.answer("Settings refreshed!")

    elif data == "fsub_refresh":
        await show_force_sub_settings(client, chat_id, callback.message.id)
        await callback.answer("Settings refreshed!")

    elif data == "fsub_close":
        await db.set_temp_state(chat_id, "")
        await callback.message.delete()
        await callback.answer("Settings closed!")

    elif data == "fsub_back":
        await db.set_temp_state(chat_id, "")
        await show_force_sub_settings(client, chat_id, message_id)
        await callback.answer("Back to settings!")

    elif data == "fsub_cancel":
        await db.set_temp_state(chat_id, "")
        await show_force_sub_settings(client, chat_id, message_id)
        await callback.answer("Action cancelled!")

# Callback for toggling channel visibility
@Bot.on_callback_query(filters.regex(r"^fsub_vis_"))
async def toggle_channel_visibility(client: Client, callback: CallbackQuery):
    """Handle callback to toggle visibility for a specific channel."""
    ch_id = int(callback.data.split("_")[-1])
    logger.info(f"Toggling visibility for channel {ch_id} by user {callback.from_user.id}")

    try:
        current_visibility = await db.get_channel_visibility(ch_id)
        new_visibility = "hide" if current_visibility == "show" else "show"
        await db.set_channel_visibility(ch_id, new_visibility)
        
        chat = await client.get_chat(ch_id)
        status = "👁️ Shown" if new_visibility == "show" else "🙈 Hidden"
        link = await client.export_chat_invite_link(ch_id) if not chat.username else f"https://t.me/{chat.username}"
        await callback.message.edit_text(
            f"<blockquote><b>✅ Visibility toggled:</b></blockquote>\n"
            f"<b>Name:</b> <a href='{link}'>{chat.title}</a>\n"
            f"<b>ID:</b> <code>{ch_id}</code>\n"
            f"<b>Visibility:</b> {status}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("• Back •", callback_data="fsub_single_off")]]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer(f"Channel {chat.title} is now {status.lower()}")
    except Exception as e:
        logger.error(f"Failed to toggle visibility for channel {ch_id}: {e}")
        await callback.message.edit_text(
            f"<blockquote><b>❌ Failed to toggle visibility for channel {ch_id}</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("• Back •", callback_data="fsub_single_off")]]),
            parse_mode=ParseMode.HTML
        )
        await callback.answer("Error occurred!")

# Modified filter to avoid conflict with link_generator.py
async def fsub_state_filter(_, __, message: Message):
    """Filter to ensure messages are processed only for force-sub related states."""
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    logger.info(f"Checking fsub_state_filter for chat {chat_id}: state={state}, message_text={message.text}")
    if state not in ["awaiting_add_channel_input", "awaiting_remove_channel_input"]:
        logger.info(f"State {state} not relevant for fsub_state_filter in chat {chat_id}")
        return False
    if not message.text:
        logger.info(f"No message text provided in chat {chat_id}")
        return False
    # Only process channel ID or 'all' inputs
    is_valid_input = message.text.lower() == "all" or (message.text.startswith("-") and message.text[1:].isdigit())
    logger.info(f"Input validation for chat {chat_id}: is_valid_input={is_valid_input}")
    return is_valid_input

@Bot.on_message(filters.private & admin & filters.create(fsub_state_filter), group=1)
async def handle_channel_input(client: Client, message: Message):
    """Handle channel ID input for force-sub settings."""
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    logger.info(f"Handling input: {message.text} for state: {state} in chat {chat_id}")

    try:
        if state == "awaiting_add_channel_input":
            channel_id = int(message.text)
            all_channels = await db.show_channels()
            channel_ids_only = [cid if isinstance(cid, int) else cid[0] for cid in all_channels]
            if channel_id in channel_ids_only:
                await message.reply(f"<blockquote><b>Channel already exists:</b></blockquote>\n <blockquote><code>{channel_id}</code></blockquote>")
                await db.set_temp_state(chat_id, "")
                await show_force_sub_settings(client, chat_id)
                return

            chat = await client.get_chat(channel_id)

            if chat.type != ChatType.CHANNEL:
                await message.reply("<b>❌ Only public or private channels are allowed.</b>")
                await db.set_temp_state(chat_id, "")
                await show_force_sub_settings(client, chat_id)
                return

            member = await client.get_chat_member(chat.id, "me")
            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                await message.reply("<b>❌ Bot must be an admin in that channel.</b>")
                await db.set_temp_state(chat_id, "")
                await show_force_sub_settings(client, chat_id)
                return

            link = await client.export_chat_invite_link(chat.id) if not chat.username else f"https://t.me/{chat.username}"
            
            await db.add_channel(channel_id)
            await message.reply(
                f"<blockquote><b>✅ Force-sub Channel added successfully!</b></blockquote>\n\n"
                f"<blockquote><b>Name:</b> <a href='{link}'>{chat.title}</a></blockquote>\n"
                f"<blockquote><b>ID: <code>{channel_id}</code></b></blockquote>",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            await db.set_temp_state(chat_id, "")
            await show_force_sub_settings(client, chat_id)

        elif state == "awaiting_remove_channel_input":
            all_channels = await db.show_channels()
            if message.text.lower() == "all":
                if not all_channels:
                    await message.reply("<blockquote><b>❌ No force-sub channels found.</b></blockquote>")
                    await db.set_temp_state(chat_id, "")
                    await show_force_sub_settings(client, chat_id)
                    return
                for ch_id in all_channels:
                    await db.rem_channel(ch_id)
                await message.reply("<blockquote><b>✅ All force-sub channels removed.</b></blockquote>")
            else:
                ch_id = int(message.text)
                if ch_id in all_channels:
                    await db.rem_channel(ch_id)
                    await message.reply(f"<blockquote><b>✅ Channel removed:</b></blockquote>\n <blockquote><code>{ch_id}</code></blockquote>")
                else:
                    await message.reply(f"<blockquote><b>❌ Channel not found:</b></blockquote>\n <blockquote><code>{ch_id}</code></blockquote>")
            await db.set_temp_state(chat_id, "")
            await show_force_sub_settings(client, chat_id)

    except ValueError:
        logger.error(f"Invalid input received: {message.text}")
        await message.reply("<blockquote><b>❌ Invalid channel ID!</b></blockquote>")
        await db.set_temp_state(chat_id, "")
        await show_force_sub_settings(client, chat_id)
    except Exception as e:
        logger.error(f"Failed to process channel input {message.text}: {e}")
        await message.reply(
            f"<blockquote><b>❌ Failed to process channel:</b></blockquote>\n<code>{message.text}</code>\n\n<i>{e}</i>",
            parse_mode=ParseMode.HTML
        )
        await db.set_temp_state(chat_id, "")
        await show_force_sub_settings(client, chat_id)

@Bot.on_message(filters.command('fsub_mode') & filters.private & admin)
async def change_force_sub_mode(client: Client, message: Message):
    """Handle /fsub_mode command to toggle force-sub mode for channels."""
    temp = await message.reply("<b><i>Wait a sec...</i></b>", quote=True)
    channels = await db.show_channels()

    if not channels:
        await temp.edit("<blockquote><b>❌ No force-sub channels found.</b></blockquote>")
        return

    buttons = []
    for ch_id in channels:
        try:
            chat = await client.get_chat(ch_id)
            mode = await db.get_channel_mode(ch_id)
            status = "🟢" if mode == "on" else "🔴"
            title = f"{status} {chat.title}"
            buttons.append([InlineKeyboardButton(title, callback_data=f"rfs_ch_{ch_id}")])
        except Exception as e:
            logger.error(f"Failed to fetch chat {ch_id}: {e}")
            buttons.append([InlineKeyboardButton(f"⚠️ {ch_id} (Unavailable)", callback_data=f"rfs_ch_{ch_id}")])

    buttons.append([InlineKeyboardButton("Close ✖️", callback_data="close")])

    await temp.edit(
        "<blockquote><b>⚡ Select a channel to toggle force-sub mode:</b></blockquote>",
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Bot.on_callback_query(filters.regex(r"^rfs_ch_"))
async def toggle_channel_mode(client: Client, callback: CallbackQuery):
    """Handle callback to toggle force-sub mode for a specific channel."""
    ch_id = int(callback.data.split("_")[-1])
    logger.info(f"Toggling mode for channel {ch_id} by user {callback.from_user.id}")

    try:
        current_mode = await db.get_channel_mode(ch_id)
        new_mode = "off" if current_mode == "on" else "on"
        await db.set_channel_mode(ch_id, new_mode)
        
        chat = await client.get_chat(ch_id)
        status = "🟢" if new_mode == "on" else "🔴"
        await callback.message.edit_text(
            f"<blockquote><b>✅ Mode toggled for channel:</b></blockquote>\n\n"
            f"<blockquote><b>Name:</b> <a href='https://t.me/{chat.username}'>{chat.title}</a></blockquote>\n"
            f"<blockquote><b>ID:</b> <code>{ch_id}</code></blockquote>\n"
            f"<blockquote><b>Mode:</b> {status} {'Enabled' if new_mode == 'on' else 'Disabled'}</blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Back •", callback_data="fsub_toggle_mode")]
            ]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer(f"Force-sub {'enabled' if new_mode == 'on' else 'disabled'} for channel {ch_id}")
    except Exception as e:
        logger.error(f"Failed to toggle mode for channel {ch_id}: {e}")
        await callback.message.edit_text(
            f"<blockquote><b>❌ Failed to toggle mode for channel:</b></blockquote>\n<code>{ch_id}</code>\n\n<i>{e}</i>",
            parse_mode=ParseMode.HTML
        )
        await callback.answer()

@Bot.on_chat_member_updated()
async def handle_Chatmembers(client: Client, chat_member_updated: ChatMemberUpdated):    
    """Handle updates to chat members for force-sub channels."""
    chat_id = chat_member_updated.chat.id

    if await db.reqChannel_exist(chat_id):
        old_member = chat_member_updated.old_chat_member

        if not old_member:
            return

        if old_member.status == ChatMemberStatus.MEMBER:
            user_id = old_member.user.id

            if await db.req_user_exist(chat_id, user_id):
                await db.del_req_user(chat_id, user_id)
                logger.info(f"Removed user {user_id} from request list for channel {chat_id} after joining")

@Bot.on_chat_join_request()
async def handle_join_request(client: Client, chat_join_request):
    """Handle join requests for force-sub channels."""
    chat_id = chat_join_request.chat.id
    user_id = chat_join_request.from_user.id

    if await db.reqChannel_exist(chat_id):
        mode = await db.get_channel_mode(chat_id)
        if mode == "on" and not await db.req_user_exist(chat_id, user_id):
            await db.req_user(chat_id, user_id)
            logger.info(f"Added join request for user {user_id} in channel {chat_id}")
            try:
                await client.approve_chat_join_request(chat_id, user_id)
                logger.info(f"Approved join request for user {user_id} in channel {chat_id}")
            except Exception as e:
                logger.error(f"Failed to approve join request for user {user_id} in channel {chat_id}: {e}")

@Bot.on_message(filters.command('addchnl') & filters.private & admin)
async def add_force_sub(client: Client, message: Message):
    """Handle /addchnl command to add a force-sub channel."""
    temp = await message.reply("<b><i>Waiting...</i></b>", quote=True)
    args = message.text.split(maxsplit=1)

    if len(args) != 2:
        buttons = [[InlineKeyboardButton("Close", callback_data="close")]]
        await temp.edit(
            "<blockquote><b>Usage:</b></blockquote>\n<code>/addchnl -100XXXXXXXXXX</code>\n\n"
            "<b>Add only one channel at a time.</b>",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML
        )
        return

    try:
        channel_id = int(args[1])
        all_channels = await db.show_channels()
        channel_ids_only = [cid if isinstance(cid, int) else cid[0] for cid in all_channels]
        if channel_id in channel_ids_only:
            await temp.edit(f"<blockquote><b>Channel already exists:</b></blockquote>\n <blockquote><code>{channel_id}</code></blockquote>")
            return

        chat = await client.get_chat(channel_id)

        if chat.type != ChatType.CHANNEL:
            await temp.edit("<b>❌ Only public or private channels are allowed.</b>")
            return

        member = await client.get_chat_member(chat.id, "me")
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await temp.edit("<b>❌ Bot must be an admin in that channel.</b>")
            return

        link = await client.export_chat_invite_link(chat.id) if not chat.username else f"https://t.me/{chat.username}"
        
        await db.add_channel(channel_id)
        await temp.edit(
            f"<blockquote><b>✅ Force-sub Channel added successfully!</b></blockquote>\n\n"
            f"<blockquote><b>Name:</b> <a href='{link}'>{chat.title}</a></blockquote>\n"
            f"<blockquote><b>ID: <code>{channel_id}</code></b></blockquote>",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    except ValueError:
        await temp.edit("<blockquote><b>❌ Invalid channel ID!</b></blockquote>")
    except Exception as e:
        logger.error(f"Failed to add channel {args[1]}: {e}")
        await temp.edit(f"<blockquote><b>❌ Failed to add channel:</b></blockquote>\n<code>{args[1]}</code>\n\n<i>{e}</i>", parse_mode=ParseMode.HTML)

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved
#
