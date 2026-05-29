# bot_v2/bot/handlers/files.py
# This module handles all file and folder management features for users.

import os
import shutil
import re
import zipfile
import html
import hashlib
import tempfile
import asyncio
from datetime import datetime
from urllib.parse import quote
from typing import List, Tuple, Dict, Any, Optional, TYPE_CHECKING

from telethon import events
from telethon.tl.custom import Button
from telethon.tl.types import KeyboardButtonCallback
from telethon.tl import types as telethon_types
from telethon.extensions import html as telethon_html
from cryptography.fernet import Fernet # Import encryption
from telebot import TeleBot
import telebot.types as telebot_types
from bot.services.telegram import send_message_to_admin

# Telebot types for compatibility (we'll convert to Telethon)
class TelebotButton:
    """Compatibility wrapper for telebot-style buttons"""
    def __init__(self, text, callback_data=None, web_app=None):
        self.text = text
        self.callback_data = callback_data
        self.web_app = web_app

class TelebotMarkup:
    """Compatibility wrapper for telebot-style markup"""
    def __init__(self, row_width=2):
        self.keyboard = []
        self.row_width = row_width
        self.current_row = []
        self.has_webapp = False
    
    def add(self, *buttons):
        for btn in buttons:
            if btn.web_app:
                self.has_webapp = True
            self.current_row.append(btn)
            if len(self.current_row) >= self.row_width:
                self.keyboard.append(self.current_row)
                self.current_row = []
        if self.current_row and len(buttons) == 1:
            self.keyboard.append(self.current_row)
            self.current_row = []
    
    def to_telethon(self):
        """Convert to Telethon buttons"""
        if self.current_row:
            self.keyboard.append(self.current_row)
            self.current_row = []
        
        telethon_buttons = []
        for row in self.keyboard:
            button_row = []
            for btn in row:
                if btn.web_app:
                    # WebApp buttons - use URL button as fallback
                    button_row.append(Button.url(btn.text, btn.web_app.url))
                else:
                    callback = btn.callback_data
                    if isinstance(callback, bytes):
                        callback = callback.decode()
                    button_row.append(Button.inline(btn.text, callback))
            telethon_buttons.append(button_row)
        return telethon_buttons
    
    def to_telebot(self):
        """Convert to Telebot markup for WebApp support"""
        if self.current_row:
            self.keyboard.append(self.current_row)
            self.current_row = []
        
        telebot_markup = telebot_types.InlineKeyboardMarkup()
        for row in self.keyboard:
            button_row = []
            for btn in row:
                if btn.web_app:
                    # Real WebApp button
                    button_row.append(telebot_types.InlineKeyboardButton(
                        text=btn.text,
                        web_app=telebot_types.WebAppInfo(url=btn.web_app.url)
                    ))
                else:
                    callback = btn.callback_data
                    if isinstance(callback, bytes):
                        callback = callback.decode()
                    button_row.append(telebot_types.InlineKeyboardButton(
                        text=btn.text,
                        callback_data=callback
                    ))
            telebot_markup.row(*button_row)
        return telebot_markup

class TelebotWebAppInfo:
    def __init__(self, url):
        self.url = url

# Create compatibility namespace
class types:
    InlineKeyboardButton = TelebotButton
    InlineKeyboardMarkup = TelebotMarkup
    WebAppInfo = TelebotWebAppInfo

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_all_users, save_all_users, load_host_settings, load_bots_data, save_bots_data
from bot.core.state import conversation_manager
from bot.utils.telegram import safe_edit_message
from bot.services.user_service import check_user_status, get_user_data, save_user_data
from bot.core.database import increment_stat
from bot.services.file_service import get_user_root, get_current_path, set_current_path, user_current_working_directory, USER_BOTS_ROOT_DIR
from bot.services.quota_service import get_user_usage, get_quota_limits, can_add_files
from bot.services.telegram import delete_webhook_for_token, set_webhook_for_token

# --- Developer Logger Import ---
from bot.utils.dev_logger import log_step
from bot.utils.text import generate_recursive_tree_view

# --- Centralized Navigation System ---
from bot.core.navigation import create_nav_button_data, resolve_nav_data

# --- Cache for Delete Confirmations ---
DELETE_CONFIRMATION_CACHE = {}

async def cleanup_delete_cache(key: str, delay: int = 600): # 10 minutes
    """Removes a delete confirmation entry from the cache after a delay."""
    await asyncio.sleep(delay)
    if key in DELETE_CONFIRMATION_CACHE:
        del DELETE_CONFIRMATION_CACHE[key]

def get_hashed_data(prefix: str, file_name: str) -> bytes:
    return create_nav_button_data(prefix, file_name)

def resolve_file_data(data_str: str) -> str:
    return resolve_nav_data(data_str)

# --- Helper Functions ---

