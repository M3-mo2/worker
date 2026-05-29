# bot_v2/bot/handlers/admin/users.py
# Contains handlers for managing admins and banned users.

from telethon import events
from telethon.tl.custom import Button
from telethon.tl.functions.users import GetFullUserRequest
from typing import TYPE_CHECKING, Dict, Any, Optional, List
import math

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_admin_list, save_admin_list, load_banned_list, save_banned_list
from bot.core.state import conversation_manager

# Local Imports from bot_v2 services
from bot.services.telegram import get_user_info
from bot.services.user_service import check_user_status

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message

# --- Constants ---
ITEMS_PER_PAGE = 10

# --- Helper Functions ---

def get_pagination_buttons(current_page: int, total_pages: int, data_prefix: str) -> List[Button]:
    buttons = []
    if current_page > 1:
        buttons.append(Button.inline("⬅️ السابق", data=f"{data_prefix}_page_{current_page - 1}"))
    if current_page < total_pages:
        buttons.append(Button.inline("التالي ➡️", data=f"{data_prefix}_page_{current_page + 1}"))
    return buttons

async def format_user_entry(user_id: str, user_info: Dict[str, Any]) -> str:
    first_name = user_info.get('first_name', 'Unknown')
    username = user_info.get('username')
    username_text = f"(@{username})" if username else ""
    return f"👤 [{first_name}](tg://user?id={user_id}) {username_text}\n   └ الأيدي: `{user_id}`"

# --- UI Functions ---

def get_admins_menu_buttons() -> List[List[Button]]:
    return [
        [Button.inline("➕ أضف أدمن", data='admin:add_admin'), Button.inline("➖ حذف أدمن", data='admin:rem_admin_menu')],
        [Button.inline("📋 عرض الأدمنية", data='admin:list_admins_page_1'), Button.inline("🗑️ حذف الكل", data='admin:clear_admins_confirm')],
        [Button.inline("⬅️ رجوع", data='admin:main_menu')]
    ]

async def send_admins_menu(event: events.CallbackQuery.Event):
    text = "**⚙️ ⦗ قسم إدارة الأدمنية ⦘**\n\nإليك الخيارات المتاحة لإدارة طاقم العمل:"
    await safe_edit_message(event, text, buttons=get_admins_menu_buttons())

def get_ban_menu_buttons() -> List[List[Button]]:
    return [
        [Button.inline("➕ أضف محظور", data='admin:add_ban'), Button.inline("➖ حذف محظور", data='admin:rem_ban_menu')],
        [Button.inline("📋 عرض المحظورين", data='admin:list_banned_page_1'), Button.inline("🗑️ حذف الكل", data='admin:clear_banned_confirm')],
        [Button.inline("⬅️ رجوع", data='admin:main_menu')]
    ]

async def send_ban_menu(event: events.CallbackQuery.Event):
    text = "**🚫 ⦗ قسم إدارة الحظر ⦘**\n\nإليك الخيارات المتاحة لإدارة القائمة السوداء:"
    await safe_edit_message(event, text, buttons=get_ban_menu_buttons())

# --- Unified List View (Pagination) ---

async def list_users_paginated(event: events.CallbackQuery.Event, user_type: str, page: int):
    if user_type == "admins":
        users = load_admin_list()
        title = "الأدمنية"
        back_data = "admin:admins_menu"
        data_prefix = "admin:list_admins"
    else:
        users = load_banned_list()
        title = "المحظورين"
        back_data = "admin:ban_menu"
        data_prefix = "admin:list_banned"

    if not users:
        return await event.answer(f"⚠️ لا يوجد {title} حالياً.", alert=True)

    user_ids = list(users.keys())
    total_items = len(user_ids)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_items = user_ids[start_idx:end_idx]

    text = f"**📋 ⦗ قائمة {title} ({total_items}) ⦘**\n\n"
    for uid in current_items:
        text += await format_user_entry(uid, users[uid]) + "\n\n"
    
    text += f"صفحة `{page}` من `{total_pages}`"
    
    buttons = []
    nav_row = get_pagination_buttons(page, total_pages, data_prefix)
    if nav_row:
        buttons.append(nav_row)
    buttons.append([Button.inline("⬅️ رجوع", data=back_data)])
    
    await safe_edit_message(event, text, buttons=buttons)

