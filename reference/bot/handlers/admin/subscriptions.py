# bot_v2/bot/handlers/admin/subscriptions.py
# Contains handlers for manually managing user subscriptions (adding/removing PRO plans).

import time
from datetime import datetime
from telethon import events
from telethon.tl.custom import Button
from typing import TYPE_CHECKING, Dict, Any, List

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_all_users, save_all_users
from bot.core.state import conversation_manager
from bot.services.telegram import get_user_info


# Local Imports from bot_v2 services
from bot.services.telegram import get_user_info
from bot.services.user_service import check_user_status, get_user_data, save_user_data
from bot.services.billing_service import update_user_bot_tiers

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message
from bot.utils.time import _TZ

# Local Imports from bot_v2 handlers (for now, will be refactored later)


# --- UI Functions ---
def get_subs_menu_buttons() -> List[List[Button]]:
    """Creates the buttons for the subscription management menu."""
    return [
        [Button.inline("➕ إضافة اشتراك", data='admin:add_sub'), Button.inline("➖ حذف اشتراك", data='admin:rem_sub')],
        [Button.inline("📋 عرض المشتركين", data='admin:list_subs')],
        [Button.inline("⬅️ رجوع", data='admin:main_menu')]
    ]

async def send_subs_menu(event: events.CallbackQuery.Event):
    """Sends or edits the subscription management menu."""
    text = "**⭐️ قسم إدارة الاشتراكات**\n\nاختر الإجراء المطلوب:"
    buttons = get_subs_menu_buttons()
    await safe_edit_message(event, text, buttons=buttons)


# --- Callbacks ---

async def subs_menu_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    await send_subs_menu(event)


