# bot_v2/bot/handlers/admin/main.py
# Contains the main admin panel and handlers for global bot settings.

from telethon import events
from telethon.tl.custom import Button
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_admin_settings, save_admin_settings
from bot.core.state import conversation_manager

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message

# Local Imports from bot_v2 handlers (for now, will be refactored later)
from bot.handlers.admin.users import send_admins_menu, send_ban_menu
from bot.handlers.admin.subscriptions import send_subs_menu
from bot.handlers.admin.broadcast import send_broadcast_menu
from bot.handlers.admin.fsub import send_force_subscribe_menu
from bot.handlers.admin.stats import send_stats_menu
from bot.handlers.admin.settings import send_host_settings_panel, send_site_settings_panel
from bot.handlers.admin.points import send_points_admin_panel # Import points panel

SOURCE_CHANNEL_URL = "https://t.me/BroCood" # Placeholder URL

# --- UI Functions ---
def get_main_admin_panel_buttons(user_id: int) -> List[List[Button]]:
    """Generates the buttons for the main admin panel."""
    admin_settings = load_admin_settings()
    forwarding_status = "✅" if admin_settings.get('message_forwarding', True) else "❌"
    bot_status = "✅ يعمل" if admin_settings.get('bot_status', True) else "❌ معطل"
    
    daily_backup = admin_settings.get('daily_backup', False)
    daily_backup_status = "✅ مفعل" if daily_backup else "❌ معطل"
    
    buttons = [
        [Button.inline(f"توجيه الرسائل {forwarding_status}", data='admin:toggle_forwarding'), Button.inline(f"وضع البوت {bot_status}", data='admin:toggle_bot_status')],
        [Button.inline("📦 نسخ احتياطي فوري", data="admin:backup_now"), Button.inline(f"نسخ يومي: {daily_backup_status}", data="admin:toggle_daily_backup")],
        [Button.inline("قسم الحظر", data='admin:ban_menu'), Button.inline("قسم الاشتراكات", data='admin:subs_menu')],
        [Button.inline("قسم الاذاعه", data='admin:broadcast_menu'), Button.inline("الاشتراك الاجباري", data='admin:force_subscribe_menu')],
        [Button.inline("📊 الإحصائيات", data='admin:stats_menu'), Button.inline("🛒 إدارة الماركت", data='admin_marketplace_home')],
        [Button.inline("💎 نظام النقاط", data='admin:points_menu'), Button.inline("🌐 إعدادات الموقع", data='admin:site_settings_section')],
        [Button.inline("⚙️ إعدادات الاستضافة", data='admin:host_settings_section')]
    ]

    # Add the admins management button only if the user is a SUDO_USER
    if user_id in settings.telegram.SUDO_USERS:
        buttons.insert(1, [Button.inline("قسم الادمنيه", data='admin:admins_menu')])
        
    return buttons


async def send_main_admin_panel(event: events.NewMessage.Event | events.CallbackQuery.Event, edit: bool = False):
    """Sends or edits the main admin panel message."""
    sender_id = event.sender_id
    text = f"أهلاً بك عزيزي المطور، إليك لوحة التحكم.\n\[قناة السورس]({SOURCE_CHANNEL_URL})"
    buttons = get_main_admin_panel_buttons(sender_id)
    
    if edit:
        try:
            await safe_edit_message(event, text, buttons=buttons, parse_mode='md')
        except Exception:
            # Fallback only if edit fails completely
            try:
                await event.client.send_message(sender_id, text, buttons=buttons, parse_mode='md', link_preview=False)
            except Exception:
                pass
    else:
        # For NewMessage events, use event.reply or event.respond
        if isinstance(event, events.NewMessage.Event):
            await event.reply(text, buttons=buttons, parse_mode='md', link_preview=False)
        else: # CallbackQuery event, but edit=False implies sending a new message if current one is not to be edited
             try:
                 await event.client.send_message(sender_id, text, buttons=buttons, parse_mode='md', link_preview=False)
             except Exception as e:
                 print(f"Failed to send message in admin panel: {e}")


# --- Callbacks ---