def validate_name(name: str, name_type: str = "folder") -> Tuple[bool, str]:
    """
    Validates folder/file names for security and compatibility.
    
    Args:
        name: The name to validate
        name_type: "folder" or "file" for better error messages
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, f"❌ اسم {name_type} فارغ."
    
    name = name.strip()
    
    # Prevent starting with dot (hidden files/folders)
    if name.startswith('.'):
        return False, f"❌ لا يمكن إنشاء {name_type} مخفي (يبدأ بـ `.`)."
    
    # Allow letters, numbers, hyphens, underscores, and dots
    # For files, also allow extension dots
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', name):
        return False, f"❌ اسم {name_type} غير صالح. يمكنك استخدام حروف، أرقام، `-`، `_`، و `.` فقط."
    
    # Prevent path traversal
    if '..' in name:
        return False, f"❌ لا يمكن استخدام `..` في اسم {name_type}."
    
    # Prevent Windows reserved names
    reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                     'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                     'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    base_name = name.split('.')[0].upper()  # Check name without extension
    if base_name in reserved_names:
        return False, f"❌ اسم {name_type} محجوز من قبل النظام. اختر اسماً آخر."
    
    # Length check
    if len(name) > 255:
        return False, f"❌ اسم {name_type} طويل جداً (الحد الأقصى 255 حرف)."
    
    return True, ""

def generate_tree_view(path: str, prefix: str = "") -> str:
    """Recursively generates a tree view string for a given path."""
    tree_string = ""
    try:
        items = sorted(os.listdir(path))
    except FileNotFoundError:
        return " (المجلد الرئيسي غير موجود) "

    # Separate directories and files to list directories first
    dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
    files = [item for item in items if not os.path.isdir(os.path.join(path, item)) and item.endswith(('.php', '.json', '.txt'))] # Filter by allowed extensions

    # List directories
    for i, item in enumerate(dirs):
        is_last = (i == len(dirs) - 1) and (len(files) == 0)
        tree_string += f"{prefix}{'└── ' if is_last else '├── '}{item}/\n"

    # List files
    for i, item in enumerate(files):
        is_last = (i == len(files) - 1)
        tree_string += f"{prefix}{'└── ' if is_last else '├── '}{item}\n"

    return tree_string

# ===== وضع المطور (Developer Mode) =====
DEV_MODE = True  # اجعلها False لإيقاف التسجيل التفصيلي
ACTION_LOG_FILE = os.path.join(settings.PROJECT_ROOT, 'data', 'bot_actions_log.txt')
ACTION_LOG_FILE = os.path.join(settings.PROJECT_ROOT, 'data', 'files_log.txt')

async def log_action(action: str, details: str):
    """تسجيل الأحداث في وضع المطور"""
    if not DEV_MODE:
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{action}] {details}\n"
    
    # طباعة في الكونسول وكتابة في الملف
    print(f"📝 {action}: {details}")
    try:
        with open(ACTION_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_message)
    except Exception as e:
        print(f"❌ Failed to write to log: {e}")


async def generate_hosting_view(user_id: int) -> Tuple[str, List[List[Button]]]:
    """Generates the message text and buttons for the 'My Hosting' view."""
    current_path = get_current_path(user_id)
    user_root = get_user_root(user_id)
    
    # Get upload folder from user settings, default to root
    user_data = get_user_data(user_id)
    default_upload_folder = user_data.get('upload_folder', user_root)
    if not os.path.exists(default_upload_folder):
        default_upload_folder = user_root

    # --- List and filter contents ---
    try:
        items = os.listdir(current_path)
    except FileNotFoundError:
        # If current_path somehow disappeared, reset to user_root
        user_current_working_directory[user_id] = user_root
        current_path = user_root
        items = os.listdir(current_path)

    folders = sorted([item for item in items if os.path.isdir(os.path.join(current_path, item))])
    
    host_settings = load_host_settings()
    allowed_extensions_list = []
    if host_settings.get('allow_php', True): allowed_extensions_list.append('.php')
    if host_settings.get('allow_json', True): allowed_extensions_list.append('.json')
    if host_settings.get('allow_txt', True): allowed_extensions_list.append('.txt')

    allowed_files = sorted([item for item in items if not os.path.isdir(os.path.join(current_path, item)) and os.path.splitext(item)[1].lower() in allowed_extensions_list])


    # --- Create Buttons ---
    buttons: List[List[Button]] = []
    # File and folder buttons
    for folder in folders:
        folder_icon = "📁"
        try:
            if os.listdir(os.path.join(current_path, folder)):
                folder_icon = "🗂"
        except OSError: pass
        buttons.append([Button.inline(f"{folder_icon} {folder}", data=get_hashed_data("nav", folder))])
    for file in allowed_files:
        icon = "📄"
        if file.endswith('.php'): icon = "🐘"
        elif file.endswith('.json'): icon = "📜"
        elif file.endswith('.txt'): icon = "📝"
        buttons.append([Button.inline(f"{icon} {file}", data=get_hashed_data("file", file))])

    # --- Action Buttons ---
    management_buttons = [
        Button.inline("➕ انشاء مجلد", data="create_folder"),
        Button.inline("🗑️ حذف مجلد", data="delete_folder")
    ]
    buttons.append(management_buttons)
    
    # Clean Folder Button (New)
    buttons.append([Button.inline("🧹 تنظيف المجلد", data="clean_folder_prompt")])

    # Set Upload Folder Button (Moved to its own row)
    if current_path != default_upload_folder:
        buttons.append([Button.inline("📥 تعيين كمجلد للرفع", data="set_upload_folder")])
    
    # Bottom Actions (Zip / Delete This Folder)
    bottom_actions = []
    bottom_actions.append(Button.inline("📦 تحميل المجلد (Zip)", data="zip_current_folder"))
    # Add button to delete the current folder, but not the root
    if current_path != user_root:
        bottom_actions.append(Button.inline("🚮 حذف هذا المجلد", data="delete_this_folder"))
    buttons.append(bottom_actions)

    # --- Navigation Buttons ---
    nav_buttons = []
    if current_path != user_root:
        nav_buttons.append(Button.inline("⬆️ رجوع", data="nav:.."))
    nav_buttons.append(Button.inline("↩️ القائمة الرئيسية", data="main_menu"))
    buttons.append(nav_buttons)

    # --- Create Message Text ---
    relative_path = os.path.relpath(current_path, USER_BOTS_ROOT_DIR)
    display_path = f"./{relative_path}"
    display_path_escaped = html.escape(display_path)

    usage = get_user_usage(user_id)
    limits = get_quota_limits(user_id)
    
    storage_used_mb = usage['total_bytes'] / (1024 * 1024)
    storage_percent = (storage_used_mb / limits['max_storage_mb']) * 100 if limits['max_storage_mb'] > 0 else 0
    
    # Usage Bar / Info
    usage_info = (
        f"📊 <b>الاستهلاك:</b> <code>{storage_used_mb:.2f}/{limits['max_storage_mb']} MB</code> ({storage_percent:.1f}%)\n"
        f"📄 <b>الملفات:</b> <code>{usage['file_count']}/{limits['max_files']}</code> | "
        f"📁 <b>المجلدات:</b> <code>{usage['folder_count']}/{limits['max_folders']}</code>\n\n"
    )

    tree_view = generate_tree_view(current_path)
    message_text = f"<b>🗂️ استضافتي</b>\n\n{usage_info}<b>الموقع الحالي:</b> <code>{display_path_escaped}</code>\n\n"
    
    if storage_used_mb >= limits['max_storage_mb'] * 0.9:
        message_text += "⚠️ <b>تحذير: شارفت مساحة التخزين على الامتلاء!</b>\n\n"

    if current_path == default_upload_folder:
        message_text += "<blockquote>✨ هذا هو مجلد الرفع الافتراضي.</blockquote>\n\n"

    if tree_view:
        tree_view_escaped = html.escape(tree_view)
        root_name_escaped = html.escape(os.path.basename(display_path))
        message_text += f"<pre>{root_name_escaped}/\n{tree_view_escaped}</pre>\n"
    else:
        message_text += "<i>المجلد فارغ.</i>\n"
    
    return message_text, buttons


async def my_hosting_handler(event: events.CallbackQuery.Event):
    """Handles displaying the user's hosting directory and file tree."""
    sender_id = event.sender_id
    # check_user_status will be imported from bot.handlers.admin.users or a service
    user_status = check_user_status(sender_id) # Placeholder
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
        
    message_text, buttons = await generate_hosting_view(sender_id)
    await safe_edit_message(event, message_text, buttons=buttons, parse_mode='html')


async def navigate_handler(event: events.CallbackQuery.Event):
    """Handles folder navigation."""
    sender_id = event.sender_id
    user_status = check_user_status(sender_id) # Placeholder
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
        
    raw_data = event.data.decode('utf-8').split(':', 1)[1]
    destination = resolve_file_data(raw_data)

    # Update the user's current path
    new_path = set_current_path(sender_id, destination)
    if new_path is None:
        return await event.answer("❌ لا يمكن الوصول إلى هذا المسار.", alert=True)

    # Regenerate and display the new view
    message_text, buttons = await generate_hosting_view(sender_id)
    await safe_edit_message(event, message_text, buttons=buttons, parse_mode='html')


async def create_folder_prompt_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    current_path = get_current_path(sender_id)
    usage = get_user_usage(sender_id)
    limits = get_quota_limits(sender_id)

    if usage['folder_count'] >= limits['max_folders']:
        return await event.answer(f"❌ لقد وصلت إلى الحد الأقصى للمجلدات المسموح بها لهذه الفئة ({limits['max_folders']}).", alert=True)


    conversation_manager.set_state(sender_id, "awaiting_folder_name", message_id=event.message_id)
    await safe_edit_message(
        event,
        "**➕ إنشاء مجلد جديد:**\n\nأرسل الآن اسم المجلد الذي تريد إنشاءه.",
        buttons=[[Button.inline("❌ إلغاء", data="cancel_action")]]
    )

async def delete_folder_prompt_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    current_path = get_current_path(sender_id)
    try:
        items = sorted(os.listdir(current_path))
    except OSError:
        return await event.answer("❌ لا يمكن الوصول للمجلد.", alert=True)

    dirs = [d for d in items if os.path.isdir(os.path.join(current_path, d))]

    if not dirs:
        return await event.answer("📂 لا توجد مجلدات فرعية للحذف.", alert=True)

    buttons = []
    for d in dirs:
        buttons.append([Button.inline(f"🗑️ {d}", data=f"del_sub:{d}")])
    
    buttons.append([Button.inline("❌ إلغاء", data="my_hosting")])

    await safe_edit_message(event, "**🗑️ حذف مجلد فرعي:**\n\nاختر المجلد الذي تريد حذفه:", buttons=buttons)