async def add_sub_prompt(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    conversation_manager.set_state(sender_id, "awaiting_sub_user", message_id=event.message_id)
    await safe_edit_message(event, "**➕ إضافة اشتراك**\n\nأرسل الآن ID المستخدم، أو اليوزرنيم، أو قم بالرد على رسالته.", buttons=[[Button.inline("إلغاء ❌", data="admin:cancel_action")]])

async def rem_sub_prompt(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    conversation_manager.set_state(sender_id, "awaiting_sub_to_rem", message_id=event.message_id)
    await safe_edit_message(event, "**➖ حذف اشتراك**\n\nأرسل الآن ID المستخدم، أو اليوزرنيم، أو قم بالرد على رسالته لحذف اشتراكه.", buttons=[[Button.inline("إلغاء ❌", data="admin:cancel_action")]])

async def list_subs_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)

    all_users = load_all_users()
    pro_users = {uid: uinfo for uid, uinfo in all_users.items() if uinfo.get('plan') == 'pro'}
    
    if not pro_users:
        return await event.answer("ℹ️ لا يوجد مشتركين في الخطة المدفوعة حالياً.", alert=True)

    message = "**📋 قائمة المشتركين في الخطة المدفوعة:**\n\n"
    for user_id, user_info in pro_users.items():
        first_name = user_info.get('first_name', 'N/A')
        expiry_ts = user_info.get('plan_expiry')
        if expiry_ts:
            if time.time() > expiry_ts: # Check if subscription is expired
                try:
                    expiry_str = f"- منتهي منذ {datetime.fromtimestamp(expiry_ts, _TZ).strftime('%Y-%m-%d')}"
                except:
                    expiry_str = "- منتهي (تاريخ غير صالح)"
            else:
                try:
                    expiry_str = f"- ينتهي في {datetime.fromtimestamp(expiry_ts, _TZ).strftime('%Y-%m-%d')}"
                except:
                     expiry_str = "- ينتهي (تاريخ غير صالح)"
        else:
            expiry_str = "- اشتراك دائم"
        
        message += f"- [{first_name}](tg://user?id={user_id}) (`{user_id}`) {expiry_str}\n"

    # We use event.edit to show the list in the panel itself
    await safe_edit_message(event, message, buttons=[[Button.inline("⬅️ رجوع", data='admin:subs_menu')]])


# --- Conversation Handler for admin:subscriptions (message inputs) ---
async def admin_subs_conversation_handler(event: events.NewMessage.Event):
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


    # --- ADD SUBSCRIPTION (Part 1: Get User) ---
    if state_status == "awaiting_sub_user":
        user_input = event.text
        if event.is_reply:
            reply = await event.get_reply_message()
            user_input = reply.sender_id
        user_info = await get_user_info(user_input)
        if not user_info:
            await event.reply("❌ لم أتمكن من العثور على هذا المستخدم. تم إلغاء العملية.")
            conversation_manager.delete_state(sender_id)
            await restore_panel(send_subs_menu)
            return

        # Store user info and ask for days
        context = {'sub_user_info': user_info}
        conversation_manager.set_state(sender_id, 'awaiting_sub_days', context=context, message_id=message_id_to_edit) # Update state
        await event.reply(f"👤 المستخدم: **{user_info['first_name']}** (`{user_info['id']}`)\n\n🗓️ أرسل الآن عدد أيام الاشتراك (مثال: 30).")

    # --- ADD SUBSCRIPTION (Part 2: Get Days & Save) ---
    elif state_status == "awaiting_sub_days":
        try:
            days = int(event.text)
            if days <= 0:
                await event.reply("❌ يرجى إدخال عدد أيام صحيح أكبر من صفر.")
                return

            user_info = state_data['context']['sub_user_info']
            user_id_str = str(user_info['id'])

            # Calculate expiry timestamp
            expiry_timestamp = int(time.time()) + (days * 86400) # 86400 seconds in a day

            # Update all_users.json
            new_user_data = get_user_data(int(user_id_str))
            if not new_user_data: # If user not found, initialize a new dict
                user_entity = await event.get_sender()
                new_user_data = {
                    "first_name": user_info['first_name'],
                    "username": user_info['username']
                }
            new_user_data['plan'] = 'pro'
            new_user_data['plan_expiry'] = expiry_timestamp
            new_user_data.pop('expiry_warning_sent', None)
            save_user_data(int(user_id_str), new_user_data)
            
            update_user_bot_tiers(user_id_str, 'pro') # Placeholder
            
            expiry_date_str = datetime.fromtimestamp(expiry_timestamp, _TZ).strftime('%Y-%m-%d %H:%M')
            confirmation_message = (
                f"✅ **تمت ترقية المستخدم بنجاح!**\n\n"
                f"👤 **المستخدم:** [{user_info['first_name']}](tg://user?id={user_id_str})\n"
                f"⭐️ **الخطة الحالية:** PRO\n"
                f"🗓️ **مدة الاشتراك:** {days} يوم\n"
                f"⏳ **تاريخ الانتهاء:** `{expiry_date_str}`"
            )
            await event.reply(confirmation_message, parse_mode='md')

        except (ValueError, TypeError):
            await event.reply("❌ إدخال غير صالح. يرجى إرسال عدد الأيام كرقم صحيح.")
        except Exception as e:
            await event.reply(f"❌ حدث خطأ غير متوقع: {e}")
        finally:
            conversation_manager.delete_state(sender_id)
            await restore_panel(send_subs_menu)

    # --- REMOVE SUBSCRIPTION ---
    elif state_status == "awaiting_sub_to_rem":
        user_input = event.text
        if event.is_reply:
            reply = await event.get_reply_message()
            user_input = reply.sender_id
        user_info = await get_user_info(user_input)
        if not user_info:
            await event.reply("❌ لم أتمكن من العثور على هذا المستخدم. تم إلغاء العملية.")
        else:
            user_id_str = str(user_info['id'])
            user_data_to_update = get_user_data(int(user_id_str))
            if user_data_to_update and user_data_to_update.get('plan') == 'pro':
                user_data_to_update['plan'] = 'free'
                user_data_to_update.pop('plan_expiry', None)
                save_user_data(int(user_id_str), user_data_to_update)
                update_user_bot_tiers(user_id_str, 'free') # Placeholder
                await event.reply(f"✅ تم إلغاء اشتراك المستخدم [{user_info['first_name']}](tg://user?id={user_id_str}) وإعادته للخطة المجانية.")
            else:
                await event.reply("ℹ️ هذا المستخدم ليس لديه اشتراك مدفوع أصلاً.")

        conversation_manager.delete_state(sender_id)
        await restore_panel(send_subs_menu)


def setup(client_instance: "TelegramClient"):
    """Registers all admin subscription management handlers with the TelegramClient."""
    # Callbacks for menu navigation
    client_instance.on(events.CallbackQuery(pattern=b'admin:subs_menu'))(subs_menu_callback)

    # Callbacks for actions
    client_instance.on(events.CallbackQuery(pattern=b'admin:add_sub'))(add_sub_prompt)
    client_instance.on(events.CallbackQuery(pattern=b'admin:rem_sub'))(rem_sub_prompt)
    client_instance.on(events.CallbackQuery(pattern=b'admin:list_subs'))(list_subs_callback)

    # NewMessage handler for conversations
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.has_state(e.sender_id) and conversation_manager.get_status(e.sender_id) in ["awaiting_sub_user", "awaiting_sub_days", "awaiting_sub_to_rem"]))(admin_subs_conversation_handler)
    print("✅ Admin Subscription Management handlers registered.")