async def admin_callback_handler(event: events.CallbackQuery.Event):
    """
    Handles all callbacks related to the admin panel.
    This handler specifically catches any data that starts with 'admin:'.
    """
    sender_id = event.sender_id
    user_status = check_user_status(sender_id) # Placeholder

    # Allow access if the user is a SUDO_USER or a regular admin
    if sender_id in settings.telegram.SUDO_USERS or user_status == 'admin':
        data = event.data.decode('utf-8').split(':')[1]

        # --- Main Panel Toggles ---
        if data in ['toggle_forwarding', 'toggle_bot_status']:
            admin_settings = load_admin_settings()
            if data == 'toggle_forwarding':
                admin_settings['message_forwarding'] = not admin_settings.get('message_forwarding', True)
            elif data == 'toggle_bot_status':
                admin_settings['bot_status'] = not admin_settings.get('bot_status', True)
            save_admin_settings(admin_settings)
            await send_main_admin_panel(event, edit=True)
            await event.answer("تم تحديث الإعداد.")

        # --- Cancel Action (Generic) ---
        elif data == 'cancel_action':
            if conversation_manager.has_state(sender_id):
                conversation_manager.delete_state(sender_id)
            
            # This is a generic cancel. It should ideally return to the specific menu.
            # For now, it returns to the main admin panel.
            # A better implementation would be to store the 'return_to' menu in the state.
            await event.answer("تم إلغاء العملية.", alert=True)
            await send_main_admin_panel(event, edit=True)

        # --- Menu Navigation ---
        elif data == 'main_menu':
            if conversation_manager.has_state(sender_id):
                conversation_manager.delete_state(sender_id) # Clear conversation state
            await send_main_admin_panel(event, edit=True)
        elif data == 'admins_menu':
            await send_admins_menu(event)
        elif data == 'ban_menu':
            await send_ban_menu(event)
        elif data == 'subs_menu':
            await send_subs_menu(event)
        elif data == 'broadcast_menu':
            await send_broadcast_menu(event)
        elif data == 'force_subscribe_menu':
            await send_force_subscribe_menu(event)
        elif data == 'stats_menu':
            await send_stats_menu(event)
        elif data == 'host_settings_section':
            await send_host_settings_panel(event)
        elif data == 'site_settings_section':
            await send_site_settings_panel(event)
        elif data == 'points_menu':
            await send_points_admin_panel(event)
        
        # --- Other callbacks will be handled by their respective modules ---
        else:
            pass
    else:
        await event.answer("🚫 أنت لست من مطورين البوت.", alert=True)


# --- NewMessage Handlers for Admin Conversations ---
async def admin_conversation_handler(event: events.NewMessage.Event):
    """Handles text messages that are part of an admin conversation."""
    sender_id = event.sender_id
    state_data = conversation_manager.get_state(sender_id)
    state_status = state_data.get('status')
    message_id_to_edit = state_data.get('message_id')

    # A helper function to restore the panel after an action
    async def restore_panel(menu_function_to_call):
        if message_id_to_edit:
            try:
                # Create a mock event to pass to the menu function
                mock_event = await event.client.get_messages(sender_id, ids=message_id_to_edit)
                if mock_event:
                    # The called function should accept 'event' and potentially 'edit=True'
                    await menu_function_to_call(mock_event, edit=True) # Assuming 'edit=True' by default for restore
            except Exception as e:
                print(f"Error restoring panel: {e}")
                # Fallback if editing fails
                await event.reply("اكتمل الإجراء.")

    # --- Add your conversation handling logic here based on state_status ---
    # Example:
    # if state_status == "awaiting_admin_to_add":
    #     user_info = await get_user_info_from_text(event.text) # Placeholder for user info resolver
    #     # ... logic ...
    #     conversation_manager.delete_state(sender_id)
    #     await restore_panel(send_admins_menu)


def setup(client_instance: "TelegramClient"):
    """Registers all admin main handlers with the TelegramClient."""
    client_instance.on(events.CallbackQuery(pattern=b'admin:'))(admin_callback_handler)
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and (e.sender_id in settings.telegram.SUDO_USERS or check_user_status(e.sender_id) == 'admin') and conversation_manager.has_state(e.sender_id)))(admin_conversation_handler)
    print("✅ Admin Main handlers registered.")