# Message handler for creating/deleting folders
async def folder_conversation_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    status = state.get('status')
    message_id_to_edit = state.get('message_id')
    folder_name = event.text.strip()
    current_path = get_current_path(sender_id)
    target_path = os.path.join(current_path, folder_name)

    if status == "awaiting_folder_name":
        # Validate folder name
        is_valid, error_msg = validate_name(folder_name, "المجلد")
        if not is_valid:
            await event.reply(error_msg)
            return

        if os.path.exists(target_path):
            await event.reply("❌ مجلد بهذا الاسم موجود بالفعل.")
            return

        can_add, reason = can_add_files(sender_id, new_folders=1)
        if not can_add:
            await event.reply(f"❌ **لا يمكن إنشاء المجلد:** {reason}")
            return

        try:
            os.makedirs(target_path)
            try: os.chmod(target_path, 0o777)
            except: pass
            await increment_stat(sender_id, 'folders_created')
            await event.reply(f"✅ تم إنشاء المجلد `{folder_name}` بنجاح.")
        except Exception as e:
            await event.reply(f"❌ فشل إنشاء المجلد: {e}")
        
    elif status == "awaiting_folder_to_delete":
        if not folder_name:
            await event.reply("❌ يرجى إرسال اسم مجلد صالح.")
            return

        if not os.path.exists(target_path) or not os.path.isdir(target_path):
            await event.reply("❌ المجلد غير موجود.")
            return

        user_root = get_user_root(sender_id)
        # Security: ensure folder to delete is within user's root and not the root itself
        if os.path.commonpath([user_root, target_path]) != user_root or target_path == user_root:
            await event.reply("🚫 لا يمكنك حذف هذا المجلد (غير مصرح به).")
            return

        try:
            shutil.rmtree(target_path) # Remove directory and all its contents
            await increment_stat(sender_id, 'folders_deleted')
            await event.reply(f"✅ تم حذف المجلد `{folder_name}` بنجاح.")
        except Exception as e:
            await event.reply(f"❌ فشل حذف المجلد: {e}")
    
    conversation_manager.delete_state(sender_id)
    # Refresh the hosting view
    message_text, buttons = await generate_hosting_view(sender_id)
    # Edit the original message to show the updated view
    if message_id_to_edit:
        try:
            status_msg = await event.client.get_messages(sender_id, ids=message_id_to_edit)
            await safe_edit_message(status_msg, message_text, buttons=buttons, parse_mode='html')
        except Exception as e:
            print(f"Error editing message after folder op: {e}")
            await event.reply(message_text, buttons=buttons, parse_mode='html')
    else:
        await event.reply(message_text, buttons=buttons, parse_mode='html')


async def set_upload_folder_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    current_path = get_current_path(sender_id)
    user_data = get_user_data(sender_id)
    user_data['upload_folder'] = current_path
    save_user_data(sender_id, user_data)
    await event.answer("✅ تم تعيين هذا المجلد كمجلد الرفع الافتراضي.", alert=True)
    
    # Refresh the view
    message_text, buttons = await generate_hosting_view(sender_id)
    await safe_edit_message(event, message_text, buttons=buttons, parse_mode='html')


async def delete_this_folder_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    current_path = get_current_path(sender_id)
    user_root = get_user_root(sender_id)

    if current_path == user_root:
        return await event.answer("❌ لا يمكنك حذف المجلد الرئيسي!", alert=True)

    # Generate recursive tree view for confirmation
    tree_text = generate_recursive_tree_view(current_path)
    
    # Check Telegram limits (approx 4096 chars). Reserve space for headers.
    MAX_TREE_LEN = 3000
    if len(tree_text) > MAX_TREE_LEN:
        tree_text = tree_text[:MAX_TREE_LEN] + "\n... (تم القص لتجاوز الحد)"

    folder_name = os.path.basename(current_path)
    
    msg = (
        f"<b>🗑️ حذف المجلد الحالي</b>\n\n"
        f"المسار: <code>{html.escape(folder_name)}</code>\n\n"
        f"<b>محتويات المجلد:</b>\n"
        f"<blockquote expandable>{html.escape(tree_text)}</blockquote>\n\n"
        f"⚠️ <b>هل أنت متأكد؟</b> سيتم حذف المجلد وكل ما بداخله نهائياً."
    )

    buttons = [
        [Button.inline("✅ نعم، احذف نهائياً", data="confirm_delete_this_folder")],
        [Button.inline("❌ إلغاء", data="my_hosting")]
    ]
    
    # Use manual parsing for expandable blockquote
    parsed_text, entities = telethon_html.parse(msg)
    for entity in entities:
        if isinstance(entity, telethon_types.MessageEntityBlockquote):
            entity.collapsed = True
            
    await safe_edit_message(event, parsed_text, buttons=buttons, parse_mode=None, entities=entities)

async def confirm_delete_this_folder_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    current_path = get_current_path(sender_id)
    user_root = get_user_root(sender_id)

    if current_path == user_root:
        return await event.answer("❌ لا يمكنك حذف المجلد الرئيسي!", alert=True)

    # --- Stop and remove any bots running within this folder ---
    from bot.core.data_manager import load_bots_data, save_bots_data # Import dynamically
    bots_data = load_bots_data()
    tokens_to_remove = []
    for token, info in bots_data.items():
        # Ensure target_path is absolute for commonpath comparison
        target_path = info.get('path', '')
        if not os.path.isabs(target_path):
            target_path = os.path.join(USER_BOTS_ROOT_DIR, target_path)

        if info.get('owner') == sender_id and os.path.commonpath([current_path]) == os.path.commonpath([current_path, target_path]):
            tokens_to_remove.append(token)
    
    if tokens_to_remove:
        for token in tokens_to_remove:
            del bots_data[token]
        save_bots_data(bots_data)
        await event.answer(f"ℹ️ تم إيقاف وحذف {len(tokens_to_remove)} بوتات كانت تعمل داخل المجلد.", alert=True)

    # Navigate up one level before deleting
    parent_path = os.path.dirname(current_path)
    user_current_working_directory[sender_id] = parent_path

    # --- Delete the folder ---
    try:
        shutil.rmtree(current_path)
        await increment_stat(sender_id, 'folders_deleted')
        await event.answer(f"🗑️ تم حذف المجلد بنجاح.", alert=False)
    except OSError as e:
        await event.answer(f"❌ فشل حذف المجلد", alert=True)
        # Log to admin
        for admin_id in settings.telegram.SUDO_USERS:
            if not await send_message_to_admin(admin_id, f"⚠️ حدث خطأ أثناء حذف مجلد\n👤 المستخدم: {sender_id}\n📁 المسار: {current_path}\n💥 الخطأ: {e}"):
                print(f"Failed to notify admin {admin_id} about folder deletion")


    # Regenerate and display the new view from the parent directory
    message_text, buttons = await generate_hosting_view(sender_id)
    await safe_edit_message(event, message_text, buttons=buttons, parse_mode='html')

