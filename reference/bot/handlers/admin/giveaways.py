# bot_v2/bot/handlers/admin/giveaways.py
# Contains handlers for creating and managing giveaway codes for PRO subscriptions.

import time
import secrets
from datetime import datetime
from telethon import events
from telethon.tl.custom import Button
from typing import TYPE_CHECKING, Dict, Any, List

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_giveaways, save_giveaways
from bot.core.state import conversation_manager

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message
from bot.utils.time import _TZ # From utilities

# Local Imports from bot_v2 handlers (for now, will be refactored later)


# --- UI Functions ---
# Giveaways are usually started from the host_settings_panel
# So this module will primarily have the conversation handlers for creation
async def send_giveaway_creation_prompt(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    conversation_manager.set_state(sender_id, "awaiting_giveaway_days", message_id=event.message_id)
    await safe_edit_message(event, "🗓️ **إنشاء مسابقة**\n\nأرسل الآن عدد **الأيام** التي سيحصل عليها الفائزون (مثال: 30).", buttons=[[Button.inline("إلغاء ❌", data="admin:cancel_action")]])


# --- Callbacks ---

async def create_giveaway_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) != 'sudo': # Only SUDO can create giveaways
        return await event.answer("🚫 هذه الميزة مخصصة للمالك فقط.", alert=True)
    await send_giveaway_creation_prompt(event)


# --- Conversation Handler ---
async def admin_giveaways_conversation_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    state_data = conversation_manager.get_state(sender_id)
    state_status = state_data.get('status')
    message_id_to_edit = state_data.get('message_id')

    # A helper function to restore the panel after an action
    async def restore_panel(menu_function_to_call):
        if message_id_to_edit:
            try:
                mock_event = await event.client.get_messages(sender_id, ids=message_id_to_edit)
                if mock_event:
                    await menu_function_to_call(mock_event)
            except Exception as e:
                print(f"Error restoring panel: {e}")
                await event.reply("اكتمل الإجراء.")


    # --- CREATE GIVEAWAY (Part 1: Get Days) ---
    if state_status == "awaiting_giveaway_days":
        try:
            days = int(event.text)
            if days <= 0:
                await event.reply("❌ يرجى إدخال عدد أيام صحيح أكبر من صفر.")
                return

            # Store days and ask for limit
            state_data['giveaway_days'] = days
            conversation_manager.set_state(sender_id, 'awaiting_giveaway_limit', context=state_data['context'], message_id=message_id_to_edit)
            await event.reply(f"🗓️ الأيام: {days}\n\n👥 أرسل الآن عدد **الأشخاص** المسموح لهم باستخدام هذا الكود (مثال: 5).")

        except (ValueError, TypeError):
            await event.reply("❌ إدخال غير صالح. يرجى إرسال عدد الأيام كرقم صحيح.")

    # --- CREATE GIVEAWAY (Part 2: Get Limit & Generate) ---
    elif state_status == "awaiting_giveaway_limit":
        try:
            limit = int(event.text)
            if limit <= 0:
                await event.reply("❌ يرجى إدخال عدد أشخاص صحيح أكبر من صفر.")
                return

            days = state_data['context']['giveaway_days']
            
            # Generate a unique code
            giveaways = load_giveaways()
            while True:
                code = secrets.token_hex(4) # Example: 8 random hex chars
                if code not in giveaways:
                    break
            
            now = int(time.time())
            
            # Create and save the code
            giveaways[code] = {
                "days": days,
                "limit": limit,
                "created_at": now,
                "claimed_by": []
            }
            save_giveaways(giveaways)

            confirmation_message = (
                f"✅ **تم إنشاء كود المسابقة بنجاح!**\n\n"
                f"👇 اضغط على الكود لنسخه:\n`{code}`\n\n"
                f"▫️ **المدة:** {days} يوم\n"
                f"▫️ **العدد:** {limit} أشخاص\n\n"
                f"⚠️ *الكود صالح لمدة 24 ساعة فقط من الآن.*"
            )
            await event.reply(confirmation_message, parse_mode='md')

        except (ValueError, TypeError):
            await event.reply("❌ إدخال غير صالح. يرجى إرسال عدد الأشخاص كرقم صحيح.")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ غير متوقع: {e}")
        finally:
            conversation_manager.delete_state(sender_id)
            # Restore the hosting settings panel (where giveaway creation is triggered from)
            from bot.handlers.admin.settings import send_host_settings_panel
            await restore_panel(send_host_settings_panel)


def setup(client_instance: "TelegramClient"):
    """Registers all admin giveaway handlers with the TelegramClient."""
    # Callbacks for actions
    client_instance.on(events.CallbackQuery(pattern=b'admin:create_giveaway'))(create_giveaway_callback)

    # NewMessage handler for conversations
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.has_state(e.sender_id) and conversation_manager.get_status(e.sender_id) in ["awaiting_giveaway_days", "awaiting_giveaway_limit"]))(admin_giveaways_conversation_handler)
    print("✅ Admin Giveaways handlers registered.")
