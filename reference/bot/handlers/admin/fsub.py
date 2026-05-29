# bot_v2/bot/handlers/admin/fsub.py
# Contains handlers for managing force-subscribe channels.

from telethon import events
from telethon.tl.custom import Button
from bot.services.telegram import get_chat_entity, export_chat_invite_link
from telethon.errors.rpcerrorlist import UserNotParticipantError
from typing import TYPE_CHECKING, Dict, Any, List

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_admin_settings, save_admin_settings
from bot.core.state import conversation_manager

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status
from bot.utils.telegram import safe_edit_message

if TYPE_CHECKING:
    from telethon import TelegramClient

# --- UI Functions ---
async def send_force_subscribe_menu(event: events.CallbackQuery.Event):
    admin_settings = load_admin_settings()
    channels = admin_settings.get("force_subscribe_channels", [])
    
    text = (
        "**🌟 ⦗ قسم الاشتراك الإجباري ⦘**\n\n"
        "💡 **الوصف:** هنا يمكنك إدارة القنوات التي يجب على المستخدمين الاشتراك بها كشرط لاستخدام البوت.\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📊 **إحصائيات:** مسجل لديك حالياً ` {len(channels)} ` قناة/مجموعة فرض.\n\n"
        "👇 إختر من الأزرار أدناه لإدارة قنواتك:"
    )
    
    buttons = [
        [Button.inline("➕ إضافة قناة جديدة", data='admin:add_fsub_channel')]
    ]
    
    if channels:
        # Show specific channels for quick deletion
        for channel in channels:
            title = channel.get('title', 'قناة غير معروفة')
            # Using channel ID in button data for removal
            buttons.append([Button.inline(f"🗑️ حذف: {title}", data=f"admin:rem_fsub_channel_{channel['id']}")])
        
        # Add a button to show all channel details nicely
        buttons.append([Button.inline("📋 عرض تفاصيل القنوات الحالية", data='admin:view_fsub_channels_info')])

    buttons.append([Button.inline("⬅️ عودة للقائمة الرئيسية", data='admin:main_menu')])
    
    await safe_edit_message(event, text, buttons=buttons)


async def view_fsub_channels_info_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)

    admin_settings = load_admin_settings()
    channels = admin_settings.get("force_subscribe_channels", [])

    if not channels:
        return await event.answer("⚠️ لا توجد قنوات مضافة حالياً.", alert=True)

    text = "**📋 ⦗ تفاصيل قنوات الاشتراك الإجباري ⦘**\n\n"
    for i, ch in enumerate(channels, 1):
        text += (
            f"**{i}. {ch.get('title', 'بدون اسم')}**\n"
            f"   • الايدي: `{ch.get('id')}`\n"
            f"   • الرابط: [اضغط هنا]({ch.get('link')})\n"
            "━━━━━━━━━━━━━━━━━━\n"
        )

    buttons = [[Button.inline("⬅️ رجوع لقسم الاشتراك الإجباري", data='admin:force_subscribe_menu')]]
    await safe_edit_message(event, text, buttons=buttons, link_preview=False)


# --- Callbacks ---

async def force_subscribe_menu_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    await send_force_subscribe_menu(event)


async def add_fsub_channel_prompt(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    conversation_manager.set_state(sender_id, "awaiting_fsub_channel", message_id=event.message_id)
    await safe_edit_message(event, "**➕ إضافة قناة للاشتراك الإجباري**\n\nأرسل الآن يوزر القناة (e.g., @username) أو أعد توجيه رسالة منها.", buttons=[[Button.inline("إلغاء ❌", data="admin:cancel_action")]])


async def rem_fsub_channel_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    
    channel_id_to_remove = int(event.pattern_match.group(1).decode())
    admin_settings = load_admin_settings()
    channels = admin_settings.get("force_subscribe_channels", [])
    
    # Filter out the channel to be removed
    admin_settings["force_subscribe_channels"] = [ch for ch in channels if ch["id"] != channel_id_to_remove]
    
    save_admin_settings(admin_settings)
    await event.answer("🗑️ تم حذف القناة بنجاح.", alert=True)
    await send_force_subscribe_menu(event) # Refresh the menu


# --- Conversation Handler ---
async def admin_fsub_conversation_handler(event: events.NewMessage.Event):
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

    # --- ADD FORCE SUBSCRIBE CHANNEL ---
    if state_status == "awaiting_fsub_channel":
        try:
            entity = None
            if event.message.forward:
                # Get entity from the forwarded message's chat
                entity = await get_chat_entity(event.message.forward.chat_id)
            else:
                entity = await get_chat_entity(event.text.strip())

            if not hasattr(entity, 'title'):
                 await event.reply("❌ هذا الكيان ليس قناة أو مجموعة. يرجى المحاولة مرة أخرى.")
                 return
            
            # Try to create a new invite link
            try:
                link = await export_chat_invite_link(entity.id)
            except Exception:
                # Fallback to public username if creating a link fails
                if hasattr(entity, 'username') and entity.username:
                    link = f"https://t.me/{entity.username}"
                else:
                    await event.reply("❌ لا يمكنني إنشاء رابط دعوة لهذه القناة. تأكد من أن البوت مشرف في القناة ولديه صلاحية دعوة المستخدمين.")
                    return

            admin_settings = load_admin_settings()
            if "force_subscribe_channels" not in admin_settings:
                admin_settings["force_subscribe_channels"] = []
            
            # Formulate the correct ID format first
            channel_id = entity.id
            if hasattr(entity, 'broadcast') or hasattr(entity, 'megagroup'):
                if channel_id > 0:
                    channel_id = int(f"-100{channel_id}")

            # Check if channel is already added using the normalized ID
            if any(ch["id"] == channel_id for ch in admin_settings["force_subscribe_channels"]):
                await event.reply("⚠️ هذه القناة مضافة بالفعل في قائمة الاشتراك الإجباري.")
            else:
                admin_settings["force_subscribe_channels"].append({
                    "id": channel_id,
                    "title": entity.title,
                    "link": link
                })
                save_admin_settings(admin_settings)
                await event.reply(f"✅ تم إضافة القناة '{entity.title}' بنجاح إلى قائمة الاشتراك الإجباري.")

        except Exception as e:
            print(f"Error adding force-sub channel: {e}")
            await event.reply("❌ خطأ. لم أتمكن من العثور على القناة. يرجى التحقق من المعرف أو تأكد من أن البوت مشرف في القناة.")
        finally:
            conversation_manager.delete_state(sender_id)
            await restore_panel(send_force_subscribe_menu)


def setup(client_instance: "TelegramClient"):
    """Registers all admin force-subscribe handlers with the TelegramClient."""
    # Callbacks for menu navigation
    client_instance.on(events.CallbackQuery(pattern=b'admin:force_subscribe_menu'))(force_subscribe_menu_callback)

    # Callbacks for actions
    client_instance.on(events.CallbackQuery(pattern=b'admin:add_fsub_channel'))(add_fsub_channel_prompt)
    client_instance.on(events.CallbackQuery(pattern=b'admin:view_fsub_channels_info'))(view_fsub_channels_info_callback)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:rem_fsub_channel_(-?\d+)'))(rem_fsub_channel_callback)

    # NewMessage handler for conversations
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.has_state(e.sender_id) and conversation_manager.get_status(e.sender_id) == "awaiting_fsub_channel"))(admin_fsub_conversation_handler)
    print("✅ Admin Force-Subscribe handlers registered.")