# --- Unified Removal Menu (Buttons) ---

async def rem_user_menu(event: events.CallbackQuery.Event, user_type: str, page: int = 1):
    if user_type == "admins":
        users = load_admin_list()
        title = "الأدمنية"
        back_data = "admin:admins_menu"
        data_prefix = "admin:rem_admin_menu"
        type_prefix = "admin:rem_admin_id_"
    else:
        users = load_banned_list()
        title = "المحظورين"
        back_data = "admin:ban_menu"
        data_prefix = "admin:rem_ban_menu"
        type_prefix = "admin:rem_ban_id_"

    if not users:
        return await event.answer(f"⚠️ لا توجد قائمة {title} للحذف منها.", alert=True)

    user_ids = list(users.keys())
    total_items = len(user_ids)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_items = user_ids[start_idx:end_idx]

    text = (
        f"**➖ ⦗ حذف من {title} ⦘**\n\n"
        "إختر العضو من الأزرار بالأسفل للحذف، أو أرسل الـ ID/يوزرنيم مباشرة."
    )
    
    buttons = []
    for uid in current_items:
        name = users[uid].get('first_name', 'Unknown')
        buttons.append([Button.inline(f"❌ {name} ({uid})", data=f"{type_prefix}{uid}")])

    nav_row = get_pagination_buttons(page, total_pages, data_prefix)
    if nav_row:
        buttons.append(nav_row)
    
    buttons.append([Button.inline("⬅️ رجوع", data=back_data)])
    
    # Set state for manual input as well
    sender_id = event.sender_id
    state = "awaiting_admin_to_rem" if user_type == "admins" else "awaiting_user_to_unban"
    conversation_manager.set_state(sender_id, state, message_id=event.message_id)
    
    await safe_edit_message(event, text, buttons=buttons)

# --- Unified Clear All (Confirmation) ---

async def clear_users_confirm(event: events.CallbackQuery.Event, user_type: str):
    if user_type == "admins":
        users = load_admin_list()
        title = "الأدمنية"
        back_data = "admin:admins_menu"
        action_data = "admin:clear_admins_execute"
    else:
        users = load_banned_list()
        title = "المحظورين"
        back_data = "admin:ban_menu"
        action_data = "admin:clear_banned_execute"

    if not users:
        return await event.answer(f"⚠️ قائمة {title} فارغة بالفعل.", alert=True)

    count = len(users)
    text = (
        f"**⚠️ ⦗ تأكيد المسح الشامل ⦘**\n\n"
        f"هل أنت متأكد من رغبتك في حذف جميع {title}؟\n"
        f"📊 العدد الإجمالي: `{count}`"
    )
    
    if count <= 10:
        text += "\n\n**القائمة:**\n"
        for uid, info in users.items():
            text += f"- {info.get('first_name')} (`{uid}`)\n"
    
    buttons = [
        [Button.inline("✅ نعم، أحذف الكل", data=action_data)],
        [Button.inline("❌ إلغاء التراجع", data=back_data)]
    ]
    
    await safe_edit_message(event, text, buttons=buttons)

# --- Callbacks ---

async def admins_menu_callback(event: events.CallbackQuery.Event):
    if check_user_status(event.sender_id) != 'sudo':
        return await event.answer("🚫 هذه الميزة مخصصة للمالك فقط.", alert=True)
    await send_admins_menu(event)

async def ban_menu_callback(event: events.CallbackQuery.Event):
    if check_user_status(event.sender_id) in ['sudo', 'admin']:
        await send_ban_menu(event)
    else:
        await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)

