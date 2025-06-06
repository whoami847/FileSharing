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
import asyncio
from functools import wraps
from config import OWNER_ID, START_PIC, RANDOM_IMAGES
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant, PeerIdInvalid
from database.database import db

logger = logging.getLogger(__name__)

def admin(func):
    """Decorator to check if the user is an admin."""
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        user_id = message.from_user.id if message.from_user else None
        if not user_id:
            await message.reply("<b>❌ User ID not found!</b>")
            return
        if user_id == OWNER_ID or await db.admin_exist(user_id):
            return await func(client, message, *args, **kwargs)
        else:
            await message.reply("<b>❌ You are not authorized to use this command!</b>")
    return wrapper

async def is_subscribed(client: Client, user_id: int) -> tuple[bool, list]:
    """
    Check if a user is subscribed to all required channels.
    Returns: (is_subscribed: bool, channels_not_subscribed: list)
    """
    logger.info(f"Checking subscription status for user {user_id}")
    
    # Skip force-sub check for OWNER_ID
    if user_id == OWNER_ID:
        logger.info(f"User {user_id} is OWNER_ID, skipping force-sub check")
        return True, []

    # Check if force-sub system is enabled
    settings = await db.get_settings()
    if not settings.get('FORCE_SUB_ENABLED', True):
        logger.info("Force-sub system is disabled globally")
        return True, []

    channels = await db.show_channels()
    if not channels:
        logger.info("No force-sub channels configured")
        return True, []

    not_subscribed = []
    
    for channel_id in channels:
        try:
            # Skip if channel's display_mode is False
            display_mode = await db.get_channel_display_mode(channel_id)
            if not display_mode:
                logger.info(f"Channel {channel_id} has display_mode off, skipping")
                continue
                
            # Validate channel ID
            if not isinstance(channel_id, int):
                logger.warning(f"Invalid channel ID {channel_id}, skipping")
                continue
                
            # Check if bot can access the channel
            try:
                chat = await client.get_chat(channel_id)
            except PeerIdInvalid:
                logger.error(f"Invalid peer ID for channel {channel_id}")
                continue
                
            # Check if user is a member
            try:
                member = await client.get_chat_member(channel_id, user_id)
                if member.status in ['member', 'administrator', 'creator']:
                    logger.info(f"User {user_id} is subscribed to channel {channel_id}")
                    continue
                else:
                    logger.info(f"User {user_id} is not subscribed to channel {channel_id}")
                    not_subscribed.append((channel_id, chat.title, chat.username))
            except UserNotParticipant:
                logger.info(f"User {user_id} is not a participant in channel {channel_id}")
                not_subscribed.append((channel_id, chat.title, chat.username))
            except Exception as e:
                logger.error(f"Error checking subscription for channel {channel_id}: {e}")
                continue
                
        except Exception as e:
            logger.error(f"Unexpected error for channel {channel_id}: {e}")
            continue

    return (len(not_subscribed) == 0, not_subscribed)

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved
#