async def select_subfolder_to_delete_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    folder_name = event.data.decode('utf-8').split(':', 1)[1]
    current_path = get_current_path(sender_id)
    target_path = os.path.join(current_path, folder_name)

    if not os.path.exists(target_path) or not os.path.isdir(target_path):
        return await event.answer("❌ المجلد غير موجود.", alert=True)

    # Generate recursive tree view for confirmation
    tree_text = generate_recursive_tree_view(target_path)
    
    MAX_TREE_LEN = 3000
    if len(tree_text) > MAX_TREE_LEN:
        tree_text = tree_text[:MAX_TREE_LEN] + "\n... (تم القص لتجاوز الحد)"

    msg = (
        f"<b>🗑️ حذف المجلد:</b> <code>{html.escape(folder_name)}</code>\n\n"
        f"<b>محتويات المجلد:</b>\n"
        f"<blockquote expandable>{html.escape(tree_text)}</blockquote>\n\n"
        f"⚠️ <b>هل أنت متأكد؟</b> سيتم حذف المجلد وكل ما بداخله نهائياً."
    )

    buttons = [
        [Button.inline("✅ نعم، احذف نهائياً", data=f"conf_del_sub:{folder_name}")],
        [Button.inline("❌ إلغاء", data="delete_folder")] # Return to folder list
    ]
    
    # Use manual parsing for expandable blockquote
    parsed_text, entities = telethon_html.parse(msg)
    for entity in entities:
        if isinstance(entity, telethon_types.MessageEntityBlockquote):
            entity.collapsed = True
            
    await safe_edit_message(event, parsed_text, buttons=buttons, parse_mode=None, entities=entities)

async def confirm_delete_subfolder_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    folder_name = event.data.decode('utf-8').split(':', 1)[1]
    current_path = get_current_path(sender_id)
    target_path = os.path.join(current_path, folder_name)
    user_root = get_user_root(sender_id)

    if not os.path.exists(target_path):
         return await event.answer("❌ المجلد غير موجود.", alert=True)

    # --- Stop and remove any bots running within this folder ---
    from bot.core.data_manager import load_bots_data, save_bots_data
    bots_data = load_bots_data()
    tokens_to_remove = []
    for token, info in bots_data.items():
        target_bot_path = info.get('path', '')
        if not os.path.isabs(target_bot_path):
            target_bot_path = os.path.join(USER_BOTS_ROOT_DIR, target_bot_path)

        if info.get('owner') == sender_id:
             try:
                 if os.path.commonpath([target_path, target_bot_path]) == target_path:
                     tokens_to_remove.append(token)
             except ValueError:
                 pass
    
    if tokens_to_remove:
        for token in tokens_to_remove:
            del bots_data[token]
        save_bots_data(bots_data)
        await event.answer(f"ℹ️ تم إيقاف وحذف {len(tokens_to_remove)} بوتات كانت تعمل داخل المجلد.", alert=True)

    try:
        shutil.rmtree(target_path)
        await increment_stat(sender_id, 'folders_deleted')
        await event.answer(f"🗑️ تم حذف المجلد {folder_name} بنجاح.", alert=False)
    except OSError as e:
        await event.answer(f"❌ فشل حذف المجلد", alert=True)

    # Regenerate and display the new view
    message_text, buttons = await generate_hosting_view(sender_id)
    await safe_edit_message(event, message_text, buttons=buttons, parse_mode='html')

async def zip_current_folder_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    current_path = get_current_path(sender_id)
    folder_name = os.path.basename(current_path) or "root"
    
    if not os.listdir(current_path):
        return await event.answer("📂 المجلد فارغ.", alert=True)

    await event.answer("📦 جاري ضغط المجلد...", cache_time=0) # No cache for "in progress" messages
    
    # Create a temporary directory to store the zip file
    temp_dir = tempfile.mkdtemp()
    base_name = os.path.join(temp_dir, folder_name)
    
    try:
        # Run blocking make_archive in executor to avoid blocking the event loop
        zip_file_path = await asyncio.to_thread(
            shutil.make_archive,
            base_name,
            'zip',
            root_dir=current_path
        )
        
        await client.send_file(
            sender_id,
            zip_file_path,
            caption=f"📦 **نسخة احتياطية للمجلد:** `{folder_name}`",
            force_document=True
        )
    except Exception as e:
        print(f"Error zipping folder {current_path}: {e}")
        await event.answer("❌ فشل ضغط المجلد.", alert=True)
    finally:
        # Clean up the temporary directory and its contents
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


async def download_file_handler(event: events.CallbackQuery.Event):
    """Handles the request to download a specific file."""
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    raw_data = event.data.decode('utf-8').split(':', 1)[1]
    file_name = resolve_file_data(raw_data)
    current_path = get_current_path(sender_id)
    file_path = os.path.join(current_path, file_name)
    user_root = get_user_root(sender_id)

    # --- حماية ملف host_bootstrap.php من الحذف ---
    if file_name == 'host_bootstrap.php' and current_path == user_root:
        return await event.answer("🚫 لا يمكن حذف ملف النظام هذا (host_bootstrap.php).", alert=True)
    # ---------------------------------------------

    if not os.path.exists(file_path):
        return await event.answer("❌ الملف لم يعد موجوداً!", alert=True)

    try:
        await event.answer(f"📥 جاري إرسال الملف `{file_name}`...")
        await client.send_file(sender_id, file_path, force_document=True)
        await increment_stat(sender_id, 'file_downloads')
    except Exception as e:
        await event.answer(f"❌ فشل إرسال الملف: {e}", alert=True)