async def add_admin_prompt(event: events.CallbackQuery.Event):
    if check_user_status(event.sender_id) != 'sudo':
        return await event.answer("🚫 هذه الميزة مخصصة للمالك فقط.", alert=True)
    conversation_manager.set_state(event.sender_id, "awaiting_admin_to_add", message_id=event.message_id)
    await safe_edit_message(event, "**➕ إضافة أدمن**\n\nأرسل الآن ID المستخدم، أو اليوزرنيم، أو قم بالرد على رسالته.", buttons=[[Button.inline("إلغاء ❌", data="admin:admins_menu")]])

async def add_ban_prompt(event: events.CallbackQuery.Event):
    if check_user_status(event.sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    conversation_manager.set_state(event.sender_id, "awaiting_user_to_ban", message_id=event.message_id)
    await safe_edit_message(event, "**➕ إضافة محظور**\n\nأرسل الآن ID المستخدم، أو اليوزرنيم، أو قم بالرد على رسالته.", buttons=[[Button.inline("إلغاء ❌", data="admin:ban_menu")]])

async def generic_id_removal_callback(event: events.CallbackQuery.Event, user_type: str):
    uid = event.pattern_match.group(1).decode()
    if user_type == "admins":
        if check_user_status(event.sender_id) != 'sudo':
            return await event.answer("🚫 المالك فقط يمكنه حذف الأدمنية.", alert=True)
        users = load_admin_list()
        if uid in users:
            name = users[uid].get('first_name', uid)
            del users[uid]
            save_admin_list(users)
            await event.answer(f"✅ تم حذف {name} من الأدمنية.", alert=True)
        await rem_user_menu(event, "admins")
    else:
        users = load_banned_list()
        if uid in users:
            name = users[uid].get('first_name', uid)
            del users[uid]
            save_banned_list(users)
            await event.answer(f"✅ تم رفع الحظر عن {name}.", alert=True)
        await rem_user_menu(event, "banned")

# --- Conversation Handler ---
async def admin_users_conversation_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    state_data = conversation_manager.get_state(sender_id)
    state_status = state_data.get('status')
    message_id_to_edit = state_data.get('message_id')
    
    sudo_only_states = ["awaiting_admin_to_add", "awaiting_admin_to_rem"]
    if state_status in sudo_only_states and check_user_status(sender_id) != 'sudo':
        await event.reply("🚫 هذه الميزة مخصصة للمالك فقط.")
        conversation_manager.delete_state(sender_id)
        return

    async def restore_panel(menu_func, *args):
        if message_id_to_edit:
            try:
                mock_event = await event.client.get_messages(sender_id, ids=message_id_to_edit)
                if mock_event:
                    await menu_func(mock_event, *args)
            except Exception:
                await event.reply("اكتمل الإجراء.")

    user_input = event.text
    if event.is_reply:
        reply = await event.get_reply_message()
        user_input = reply.sender_id
    
    user_info = await get_user_info(user_input)
    if not user_info:
        await event.reply("❌ لم أتمكن من العثور على هذا المستخدم.")
        return

    uid_str = str(user_info['id'])
    name = user_info['first_name']
    mention = f"[{name}](tg://user?id={uid_str})"

    if state_status == "awaiting_admin_to_add":
        admins = load_admin_list()
        admins[uid_str] = {"first_name": name, "username": user_info['username']}
        save_admin_list(admins)
        await event.reply(f"✅ تم إضافة {mention} إلى الأدمنية.")
        conversation_manager.delete_state(sender_id)
        await restore_panel(send_admins_menu)

    elif state_status == "awaiting_admin_to_rem":
        admins = load_admin_list()
        if uid_str in admins:
            del admins[uid_str]
            save_admin_list(admins)
            await event.reply(f"✅ تم حذف {mention} من الأدمنية.")
        else:
            await event.reply("ℹ️ العضو ليس أدمن.")
        conversation_manager.delete_state(sender_id)
        await restore_panel(send_admins_menu)

    elif state_status == "awaiting_user_to_ban":
        banned = load_banned_list()
        banned[uid_str] = {"first_name": name, "username": user_info['username']}
        save_banned_list(banned)
        await event.reply(f"✅ تم حظر {mention}.")
        conversation_manager.delete_state(sender_id)
        await restore_panel(send_ban_menu)

    elif state_status == "awaiting_user_to_unban":
        banned = load_banned_list()
        if uid_str in banned:
            del banned[uid_str]
            save_banned_list(banned)
            await event.reply(f"✅ رفع الحظر عن {mention}.")
        else:
            await event.reply("ℹ️ العضو غير محظور.")
        conversation_manager.delete_state(sender_id)
        await restore_panel(send_ban_menu)

def setup(client_instance: "TelegramClient"):
    # Main Menus
    client_instance.on(events.CallbackQuery(pattern=b'admin:admins_menu'))(admins_menu_callback)
    client_instance.on(events.CallbackQuery(pattern=b'admin:ban_menu'))(ban_menu_callback)

    # List Actions (Pagination)
    @client_instance.on(events.CallbackQuery(pattern=rb'admin:list_admins_page_(\d+)'))
    async def list_admins_page_callback(e):
        page = int(e.pattern_match.group(1).decode())
        await list_users_paginated(e, "admins", page)

    @client_instance.on(events.CallbackQuery(pattern=rb'admin:list_banned_page_(\d+)'))
    async def list_banned_page_callback(e):
        page = int(e.pattern_match.group(1).decode())
        await list_users_paginated(e, "banned", page)

    # Removal Actions
    @client_instance.on(events.CallbackQuery(pattern=rb'admin:rem_admin_menu(?:_page_(\d+))?'))
    async def rem_admin_menu_callback(e):
        page_match = e.pattern_match.group(1)
        page = int(page_match.decode()) if page_match else 1
        await rem_user_menu(e, "admins", page)

    @client_instance.on(events.CallbackQuery(pattern=rb'admin:rem_ban_menu(?:_page_(\d+))?'))
    async def rem_ban_menu_callback(e):
        page_match = e.pattern_match.group(1)
        page = int(page_match.decode()) if page_match else 1
        await rem_user_menu(e, "banned", page)

    client_instance.on(events.CallbackQuery(pattern=rb'admin:rem_admin_id_(\d+)'))(lambda e: generic_id_removal_callback(e, "admins"))
    client_instance.on(events.CallbackQuery(pattern=rb'admin:rem_ban_id_(\d+)'))(lambda e: generic_id_removal_callback(e, "banned"))

    # Clear Actions
    client_instance.on(events.CallbackQuery(pattern=b'admin:clear_admins_confirm'))(lambda e: clear_users_confirm(e, "admins"))
    client_instance.on(events.CallbackQuery(pattern=b'admin:clear_banned_confirm'))(lambda e: clear_users_confirm(e, "banned"))
    
    @client_instance.on(events.CallbackQuery(pattern=b'admin:clear_admins_execute'))
    async def clear_admins_exec(e):
        save_admin_list({})
        await e.answer("🗑️ تم تصفير الأدمنية.", alert=True)
        await send_admins_menu(e)
    
    @client_instance.on(events.CallbackQuery(pattern=b'admin:clear_banned_execute'))
    async def clear_banned_exec(e):
        save_banned_list({})
        await e.answer("🗑️ تم تصفير المحظورين.", alert=True)
        await send_ban_menu(e)

    # Prompts
    client_instance.on(events.CallbackQuery(pattern=b'admin:add_admin'))(add_admin_prompt)
    client_instance.on(events.CallbackQuery(pattern=b'admin:add_ban'))(add_ban_prompt)

    # Conversation
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.has_state(e.sender_id) and conversation_manager.get_status(e.sender_id) in ["awaiting_admin_to_add", "awaiting_admin_to_rem", "awaiting_user_to_ban", "awaiting_user_to_unban"]))(admin_users_conversation_handler)
    print("✅ Admin User/Admin Management handlers registered.")
