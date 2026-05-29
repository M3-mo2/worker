# bot_v2/bot/handlers/admin/broadcast.py
# Contains handlers for the message broadcasting feature.

import asyncio
from telethon import events
from telethon.tl.custom import Button
from telethon.errors.rpcerrorlist import UserIsBlockedError
from typing import TYPE_CHECKING, Dict, Any, List

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_all_users # For global broadcast
from bot.core.state import conversation_manager

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message

# Local Imports from bot_v2 handlers (for now, will be refactored later)

if TYPE_CHECKING:
    from telethon import TelegramClient

# --- UI Functions ---
def get_broadcast_menu_buttons(broadcast_settings: Dict[str, Any]) -> List[List[Button]]:
    """Creates the buttons for the broadcast panel based on current settings."""
    forward = broadcast_settings.get('forward', False)
    pin = broadcast_settings.get('pin', False)
    formatting = broadcast_settings.get('format', 'md')

    forward_status = "✅ مفعل" if forward else "❌ معطل"
    pin_status = "✅ مفعل" if pin else "❌ معطل"
    
    format_text = "Markdown"
    if formatting == 'html':
        format_text = "HTML"
    elif formatting is None:
        format_text = "بدون تنسيق"

    buttons = [
        [
            Button.inline(f"التوجيه: {forward_status}", data='admin:toggle_bcast_forward'),
            Button.inline(f"التثبيت: {pin_status}", data='admin:toggle_bcast_pin')
        ],
        [Button.inline(f"نوع التنسيق: {format_text}", data='admin:toggle_bcast_format')],
        [Button.inline("🚀 بدء الإرسال", data='admin:start_broadcast')],
        [Button.inline("⬅️ القائمة الرئيسية", data='admin:main_menu')]
    ]
    return buttons

async def send_broadcast_menu(event: events.CallbackQuery.Event):
    """Sends or edits the broadcast menu."""
    sender_id = event.sender_id
    
    current_state = conversation_manager.get_state(sender_id)
    
    # Fix: Only initialize if not already in setup mode to avoid resetting settings
    if not conversation_manager.has_state(sender_id) or current_state.get('status') != "admin_broadcast_setup":
        conversation_manager.set_state(sender_id, "admin_broadcast_setup", context={
            'broadcast': {'forward': False, 'pin': False, 'format': 'md'} # md -> html -> None
        }, message_id=event.message_id) # Store message_id for editing
        current_state = conversation_manager.get_state(sender_id)

    settings_context = current_state.get('context', {})
    broadcast_settings = settings_context.get('broadcast', {'forward': False, 'pin': False, 'format': 'md'})
    
    text = (
        "**📢 لوحة الإذاعة والنشر**\n\n"
        "يمكنك تخصيص إعدادات الإرسال من الأسفل:\n"
        "• **التوجيه:** إرسال الرسالة كما هي (Forward) من حسابك.\n"
        "• **التثبيت:** تثبيت الرسالة عند المستخدمين (يتطلب صلاحيات).\n"
        "• **التنسيق:** نوع تنسيق النص (Markdown/HTML).\n\n"
        "__اضغط على الأزرار للتبديل، ثم اضغط بدء الإرسال.__"
    )
    buttons = get_broadcast_menu_buttons(broadcast_settings)
    await safe_edit_message(event, text, buttons=buttons)


# --- Callbacks ---

async def broadcast_menu_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    await send_broadcast_menu(event)


async def toggle_bcast_forward_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != "admin_broadcast_setup":
        return await event.answer("انتهت جلسة الإعداد. يرجى البدء من جديد.", alert=True)
    
    state['context']['broadcast']['forward'] = not state['context']['broadcast'].get('forward', False)
    conversation_manager.set_state(sender_id, state['status'], context=state['context'], message_id=state['message_id'])
    await send_broadcast_menu(event)


async def toggle_bcast_pin_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != "admin_broadcast_setup":
        return await event.answer("انتهت جلسة الإعداد. يرجى البدء من جديد.", alert=True)

    state['context']['broadcast']['pin'] = not state['context']['broadcast'].get('pin', False)
    conversation_manager.set_state(sender_id, state['status'], context=state['context'], message_id=state['message_id'])
    await send_broadcast_menu(event)


