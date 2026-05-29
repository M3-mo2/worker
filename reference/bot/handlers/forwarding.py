# bot_v2/bot/handlers/forwarding.py
# This module handles forwarding user messages to the bot owner.

from telethon import events
from typing import TYPE_CHECKING

# Local Imports
from bot.core.config import settings
from bot.core.data_manager import load_admin_settings
from bot.services.user_service import check_user_status

if TYPE_CHECKING:
    from telethon import TelegramClient

async def forward_to_owner(event: events.NewMessage.Event):
    """
    Forwards incoming private messages to the first SUDO user (Owner),
    unless it's a command or the user is banned.
    """
    # 1. فحوصات أساسية: رسالة واردة، في الخاص، وليست صادرة من البوت
    if event.out or not event.is_private:
        return

    sender_id = event.sender_id

    # 2. تجاهل رسائل المطورين (حتى لا يتم إعادة توجيه رسائلك لنفسك)
    if sender_id in settings.telegram.SUDO_USERS:
        return

    # 3. تجاهل الأوامر (التي تبدأ بـ /)
    if event.text and event.text.startswith('/'):
        return

    # 4. تجاهل المحظورين
    if check_user_status(sender_id) == 'banned':
        return

    # 5. التحقق من إعدادات التوجيه من لوحة الأدمن
    admin_settings = load_admin_settings()
    if not admin_settings.get('message_forwarding', True):
        return

    # 6. الحصول على ايدي المالك (أول ايدي في قائمة SUDO_USERS)
    if not settings.telegram.SUDO_USERS:
        return
    
    owner_id = settings.telegram.SUDO_USERS[0]

    try:
        # 7. تنفيذ التوجيه
        await event.client.forward_messages(owner_id, event.message)
    except Exception as e:
        print(f"[Forwarding] Failed to forward message from {sender_id}: {e}")

def setup(client_instance: "TelegramClient"):
    """Registers the forwarding handler."""
    client_instance.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))(forward_to_owner)
    print("✅ Forwarding handler registered (bot/handlers/forwarding.py).")