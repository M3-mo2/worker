# bot_v2/bot/utils/decorators.py
# Contains reusable decorators for Telegram handlers.

import asyncio
from functools import wraps
from typing import TYPE_CHECKING, Callable, Awaitable, Any

from telethon import events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError

# Local Imports from bot_v2 core
from bot.core.config import settings
from bot.core.data_manager import load_admin_settings

if TYPE_CHECKING:
    from telethon import TelegramClient

# --- Decorators ---

def force_subscribe_required(func: Callable[[Any], Awaitable[Any]]) -> Callable[[Any], Awaitable[Any]]:
    """
    Decorator to enforce subscription to configured channels before executing a handler.
    Checks if the user is subscribed to all required channels configured in admin settings.
    """
    @wraps(func)
    async def wrapper(event: Any): # event can be NewMessage or CallbackQuery
        sender_id = event.sender_id
        # SUDO_USERS are always exempt
        if sender_id in settings.telegram.SUDO_USERS:
            return await func(event)

        admin_settings = load_admin_settings()
        force_channels = admin_settings.get("force_subscribe_channels", [])
        
        if not force_channels: # No channels configured, no enforcement needed
            return await func(event)

        not_joined = []
        for channel_data in force_channels:
            channel_id = channel_data["id"]
            try:
                # Convert to proper channel format if needed
                if isinstance(channel_id, int) and channel_id > 0 and not str(channel_id).startswith('-100'):
                    # This is likely a bare channel ID, convert it
                    channel_id = int(f"-100{channel_id}")
                
                # Use event.client which is the TelegramClient instance
                await event.client(GetParticipantRequest(channel=channel_id, participant=sender_id))
                await asyncio.sleep(0.1) # Small delay to avoid flooding API
            except UserNotParticipantError:
                not_joined.append(channel_data)
            except Exception as e:
                print(f"Error checking subscription for channel {channel_id}: {e}")
                # Assume not joined if there's an error (e.g., bot not in channel)
                not_joined.append(channel_data)

        if not not_joined: # User is subscribed to all required channels
            return await func(event)

        # --- NEW: Save Pending Referral if present ---
        # If user is NOT subscribed, we check if they came via a referral link
        try:
            if isinstance(event, events.NewMessage.Event) and event.message and event.message.message:
                txt = event.message.message
                if '/start' in txt and 'ref_' in txt:
                    parts = txt.split()
                    for p in parts:
                        if p.startswith('ref_'):
                            try:
                                referrer_id = int(p.split('_')[1])
                                if referrer_id != sender_id:
                                    from bot.utils.points import save_pending_referral
                                    save_pending_referral(sender_id, referrer_id)
                            except: pass
        except Exception as e:
            print(f"Error saving pending referral in decorator: {e}")
        # ---------------------------------------------

        # User is not subscribed to some channels, send a message to join
        buttons = []
        for channel_data in not_joined:
            try:
                link = channel_data.get('link', 'https://t.me') # Fallback link
                buttons.append([Button.url(channel_data['title'], link)])
            except Exception as e:
                print(f"Could not create button for {channel_data}: {e}")

        if not buttons: # If no valid buttons could be created, send a generic message
            if isinstance(event, events.CallbackQuery.Event):
                await event.answer("عذراً، يجب عليك الاشتراك في القنوات المطلوبة أولاً، لكنني لم أتمكن من جلب الروابط. يرجى إبلاغ المطور.", alert=True)
            else:
                await event.reply("عذراً، يجب عليك الاشتراك في القنوات المطلوبة أولاً، لكنني لم أتمكن من جلب الروابط. يرجى إبلاغ المطور.")
            return

        message = "**عذراً، عليك الاشتراك في القنوات التالية أولاً لاستخدام البوت ثم أرسل /start مجدداً:**"
        if isinstance(event, events.CallbackQuery.Event):
            await event.answer(message, alert=True) # Send as alert
            # Also edit the message to show the buttons
            await event.edit(message, buttons=buttons)
        else:
            await event.reply(message, buttons=buttons)
        
        raise events.StopPropagation # Stop further handler execution
    
    return wrapper


def maintenance_check(func: Callable[[Any], Awaitable[Any]]) -> Callable[[Any], Awaitable[Any]]:
    """
    Decorator to check if the bot is in maintenance mode (bot_status = False).
    SUDO_USERS and admins bypass this check.
    """
    @wraps(func)
    async def wrapper(event: Any):
        sender_id = event.sender_id
        # SUDO_USERS always bypass maintenance
        if sender_id in settings.telegram.SUDO_USERS:
            return await func(event)
        
        # Check admin status
        from bot.services.user_service import check_user_status
        if check_user_status(sender_id) == 'admin':
            return await func(event)
        
        admin_settings = load_admin_settings()
        if not admin_settings.get('bot_status', True):
            msg = "🔧 **البوت حالياً في وضع الصيانة.**\n\nنعتذر عن الإزعاج، سيعود البوت للعمل قريباً. شكراً لصبرك! 🙏"
            if isinstance(event, events.CallbackQuery.Event):
                await event.answer(msg, alert=True)
            else:
                await event.reply(msg)
            raise events.StopPropagation
        
        return await func(event)
    return wrapper


print("✅ Decorators module initialized.")
