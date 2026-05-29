# bot_v2/bot/handlers/ai/keys.py
# Contains event handlers for managing user-specific AI API keys.

import asyncio
import logging
import re
from typing import Optional

from telethon import events, Button
from telethon.errors.rpcerrorlist import MessageNotModifiedError

# Local imports
from bot.core.config import settings
from bot.core.database import add_user_key, get_user_keys, delete_user_key
from bot.core.state import conversation_manager

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message

# Logger for AI key operations
ai_keys_logger = logging.getLogger(__name__)

# --- API Key Management Handlers ---
async def my_api_keys_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    
    user_keys = await get_user_keys(sender_id)

    message = "**🔑 مفاتيح API الخاصة بك للذكاء الاصطناعي:**\n\n"
    if not user_keys:
        message += "لا توجد مفاتيح API مسجلة حالياً."
    else:
        for key_data in user_keys:
            masked_key = f"{key_data['api_key'][:5]}...{key_data['api_key'][-5:]}"
            message += (
                f"- **الخدمة:** `{key_data['service'].upper()}`\n"
                f"  **المعرف:** `{key_data['nickname']}`\n"
                f"  **المفتاح:** `{masked_key}`\n"
                f"  **الحالة:** `{key_data['status']}`\n"
            )
            message += f"  [حذف](del_ai_key:{key_data['id']})\n\n" # Inline delete button (placeholder)
    
    message += "\n**ملاحظة:** إضافة مفاتيحك الخاصة تمنحك استخداماً غير محدود للذكاء الاصطناعي."

    buttons = [
        [Button.inline("➕ إضافة مفتاح جديد", data="add_new_ai_key")],
        [Button.inline("↩️ القائمة الرئيسية", data="main_menu")]
    ]

    await safe_edit_message(event, message, buttons=buttons)


async def add_new_ai_key_prompt_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    
    conversation_manager.set_state(sender_id, "awaiting_ai_key_service", message_id=event.message_id)

    message = "**➕ إضافة مفتاح API جديد:**\n\n"
    message += "اختر الخدمة التي تريد إضافة مفتاح لها:"

    buttons = [
        [Button.inline("Gemini", data="select_ai_key_service:gemini")],
        [Button.inline("Groq", data="select_ai_key_service:groq")],
        [Button.inline("❌ إلغاء", data="cancel_ai_key_add")]
    ]
    await safe_edit_message(event, message, buttons=buttons)


async def select_ai_key_service_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    service = event.pattern_match.group(1).decode()
    
    if conversation_manager.get_status(sender_id) != "awaiting_ai_key_service":
        return await event.answer("انتهت جلسة إضافة المفتاح. يرجى البدء من جديد.", alert=True)

    conversation_manager.set_state(sender_id, "awaiting_ai_key_value", context={"service": service}, message_id=event.message_id)

    message = f"**➕ إضافة مفتاح {service.upper()} API:**\n\n"
    message += f"أرسل الآن مفتاح API الخاص بخدمة {service.upper()}."
    message += "\n\n**مثال:** `AIzaSy...` (لـ Gemini) أو `gsk_...` (لـ Groq)."

    buttons = [[Button.inline("❌ إلغاء", data="cancel_ai_key_add")]]
    await safe_edit_message(event, message, buttons=buttons)


# Message handler for receiving AI API key value
async def receive_ai_key_value_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    
    if state.get('status') != "awaiting_ai_key_value":
        return # Not in this conversation

    service = state['context']['service']
    api_key_value = event.text.strip()
    message_id_to_edit = state['message_id']
    
    # Simple validation based on prefix
    is_valid = False
    if len(api_key_value) > 255:
        await event.reply("❌ المفتاح طويل جداً (الحد الأقصى 255 حرف).")
        return
        
    if service == 'gemini' and api_key_value.startswith('AIzaSy'):
        is_valid = True
    elif service == 'groq' and api_key_value.startswith('gsk_'):
        is_valid = True
    elif api_key_value.startswith('sk-'): # Fallback for some models
        is_valid = True

    if not is_valid:
        await event.reply("❌ المفتاح الذي أرسلته لا يبدو صحيحاً لهذه الخدمة. يرجى التأكد والمحاولة مرة أخرى.")
        return

    # Prompt for nickname
    conversation_manager.set_state(
        sender_id,
        "awaiting_ai_key_nickname",
        context={"service": service, "api_key_value": api_key_value},
        message_id=message_id_to_edit
    )

    status_msg = await event.client.get_messages(sender_id, ids=message_id_to_edit)
    await safe_edit_message(
        status_msg,
        "**➕ إضافة مفتاح API جديد:**\n\nأرسل الآن **اسمًا تعريفياً (لقباً)** لهذا المفتاح (مثال: `مفتاحي الشخصي`, `مفتاح تجريبي`).",
        buttons=[[Button.inline("❌ إلغاء", data="cancel_ai_key_add")]]
    )