async def toggle_bcast_format_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != "admin_broadcast_setup":
        return await event.answer("انتهت جلسة الإعداد. يرجى البدء من جديد.", alert=True)
    
    current_format = state['context']['broadcast'].get('format', 'md')
    if current_format == 'md': new_format = 'html'
    elif current_format == 'html': new_format = None
    else: new_format = 'md'

    state['context']['broadcast']['format'] = new_format
    conversation_manager.set_state(sender_id, state['status'], context=state['context'], message_id=state['message_id'])
    await send_broadcast_menu(event)


async def start_broadcast_prompt(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != "admin_broadcast_setup":
        return await event.answer("انتهت جلسة الإعداد. يرجى البدء من جديد.", alert=True)
    
    # Store message_id for editing during broadcast conversation
    conversation_manager.set_state(sender_id, "awaiting_broadcast_message", context=state['context'], message_id=event.message_id)
    await safe_edit_message(event, "**▶️ بدء الإذاعة**\n\nأرسل الآن الرسالة التي تريد إذاعتها.", buttons=[[Button.inline("إلغاء ❌", data="admin:cancel_action")]])


# --- Conversation Handler ---
async def admin_broadcast_conversation_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    state_data = conversation_manager.get_state(sender_id)
    state_status = state_data.get('status')
    message_id_to_edit = state_data.get('message_id')

    if state_status == "awaiting_broadcast_message":
        broadcast_settings = state_data.get('context', {}).get('broadcast', {})
        is_forward = broadcast_settings.get('forward', False)
        pin_message = broadcast_settings.get('pin', False)
        formatting = broadcast_settings.get('format', 'md')

        all_users = load_all_users()
        if not all_users:
            await event.reply("❌ لا يوجد مستخدمون في قاعدة البيانات للإذاعة إليهم.")
            conversation_manager.delete_state(sender_id)
            return

        await event.reply(f"📢 **جاري بدء الإذاعة إلى {len(all_users)} مستخدم...**")
        
        success_count = 0
        failure_count = 0
        
        # Iterate over a copy to avoid issues if all_users is modified during broadcast
        for user_id_str in list(all_users.keys()): 
            user_id = int(user_id_str)
            try:
                if is_forward:
                    sent_msg = await client.forward_messages(user_id, event.message)
                else:
                    sent_msg = await client.send_message(
                        user_id,
                        event.message,
                        parse_mode=formatting
                    )
                
                if pin_message:
                    await client.pin_message(user_id, sent_msg, notify=True)

                success_count += 1
                await asyncio.sleep(0.1) # Small delay to avoid API limits
            except UserIsBlockedError:
                print(f"Broadcast: User {user_id} blocked the bot.")
                failure_count += 1
            except Exception as e:
                print(f"Broadcast failed for user {user_id}: {e}")
                failure_count += 1
        
        report_text = (
            f"**📣 اكتملت الإذاعة!**\n\n"
            f"✅ **نجح الإرسال إلى:** `{success_count}` مستخدم\n"
            f"❌ **فشل الإرسال إلى:** `{failure_count}` مستخدم"
        )
        await event.reply(report_text)
        
        conversation_manager.delete_state(sender_id)
        
        # Restore the main admin panel after broadcasting
        if message_id_to_edit:
             mock_event = await event.client.get_messages(sender_id, ids=message_id_to_edit)
             if mock_event:
                from bot.handlers.admin.main import send_main_admin_panel
                await send_main_admin_panel(mock_event, edit=True)


def setup(client_instance: "TelegramClient"):
    """Registers all broadcast handlers with the TelegramClient."""
    # Callbacks for menu navigation and toggles
    client_instance.on(events.CallbackQuery(pattern=b'admin:broadcast_menu'))(broadcast_menu_callback)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:toggle_bcast_forward'))(toggle_bcast_forward_callback)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:toggle_bcast_pin'))(toggle_bcast_pin_callback)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:toggle_bcast_format'))(toggle_bcast_format_callback)
    client_instance.on(events.CallbackQuery(pattern=b'admin:start_broadcast'))(start_broadcast_prompt)

    # NewMessage handler for broadcast conversation
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.get_status(e.sender_id) == "awaiting_broadcast_message"))(admin_broadcast_conversation_handler)
    print("✅ Admin Broadcast handlers registered.")