async def delete_file_handler(event: events.CallbackQuery.Event):
    """Asks for confirmation before deleting a file."""
    data_content = event.pattern_match.group(1).decode()
    parts = data_content.split(':')
    # Resolve the filename from the hash if present
    file_name = resolve_file_data(parts[0])
    
    # التحقق من حالة زر اختيار حذف البوت (Toggle)
    delete_bot_record = False
    if len(parts) > 1:
        delete_bot_record = parts[1] == '1'
    
    sender_id = event.sender_id
    current_path = get_current_path(sender_id)
    file_path = os.path.join(current_path, file_name)
    
    # فحص هل الملف مرتبط ببوت مسجل؟
    bots_data = load_bots_data()
    rel_path = os.path.relpath(file_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')
    
    associated_token = None
    for token, info in bots_data.items():
        if info.get('path') == rel_path and info.get('owner') == sender_id:
            associated_token = token
            break
            
    buttons = []
    
    if associated_token:
        # زر التبديل (Toggle Button)
        icon = "✅" if delete_bot_record else "⬜"
        next_state = "0" if delete_bot_record else "1"
        # نستخدم نفس الهاندلر لعمل تحديث للقائمة
        buttons.append([
            Button.inline(f"{icon} حذف سجل البوت والتوكن", data=f"delete_file:{parts[0]}:{next_state}")
        ])
    
    # تمرير حالة الحذف للزر النهائي
    # --- FIX: Use a hash key to avoid exceeding 64-byte limit ---
    unique_key = hashlib.sha1(f"{sender_id}:{file_path}:{delete_bot_record}".encode()).hexdigest()[:16]
    DELETE_CONFIRMATION_CACHE[unique_key] = {
        'file_path': file_path,
        'delete_bot_record': delete_bot_record,
        'owner_id': sender_id
    }
    asyncio.create_task(cleanup_delete_cache(unique_key))

    confirm_data = f"confirm_delete_hashed:{unique_key}"
    
    buttons.append([
        Button.inline("✅ نعم، احذف", data=confirm_data),
        Button.inline("❌ لا، تراجع", data=get_hashed_data("file", file_name))
    ])

    msg = f"**🗑️ هل أنت متأكد أنك تريد حذف الملف `{file_name}` نهائياً؟**"
    if associated_token:
        msg += "\n\n⚠️ **تنبيه:** هذا الملف مرتبط ببوت مسجل."
        if delete_bot_record:
            msg += "\n🗑️ **سيتم حذف سجل البوت والتوكن من قاعدة البيانات.**"
        else:
            msg += "\nℹ️ سيتم حذف الملف فقط (سيبقى السجل في قاعدة البيانات)."

    await safe_edit_message(event, msg, buttons=buttons)

async def confirm_delete_by_hash_handler(event: events.CallbackQuery.Event):
    """Deletes the file after confirmation using a cached key."""
    sender_id = event.sender_id
    key = event.pattern_match.group(1).decode()

    if key not in DELETE_CONFIRMATION_CACHE:
        return await event.answer("⚠️ انتهت صلاحية جلسة الحذف هذه. يرجى المحاولة مرة أخرى.", alert=True)

    cache_entry = DELETE_CONFIRMATION_CACHE.pop(key)

    if cache_entry.get('owner_id') != sender_id:
        DELETE_CONFIRMATION_CACHE[key] = cache_entry
        return await event.answer("🚫 هذا الطلب لا يخصك.", alert=True)

    file_path = cache_entry['file_path']
    delete_bot_record = cache_entry['delete_bot_record']
    file_name = os.path.basename(file_path)

    token_msg = ""
    
    # --- منطق حذف سجل البوت إذا تم تحديده ---
    if delete_bot_record:
        bots_data = load_bots_data()
        rel_path = os.path.relpath(file_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')
        
        token_to_remove = None
        for token, info in bots_data.items():
            if info.get('path') == rel_path and info.get('owner') == sender_id:
                token_to_remove = token
                break
        
        if token_to_remove:
            # حذف الويبهوك من تيليجرام
            await delete_webhook_for_token(token_to_remove)
            # حذف السجل من الملف
            del bots_data[token_to_remove]
            save_bots_data(bots_data)
            token_msg = f"\n\n🤖 **تم حذف سجل البوت.**\n🔑 التوكن المسترجع: `{token_to_remove}`"
    # ----------------------------------------

    if not os.path.exists(file_path):
        await event.answer("❌ الملف تم حذفه بالفعل أو لم يعد موجوداً!", alert=True)
    else:
        try:
            os.remove(file_path)
            await increment_stat(sender_id, 'file_deletes')
            await event.answer("🗑️ تم حذف الملف بنجاح.", alert=True)
            
            # إرسال رسالة تأكيد مع التوكن إذا وجد
            if token_msg:
                await event.respond(f"🗑️ **تم حذف الملف `{file_name}`**{token_msg}")
                
        except Exception as e:
            await event.answer(f"❌ فشل حذف الملف: {e}", alert=True)

    # Refresh the file list view
    message_text, buttons = await generate_hosting_view(sender_id)
    await safe_edit_message(event, message_text, buttons=buttons, parse_mode='html')


async def rename_file_handler(event: events.CallbackQuery.Event):
    """Starts the conversation to rename a file."""
    sender_id = event.sender_id
    raw_data = event.data.decode('utf-8').split(':', 1)[1]
    old_file_name = resolve_file_data(raw_data)
    
    conversation_manager.set_state(
        sender_id,
        "awaiting_new_name",
        context={'old_name': old_file_name},
        message_id=event.message_id
    )
    
    await safe_edit_message(
        event,
        f"**✏️ إعادة تسمية الملف:** `{old_file_name}`\n\nأرسل الآن الاسم الجديد للملف.",
        buttons=[[Button.inline("❌ إلغاء", data="cancel_action")]]
    )

async def file_rename_conversation_handler(event: events.NewMessage.Event):
    """Handles the user's input for the new file name."""
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != "awaiting_new_name":
        return

    new_name = event.text.strip()
    old_name = state['context']['old_name']
    message_id_to_edit = state['message_id']
    
    current_path = get_current_path(sender_id)
    old_path = os.path.join(current_path, old_name)

    # Validate new name
    is_valid, error_msg = validate_name(new_name, "الملف")
    if not is_valid:
        await event.reply(error_msg)
        return

    # Extension Handling
    _, old_ext = os.path.splitext(old_name)
    _, new_ext = os.path.splitext(new_name)

    # Auto-append extension if missing
    if not new_ext:
        new_name += old_ext
        new_ext = old_ext
    
    # Enforce extension rules
    allowed_target_exts = ['.bak', '.txt']
    if new_ext.lower() != old_ext.lower() and new_ext.lower() not in allowed_target_exts:
        await event.reply(f"❌ تغيير الصيغة غير مسموح.\nيجب أن تكون الصيغة `{old_ext}` أو يمكنك التحويل إلى: `.bak`, `.txt` فقط.")
        return

    new_path = os.path.join(current_path, new_name)

    if os.path.exists(new_path):
        await event.reply("❌ يوجد ملف بنفس الاسم الجديد بالفعل. اختر اسماً آخر.")
        return

    if not os.path.exists(old_path):
         await event.reply("❌ الملف الأصلي لم يعد موجوداً. تم إلغاء العملية.")
    else:
        try:
            os.rename(old_path, new_path)
            await event.reply(f"✅ تم تغيير اسم الملف من `{old_name}` إلى `{new_name}` بنجاح.", buttons=[[Button.inline("⬅️ إعدادات الملف", data=get_hashed_data("file", new_name))]])
        except Exception as e:
            await event.reply(f"❌ فشلت إعادة التسمية: {e}")

    conversation_manager.delete_state(sender_id)
    
    # Refresh the file view
    status_msg = await event.client.get_messages(sender_id, ids=message_id_to_edit)
    # Update the panel to show the new file's menu
    await file_menu_handler(status_msg, file_name=new_name)

# Initialize TeleBot for WebApp support
telebot_bot = TeleBot(settings.telegram.BOT_TOKEN)

# Initialize Encryption for WebApp links
try:
    with open('encryption.key', 'rb') as key_file:
        ENCRYPTION_KEY = key_file.read()
    cipher_suite = Fernet(ENCRYPTION_KEY)
except Exception:
    cipher_suite = None

async def file_menu_handler(event: events.CallbackQuery.Event, file_name: str = None):
    """Displays the action menu for a specific file."""
    sender_id = event.sender_id
    # log_step("file_menu_entry", f"Entered file_menu_handler for user {sender_id}", {"file_name_arg": file_name, "event_data": event.data.decode('utf-8') if hasattr(event, 'data') else 'None'})
    await log_action("MENU_OPEN", f"User {sender_id} opened menu for file arg: {file_name}")

    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        if hasattr(event, 'answer'):
            return await event.answer("🚫 أنت محظور.", alert=True)
        else:
            return await event.reply("🚫 أنت محظور.")
    
    if not file_name:
        if hasattr(event, 'data'):
            raw_data = event.data.decode('utf-8').split(':', 1)[1]
            file_name = resolve_file_data(raw_data)
        else:
            return # Should not happen if called correctly

    current_path = get_current_path(sender_id)
    file_path = os.path.join(current_path, file_name)
    await log_action("MENU_PATH", f"Resolved Path: {file_path} (CWD: {current_path})")

    if not os.path.exists(file_path):
        await log_action("MENU_ERR", "File does not exist.")
        if hasattr(event, 'answer'):
            await event.answer("❌ الملف لم يعد موجوداً!", alert=True)
        # Refresh the view
        message_text, buttons = await generate_hosting_view(sender_id)
        return await safe_edit_message(event, message_text, buttons=buttons, parse_mode='html')

    # --- Build the message text (preview) ---
    MAX_PREVIEW_LENGTH = 1000 # Reduced for better fit
    MAX_LINES = 15
    MIN_LINES = 5
    preview_text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = []
            total_length = 0
            for i, raw_line in enumerate(f):
                line_len = len(raw_line)
                if (total_length + line_len > MAX_PREVIEW_LENGTH) or (i >= MAX_LINES):
                    break
                lines.append(raw_line)
                total_length += line_len
        if lines:
            preview_text = ''.join(lines).strip()
            preview_text = f"\n\n**📄 معاينة الملف:**\n```\n{preview_text}\n...```"
        else:
            preview_text = "\n\n⚠️ **الملف طويل جدًا ولا يمكن معاينته.**"
    except Exception as e:
        print(f"Error creating file preview for {file_path}: {e}")
        preview_text = "\n\n⚠️ **فشل في معاينة الملف.**"

    message_text = f"**التحكم بالملف:** `{file_name}`\n\n{preview_text}\n\nاختر الإجراء المطلوب:"

    # --- Build the buttons using compatibility wrapper ---
    markup = types.InlineKeyboardMarkup(row_width=2)

    # Main logic for PHP files
    if file_name.endswith('.php'):
        # Detect if this file is a Telegram bot (direct or via include chain)
        from bot.utils.bot_detector import detect_telegram_bot
        detection = detect_telegram_bot(file_path)
        has_input = detection['is_bot']

        # Check running status
        bots_data = load_bots_data()
        bot_token = None

        # FIX: Use the full relative path to accurately find the bot's status.
        # The old method using `os.path.basename` was ambiguous and could not
        # distinguish between files with the same name in different directories.
        rel_path = os.path.relpath(file_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')
        await log_action("MENU_CHECK_STATUS", f"Checking status for RelPath: {rel_path}")

        # Logic to handle potential duplicate entries for the same file (e.g. changed tokens)
        candidates = []
        for token, info in bots_data.items():
            if info.get('path') == rel_path and info.get('owner') == sender_id:
                candidates.append(token)
        
        # Prioritize a running token if multiple exist for this file
        running_token = next((t for t in candidates if bots_data[t].get('status') == 'running'), None)
        
        if running_token:
            bot_token = running_token
        elif candidates:
            bot_token = candidates[-1] # Use the most recently added one if none running
        
        is_running = bool(bot_token) and bots_data.get(bot_token, {}).get('status') == 'running'
        # If file is registered in bots.json, always show run/stop button regardless of detection
        if bot_token and not has_input:
            has_input = True
        await log_action("MENU_STATUS_RESULT", f"Is Running: {is_running} | Token: {bot_token} | Detected: {detection.get('is_bot', False)}")

        run_stop_text = "إيقاف ⏸️" if is_running else "تشغيل ▶️"
        run_stop_action = "stop_php" if is_running else "run_php"
        
        if has_input:
            markup.add(types.InlineKeyboardButton(run_stop_text, callback_data=get_hashed_data(run_stop_action, file_name).decode()))

        editor_token_row = []
        user_data = load_all_users().get(str(sender_id), {})
        plan = user_data.get('plan', 'free')
        
        # التحقق من الوضع العام للبوت (مجاني للجميع أم لا)
        host_settings = load_host_settings()
        is_global_free = host_settings.get('bot_mode', 'paid') == 'free'

        if getattr(settings.web, 'WEBAPP_URL', None) and cipher_suite:

            if plan == 'pro' or is_global_free:
                log_step("editor_access", "User is PRO, generating editor link", {"user_id": sender_id})
                try:
                    relative_path = os.path.relpath(file_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')
                    encrypted_path = cipher_suite.encrypt(relative_path.encode('utf-8')).decode('utf-8')
                    editor_url = f"{settings.web.EDITOR_BASE_URL}/webapp/edit/{quote(encrypted_path)}"
                    editor_token_row.append(types.InlineKeyboardButton("تحرير 📝", web_app=types.WebAppInfo(url=editor_url)))
                except Exception as e:
                    log_step("editor_error", "Failed to build editor URL", {"error": str(e)})
                    print(f"[file_menu_handler] failed to build editor URL: {e}")
            else:
                log_step("editor_access", "User is FREE, locking editor", {"user_id": sender_id})
                editor_token_row.append(types.InlineKeyboardButton("تحرير 📝 (PRO)", callback_data="pro_feature_locked:editor"))
        
        editor_token_row.append(types.InlineKeyboardButton("تغيير التوكن 🔄", callback_data=get_hashed_data("change_token", file_name).decode()))
        
        if editor_token_row:
            markup.add(*editor_token_row)

        markup.add(types.InlineKeyboardButton("ℹ️ معلومات التوكن", callback_data=get_hashed_data("token_info", file_name).decode()))
        
        if plan == 'pro' or is_global_free:
            test_run_btn = types.InlineKeyboardButton("🔬 تشغيل تجريبي", callback_data=get_hashed_data("test_run", file_name).decode())
            webhook_log_btn = types.InlineKeyboardButton("📡 سجل الويبهوك (Webhook)", callback_data=get_hashed_data("webhook_log", file_name).decode())
        else:
            test_run_btn = types.InlineKeyboardButton("🔬 تشغيل تجريبي (PRO)", callback_data="pro_feature_locked:test_run")
            webhook_log_btn = types.InlineKeyboardButton("📡 سجل الويبهوك (PRO)", callback_data="pro_feature_locked:webhook_log")

        markup.add(
            types.InlineKeyboardButton("🔎 فحص الأخطاء", callback_data=get_hashed_data("lint_file", file_name).decode()),
            test_run_btn
        )
        markup.add(webhook_log_btn)
        
        # AI buttons from bot.handlers.ai.handlers
        markup.add(
            types.InlineKeyboardButton("🤖 تصحيح بالـ AI", callback_data=get_hashed_data("ai_debug", file_name).decode()),
            types.InlineKeyboardButton("✨ تعديل بالـ AI", callback_data=get_hashed_data("ai_modify", file_name).decode())
        )
        
        backup_path = file_path + ".bak"
        if os.path.exists(backup_path):
             markup.add(types.InlineKeyboardButton("🔄 استعادة النسخة (AI)", callback_data=get_hashed_data("ai_restore", file_name).decode()))
        
        markup.add(types.InlineKeyboardButton("إعادة تسمية ✏️", callback_data=get_hashed_data("rename_file", file_name).decode()))
        markup.add(
            types.InlineKeyboardButton("تنزيل 📥", callback_data=get_hashed_data("download", file_name).decode()),
            types.InlineKeyboardButton("حذف 🗑️", callback_data=get_hashed_data("delete_file", file_name).decode())
        )

    elif file_name.endswith(('.txt', '.json')):
        markup.add(types.InlineKeyboardButton("إعادة تسمية ✏️", callback_data=get_hashed_data("rename_file", file_name).decode()))
        markup.add(
            types.InlineKeyboardButton("تنزيل 📥", callback_data=get_hashed_data("download", file_name).decode()),
            types.InlineKeyboardButton("حذف 🗑️", callback_data=get_hashed_data("delete_file", file_name).decode())
        )

    markup.add(types.InlineKeyboardButton("⬅️ رجوع إلى الملفات", callback_data="my_hosting"))

    # --- Send/Edit using appropriate method ---
    try:
        await event.answer()
    except: pass

    # If markup has WebApp buttons, use telebot to send new message
    if markup.has_webapp:
        try:
            # Try to edit message with telebot for WebApp support
            telebot_markup = markup.to_telebot()
            telebot_bot.edit_message_text(
                text=message_text,
                chat_id=sender_id,
                message_id=event.message_id,
                reply_markup=telebot_markup,
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Error editing WebApp message: {e}")
            # Fallback to telethon
            telethon_buttons = markup.to_telethon()
            try:
                await event.edit(message_text, buttons=telethon_buttons, parse_mode='md')
            except:
                pass
    else:
        # No WebApp, use telethon normally
        telethon_buttons = markup.to_telethon()
        try:
            await event.edit(message_text, buttons=telethon_buttons, parse_mode='md')
        except Exception as e:
            # Fallback to sending a new message if edit fails
            try:
                await event.respond(message_text, buttons=telethon_buttons, parse_mode='md')
            except:
                pass


# Conversation for cancelling
async def cancel_action_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    conversation_manager.delete_state(sender_id)
    
    # This handler is now only for conversations like rename/create folder
    # The "Clean Folder" menu now uses a direct "my_hosting" button
    # so no alert is needed for that case.
    await event.answer("تم إلغاء العملية.", alert=True) 
    
    # Regenerate and display the current hosting view
    message_text, buttons = await generate_hosting_view(sender_id)
    await safe_edit_message(event, message_text, buttons=buttons, parse_mode='html')


# --- Clean Folder Logic ---
async def clean_folder_prompt_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    current_path = get_current_path(sender_id)
    
    # Scan for extensions
    try:
        all_items = os.listdir(current_path)
    except OSError:
        return await event.answer("❌ لا يمكن الوصول للمجلد.", alert=True)

    items = [f for f in all_items if os.path.isfile(os.path.join(current_path, f))]
    dirs = [d for d in all_items if os.path.isdir(os.path.join(current_path, d))]

    if not items:
        if not dirs:
            return await event.answer("📂 المجلد فارغ بالفعل.", alert=True)

    extensions = set()
    for item in items:
        _, ext = os.path.splitext(item)
        if ext:
            extensions.add(ext.lower())
        else:
            extensions.add("no_ext")
    
    sorted_exts = sorted(list(extensions))
    
    if dirs:
        sorted_exts.append("__folders__")
    
    conversation_manager.set_state(
        sender_id, 
        "cleaning_folder", 
        context={
            "path": current_path,
            "available_exts": sorted_exts,
            "selected_exts": []
        },
        message_id=event.message_id
    )
    
    await render_clean_folder_menu(event, sender_id)

async def render_clean_folder_menu(event, sender_id):
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != 'cleaning_folder':
        return await event.answer("❌ انتهت الجلسة.", alert=True)
    
    context = state['context']
    path = context['path']
    available = context['available_exts']
    selected = context['selected_exts']
    
    relative_path = os.path.relpath(path, USER_BOTS_ROOT_DIR)
    display_path = f"./{relative_path}"
    
    # --- Generate Preview Text ---
    preview_sections = []
    total_files_selected = 0
    total_folders_selected = 0

    if selected:
        try:
            all_items = sorted(os.listdir(path))
        except OSError:
            all_items = []

        files = [f for f in all_items if os.path.isfile(os.path.join(path, f))]
        dirs = [d for d in all_items if os.path.isdir(os.path.join(path, d))]

        # 1. Process Files
        grouped_files = {}
        for f in files:
            _, ext = os.path.splitext(f)
            key = ext.lower() if ext else "no_ext"
            if key in selected:
                if key not in grouped_files:
                    grouped_files[key] = []
                grouped_files[key].append(f)

        for ext_key, file_list in grouped_files.items():
            count = len(file_list)
            total_files_selected += count
            header_name = ext_key.lstrip('.') if ext_key != "no_ext" else "بدون صيغة"
            
            # Format list with dashes
            list_content = "\n".join([f"- {f}" for f in file_list])
            
            section = (
                f"<b>📂 ملفات {header_name} (<code>{count}</code>):</b>\n"
                f"<blockquote expandable>{html.escape(list_content)}</blockquote>"
            )
            preview_sections.append(section)

        # 2. Process Folders
        if "__folders__" in selected and dirs:
            folder_details = []
            for d in dirs:
                d_path = os.path.join(path, d)
                # Recursive count
                f_count = 0
                d_count = 0
                for root, subdirs, subfiles in os.walk(d_path):
                    f_count += len(subfiles)
                    d_count += len(subdirs)
                
                safe_d = html.escape(d)
                folder_details.append(f"📂 {safe_d} ⤷\n - 📄 <code>{f_count}</code> | 📁 <code>{d_count}</code>")
            
            count = len(dirs)
            total_folders_selected += count
            list_content = "\n".join(folder_details)
            
            section = (
                f"<b>📁 المجلدات (<code>{count}</code>):</b>\n"
                f"<blockquote expandable>{list_content}</blockquote>"
            )
            preview_sections.append(section)

    preview_text = "\n\n".join(preview_sections)
    if preview_text:
        preview_text += "\n\n"
        
    # Summary
    summary = []
    if total_files_selected > 0: summary.append(f"<code>{total_files_selected}</code> ملف")
    if total_folders_selected > 0: summary.append(f"<code>{total_folders_selected}</code> مجلد")
    summary_text = " و ".join(summary) if summary else "لا شيء"

    text = (
        f"<b>🧹 تنظيف المجلد</b>\n\n"
        f"<b>المسار:</b> <code>{html.escape(display_path)}</code>\n\n"
        f"<b>المحدد للحذف:</b> {summary_text}\n\n"
        f"{preview_text}"
        "اختر العناصر التي تريد حذفها.\n"
        "⚠️ <b>تنبيه:</b> الحذف نهائي (بما في ذلك محتويات المجلدات)."
    )
    
    buttons = []
    row = []
    for ext in available:
        # Button formatting: remove dot, add special brackets
        if ext == "__folders__":
            label_ext = "📁 المجلدات"
        else:
            clean_ext = ext.lstrip('.') if ext != "no_ext" else "بدون صيغة"
            label_ext = f"◜{clean_ext}◞"
        
        is_selected = ext in selected
        icon = "✅" if is_selected else "⬜️"
        
        row.append(Button.inline(f"{icon} {label_ext}", data=f"clean_toggle:{ext}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
        
    buttons.append([
        Button.inline("✅ تحديد الكل", data="clean_select_all"),
        Button.inline("⬜️ إلغاء التحديد", data="clean_deselect_all")
    ])
    
    confirm_text = f"🗑️ حذف ({len(selected)}) صيغ" if selected else "🗑️ حذف"
    buttons.append([
        Button.inline(confirm_text, data="clean_confirm"),
        Button.inline("⬅️ رجوع", data="my_hosting") # Changed from cancel_action
    ])
    
    # Parse HTML manually to support collapsible blockquotes via entities
    parsed_text, entities = telethon_html.parse(text)
    
    for entity in entities:
        if isinstance(entity, telethon_types.MessageEntityBlockquote):
            entity.collapsed = True

    await safe_edit_message(event, parsed_text, buttons=buttons, parse_mode=None, entities=entities)

async def clean_folder_toggle_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    ext = event.data.decode('utf-8').split(':', 1)[1]
    
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != 'cleaning_folder':
        return await event.answer("❌ انتهت الجلسة.", alert=True)
    
    selected = state['context']['selected_exts']
    if ext in selected:
        selected.remove(ext)
    else:
        selected.append(ext)
    
    state['context']['selected_exts'] = selected
    await render_clean_folder_menu(event, sender_id)

async def clean_folder_bulk_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    action = event.data.decode('utf-8')
    
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != 'cleaning_folder':
        return await event.answer("❌ انتهت الجلسة.", alert=True)
    
    if action == "clean_select_all":
        state['context']['selected_exts'] = list(state['context']['available_exts'])
    elif action == "clean_deselect_all":
        state['context']['selected_exts'] = []
        
    await render_clean_folder_menu(event, sender_id)

async def clean_folder_confirm_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != 'cleaning_folder':
        return await event.answer("❌ انتهت الجلسة.", alert=True)
    
    context = state['context']
    path = context['path']
    user_root = get_user_root(sender_id) # للحماية
    selected = context['selected_exts']
    
    if not selected:
        return await event.answer("⚠️ لم تختر أي صيغة للحذف.", alert=True)
    
    if not os.path.exists(path):
        return await event.answer("❌ المجلد لم يعد موجوداً.", alert=True)
        
    # --- Backup before deleting ---
    items_to_delete = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            _, ext = os.path.splitext(item)
            check_ext = ext.lower() if ext else "no_ext"
            
            # --- حماية host_bootstrap.php من التنظيف ---
            if item == 'host_bootstrap.php' and path == user_root:
                continue
            # -------------------------------------------

            if check_ext in selected:
                items_to_delete.append(item_path)
        elif os.path.isdir(item_path):
            if "__folders__" in selected:
                items_to_delete.append(item_path)

    if items_to_delete:
        await event.answer("⏳ جارِ إنشاء نسخة احتياطية قبل الحذف...", cache_time=5)
        temp_dir = tempfile.mkdtemp()
        backup_zip_path = None
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
            zip_filename = f"backup_before_clean_{timestamp}.zip"
            backup_zip_path = os.path.join(temp_dir, zip_filename)

            with zipfile.ZipFile(backup_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for item_path in items_to_delete:
                    arcname = os.path.relpath(item_path, path)
                    zipf.write(item_path, arcname)
            
            # Send the backup
            summary = " و ".join([f"<code>{ext.lstrip('.')}</code>" for ext in selected if ext != '__folders__'] + (["المجلدات"] if "__folders__" in selected else []))
            caption = (
                f"<b>📦 نسخة احتياطية قبل التنظيف</b>\n\n"
                f"هذا الملف يحتوي على نسخة من العناصر التي سيتم حذفها من مجلد <code>{html.escape(os.path.basename(path))}</code>.\n\n"
                f"<b>العناصر المحددة:</b> {summary}"
            )
            await client.send_file(sender_id, backup_zip_path, caption=caption, parse_mode='html', force_document=True, silent=True)

        except Exception as e:
            await event.answer(f"⚠️ فشل إنشاء النسخة الاحتياطية، لكن سيتم المتابعة في الحذف. الخطأ: {e}", alert=False)
        finally:
            if backup_zip_path and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    # --- End Backup ---

    deleted_files = 0
    deleted_folders = 0
    
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            
            if os.path.isfile(item_path):
                _, ext = os.path.splitext(item)
                check_ext = ext.lower() if ext else "no_ext"
                
                # --- حماية host_bootstrap.php من التنظيف (تأكيد) ---
                if item == 'host_bootstrap.php' and path == user_root:
                    continue
                # ---------------------------------------------------
                
                if check_ext in selected:
                    os.remove(item_path)
                    deleted_files += 1
            
            elif os.path.isdir(item_path):
                if "__folders__" in selected:
                    shutil.rmtree(item_path)
                    deleted_folders += 1
                    
        if deleted_files > 0: await increment_stat(sender_id, 'file_deletes', amount=deleted_files)
        if deleted_folders > 0: await increment_stat(sender_id, 'folders_deleted', amount=deleted_folders)
        
        msg = f"✅ تم الحذف بنجاح:\n- {deleted_files} ملفات\n- {deleted_folders} مجلدات"
        await event.answer(msg, alert=False)
    except Exception as e:
        await event.answer(f"❌ حدث خطأ أثناء الحذف: {e}", alert=False)
        
    conversation_manager.delete_state(sender_id)
    
    # Return to hosting view
    message_text, buttons = await generate_hosting_view(sender_id)
    await safe_edit_message(event, message_text, buttons=buttons, parse_mode='html')


# run_php_handler removed — using the one in bots.py


async def stop_php_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    raw_data = event.data.decode('utf-8').split(':', 1)[1]
    file_name = resolve_file_data(raw_data)
    
    await log_action("STOP_REQ", f"User {sender_id} requested to STOP file: {file_name}")
    
    current_path = get_current_path(sender_id)
    file_path = os.path.join(current_path, file_name)
    rel_path = os.path.relpath(file_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')

    bots_data = load_bots_data()
    target_token = None
    
    # Find token associated with this file and user
    for token, info in bots_data.items():
        if info.get('path') == rel_path and info.get('owner') == sender_id:
            target_token = token
            break
    
    if not target_token:
        await log_action("STOP_FAIL", "No active bot found for this file.")
        return await event.answer("❌ هذا الملف غير مرتبط ببوت نشط.", alert=True)

    await log_action("STOP_STEP", f"Found token: {target_token[:8]}...{target_token[-4:]}")

    # 1. Delete Webhook
    await log_action("STOP_STEP", "Sending deleteWebhook request...")
    try:
        resp = await delete_webhook_for_token(target_token)
        await log_action("STOP_TELEGRAM_RESP", f"Response: {resp}")
    except Exception as e:
        await log_action("STOP_ERR", f"Error deleting webhook: {e}")

    # 2. Update DB
    if target_token in bots_data:
        bots_data[target_token]['status'] = 'stopped'
        bots_data[target_token]['webhook_set'] = False
        save_bots_data(bots_data)
        await log_action("STOP_SUCCESS", "Bot status updated to stopped.")
    
    await event.answer("🛑 تم إيقاف البوت.", alert=True)
    
    # Refresh Menu
    await file_menu_handler(event, file_name=file_name)


def setup(client_instance: "TelegramClient"):
    """Registers all file and folder management handlers with the TelegramClient."""
    client_instance.on(events.CallbackQuery(pattern=b"my_hosting"))(my_hosting_handler)
    client_instance.on(events.CallbackQuery(pattern=b"nav:(.+)"))(navigate_handler)
    client_instance.on(events.CallbackQuery(pattern=b"create_folder"))(create_folder_prompt_handler)
    client_instance.on(events.CallbackQuery(pattern=b"delete_folder"))(delete_folder_prompt_handler)
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.get_status(e.sender_id) in ["awaiting_folder_name", "awaiting_folder_to_delete"]))(folder_conversation_handler)
    client_instance.on(events.CallbackQuery(pattern=b"set_upload_folder"))(set_upload_folder_handler)
    client_instance.on(events.CallbackQuery(pattern=b"delete_this_folder"))(delete_this_folder_handler)
    client_instance.on(events.CallbackQuery(pattern=b"confirm_delete_this_folder"))(confirm_delete_this_folder_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"del_sub:(.+)"))(select_subfolder_to_delete_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"conf_del_sub:(.+)"))(confirm_delete_subfolder_handler)
    client_instance.on(events.CallbackQuery(pattern=b"zip_current_folder"))(zip_current_folder_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"download:(.+)"))(download_file_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"delete_file:(.+)"))(delete_file_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"confirm_delete_hashed:(.+)"))(confirm_delete_by_hash_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"rename_file:(.+)"))(rename_file_handler)
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.get_status(e.sender_id) == "awaiting_new_name"))(file_rename_conversation_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"file:(.+)"))(file_menu_handler)
    client_instance.on(events.CallbackQuery(pattern=b"cancel_action"))(cancel_action_handler)
    
    # Clean Folder Handlers
    client_instance.on(events.CallbackQuery(pattern=b"clean_folder_prompt"))(clean_folder_prompt_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"clean_toggle:(.+)"))(clean_folder_toggle_handler)
    client_instance.on(events.CallbackQuery(pattern=b"clean_select_all"))(clean_folder_bulk_handler)
    client_instance.on(events.CallbackQuery(pattern=b"clean_deselect_all"))(clean_folder_bulk_handler)
    client_instance.on(events.CallbackQuery(pattern=b"clean_confirm"))(clean_folder_confirm_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"stop_php:(.+)"))(stop_php_handler)
    
    print("✅ File and Folder management handlers registered.")