# Message handler for receiving AI API key nickname
async def receive_ai_key_nickname_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)

    if state.get('status') != "awaiting_ai_key_nickname":
        return # Not in this conversation
    
    nickname = event.text.strip()
    if len(nickname) > 50:
         await event.reply("❌ الاسم المختار طويل جداً (الحد الأقصى 50 حرف). حاول مرة أخرى باسم أقصر.")
         return
         
    service = state['context']['service']
    api_key_value = state['context']['api_key_value']
    message_id_to_edit = state['message_id']

    conversation_manager.delete_state(sender_id) # End conversation

    try:
        key_id = await add_user_key(sender_id, service, api_key_value, nickname)
        status_msg = await event.client.get_messages(sender_id, ids=message_id_to_edit)
        await safe_edit_message(
            status_msg,
            f"✅ تم إضافة مفتاح {service.upper()} API بنجاح! (المعرف: {nickname})",
            buttons=[[Button.inline("🔑 إدارة مفاتيح API", data="my_api_keys")]]
        )
    except Exception as e:
        ai_keys_logger.error(f"Failed to add AI key for user {sender_id}: {e}")
        status_msg = await event.client.get_messages(sender_id, ids=message_id_to_edit)
        await safe_edit_message(
            status_msg,
            f"❌ فشل إضافة المفتاح. ربما المفتاح مستخدم بالفعل أو حدث خطأ: {e}",
            buttons=[[Button.inline("🔑 إدارة مفاتيح API", data="my_api_keys")]]
        )


async def delete_ai_key_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    key_id = int(event.pattern_match.group(1).decode())

    try:
        deleted = await delete_user_key(key_id, sender_id)
        if deleted:
            await event.answer("✅ تم حذف المفتاح بنجاح.", alert=True)
            await my_api_keys_handler(event) # Refresh the keys list
        else:
            await event.answer("❌ المفتاح غير موجود أو لا تملك صلاحية حذفه.", alert=True)
    except Exception as e:
        ai_keys_logger.error(f"Failed to delete AI key {key_id} for user {sender_id}: {e}")
        await event.answer(f"❌ فشل حذف المفتاح: {e}", alert=True)


async def cancel_ai_key_add_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    conversation_manager.delete_state(sender_id)
    await event.answer("تم إلغاء عملية إضافة المفتاح.", alert=True)
    await my_api_keys_handler(event) # Go back to keys list


def setup(client):
    """Registers all AI key management handlers with the TelegramClient."""
    client.on(events.CallbackQuery(pattern=b"my_api_keys"))(my_api_keys_handler)
    client.on(events.CallbackQuery(pattern=b"add_new_ai_key"))(add_new_ai_key_prompt_handler)
    client.on(events.CallbackQuery(pattern=rb"select_ai_key_service:(.+)"))(select_ai_key_service_handler)
    client.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.get_status(e.sender_id) == "awaiting_ai_key_value"))(receive_ai_key_value_handler)
    client.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.get_status(e.sender_id) == "awaiting_ai_key_nickname"))(receive_ai_key_nickname_handler)
    client.on(events.CallbackQuery(pattern=rb"del_ai_key:(\d+)"))(delete_ai_key_handler)
    client.on(events.CallbackQuery(pattern=b"cancel_ai_key_add"))(cancel_ai_key_add_handler)

print("✅ bot_v2/bot/handlers/ai/keys.py initialized.")
