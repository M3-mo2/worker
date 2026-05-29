# bot_v2/bot/handlers/bots.py
# This module handles the lifecycle management of user-deployed PHP bots.

import os
import subprocess
import json
from datetime import datetime
import requests # Temporarily using requests for webhook calls, will be moved to services/telegram.py
from typing import List, Tuple, Dict, Any, Optional, TYPE_CHECKING

from telethon import events, errors
from telethon.tl.custom import Button

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_bots_data, save_bots_data
import re
import hashlib
import asyncio

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status, get_user_data
from bot.core.database import increment_stat
from bot.services.file_service import get_current_path, set_current_path, USER_BOTS_ROOT_DIR
from bot.services.quota_service import get_user_usage, get_quota_limits

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message
from bot.services.telegram import set_webhook_for_token, delete_webhook_for_token

# Local Imports from bot_v2 handlers (for now, will be refactored later)
from bot.handlers.files import file_menu_handler, resolve_file_data

# --- Developer Logger Import ---
from bot.utils.dev_logger import log_step

# --- Centralized Navigation System ---
from bot.core.navigation import create_nav_button_data, resolve_nav_data


# ===== وضع المطور (Developer Mode) =====
ACTION_LOG_FILE = os.path.join(settings.PROJECT_ROOT, 'data', 'bot_actions_log.txt')

async def log_action(action: str, details: str):
    """تسجيل الأحداث في وضع المطور"""
    if not getattr(settings, 'DEV_MODE', False):
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{action}] {details}\n"
    
    print(f"📝 {action}: {details}")
    try:
        with open(ACTION_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_message)
    except Exception as e:
        print(f"❌ Failed to write to log: {e}")

def get_hashed_bot_data(prefix: str, file_name: str) -> bytes:
    return create_nav_button_data(prefix, file_name)

def resolve_bot_data(data_str: str) -> str:
    return resolve_nav_data(data_str)

# --- Handlers ---
async def run_php_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    raw_data = event.pattern_match.group(1).decode()
    file_name = resolve_bot_data(raw_data)
    await log_action("RUN_REQ", f"User {sender_id} requested to RUN file: {file_name}")

    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    current_path = get_current_path(sender_id)
    file_path = os.path.join(current_path, file_name)
    
    await log_action("RUN_PATH", f"Resolved Path: {file_path} (Based on CWD: {current_path})")

    bots_data = load_bots_data()
    token_pattern = re.compile(r'(\d{6,14}:[\w\-]{35,75})')

    if not os.path.exists(file_path):
        await log_action("RUN_ERR", f"File NOT found at: {file_path}")
        return await event.answer("❌ الملف غير موجود!", alert=True)

    # Use the new comprehensive bot detector (traces include chains)
    from bot.utils.bot_detector import detect_telegram_bot
    detection = detect_telegram_bot(file_path)
    await log_action("RUN_DETECT", f"Detection result: is_bot={detection['is_bot']}, has_token={detection['has_token']}, has_input={detection['has_input']}, chain={len(detection['include_chain'])} files")

    if not detection['has_input']:
        await log_action("RUN_FAIL", "No php://input found in file or include chain")
        return await event.answer(
            "❌ لم يتم العثور على كود استقبال التحديثات (php://input) في هذا الملف أو الملفات المرتبطة به.",
            alert=True
        )

    # Read the file (or the file where the token was found) to extract the token
    token = None
    if detection['has_token'] and detection['token_source']:
        try:
            with open(detection['token_source'], 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            token_match = token_pattern.search(content)
            if token_match:
                token = token_match.group(1)
        except Exception:
            pass
    
    # Fallback: also try the entry file itself
    if not token:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            token_match = token_pattern.search(content)
            if token_match:
                token = token_match.group(1)
        except Exception as e:
            await log_action("RUN_ERR", f"Read Error: {e}")
            return await event.answer(f"❌ فشل قراءة الملف: {e}", alert=True)

    if not token:
        await log_action("RUN_FAIL", "No token found in file or include chain.")
        return await event.answer("❌ لم يتم العثور على توكن بوت في هذا الملف أو الملفات المرتبطة.", alert=True)
    
    await log_action("RUN_TOKEN", f"Found Token: {token[:8]}...{token[-4:]}")

    # --- Quota Check ---
    usage = get_user_usage(sender_id)
    limits = get_quota_limits(sender_id)
    if usage['total_bytes'] / (1024 * 1024) > limits['max_storage_mb']:
        await log_action("RUN_FAIL", "Quota exceeded.")
        return await event.answer(f"❌ لا يمكن تشغيل البوت: لقد تجاوزت مساحة التخزين المسموحة ({limits['max_storage_mb']} MB). يرجى حذف بعض الملفات.", alert=True)

    # Check if bot is already running
    if token in bots_data and bots_data[token].get('status') == 'running':
        await log_action("RUN_INFO", "Bot already running.")
        await event.answer("⚠️ هذا البوت يعمل بالفعل!", alert=True)
        # FIX: Refresh the UI to ensure the Stop button is shown
        return await file_menu_handler(event, file_name=file_name)

    # Determine bot tier (free/pro)
    user_data = get_user_data(sender_id)
    plan = user_data.get('plan', 'free')

    rel_path_for_json = os.path.relpath(file_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')
    
    # Store bot data
    secret = os.urandom(24).hex() # Generate a new secret token
    # Prepare data in memory first, don't save yet.
    bot_entry = {
        'path': rel_path_for_json,
        'status': 'running',
        'owner': sender_id,
        'webhook_set': False,
        'secret': secret,
        'tier': plan # Store the user's plan as the bot's tier
    }

    await log_action("RUN_WEBHOOK", "Sending setWebhook...")
    resp = await set_webhook_for_token(token, secret_token=secret)
    await log_action("RUN_WEBHOOK_RESP", f"Response: {resp}")

    if resp and ("\"ok\":true" in resp or "'ok': True" in resp):
        bot_entry['webhook_set'] = True
        bots_data[token] = bot_entry # Add/Update the entry in the main data dict
        save_bots_data(bots_data)
        await log_action("RUN_SUCCESS", "Webhook set and DB updated.")
        await event.answer("✅ تم تشغيل البوت وربط الويبهوك بنجاح!", alert=True)
        await increment_stat(sender_id, 'bots_started')
    else:
        # تحسين رسالة الخطأ بناءً على الرد
        error_msg = "⚠️ فشل ربط الويبهوك."
        if resp:
            if "401" in resp or "Unauthorized" in resp:
                error_msg = "❌ **خطأ:** التوكن غير صالح أو تم تعطيله من قبل تيليجرام (Unauthorized).\nيرجى التأكد من صحة التوكن."
            elif "Conflict" in resp:
                error_msg = "⚠️ **تنبيه:** يوجد تعارض في الويبهوك (Conflict). حاول مرة أخرى بعد قليل أو احذف الويبهوك يدوياً."
            else:
                # محاولة استخراج الوصف من الـ JSON
                try:
                    resp_json = json.loads(resp)
                    desc = resp_json.get("description", resp)
                    error_msg = f"⚠️ فشل ربط الويبهوك: {desc}"
                except:
                    error_msg = f"⚠️ فشل ربط الويبهوك: {resp}"
        
        # If webhook fails, we should not keep the bot as running.
        # Remove the entry if it was added for the first time.
        if token in bots_data and bots_data[token].get('secret') == secret:
            del bots_data[token]
            save_bots_data(bots_data)
        await log_action("RUN_FAIL", f"Webhook failed: {error_msg}")
        await event.answer(error_msg, alert=True)
        print(f"Webhook set failed for {token[:8]} (user {sender_id}): {resp}")

    # Refresh the file menu view
    await file_menu_handler(event, file_name=file_name)


async def stop_php_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    raw_data = event.pattern_match.group(1).decode()
    file_name = resolve_bot_data(raw_data)
    await log_action("STOP_REQ", f"User {sender_id} requested to STOP file: {file_name}")

    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)


    # Fix: Resolve full path to ensure we stop the correct bot
    current_path = get_current_path(sender_id)
    abs_file_path = os.path.join(current_path, file_name)
    rel_path = os.path.relpath(abs_file_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')
    await log_action("STOP_PATH", f"Resolved Path: {abs_file_path} (Rel: {rel_path})")
    
    bots_data = load_bots_data()
    target_token = None
    for token, info in bots_data.items():
        if info.get('owner') == sender_id and info.get('path') == rel_path:
            target_token = token
            break
    
    if not target_token:
        await log_action("STOP_FAIL", "No active bot found for this file path.")
        return await event.answer("❌ لم يتم العثور على توكن لبوت يعمل بهذا الملف.", alert=True)

    if bots_data.get(target_token, {}).get('status') == 'stopped':
        await log_action("STOP_INFO", "Bot already stopped.")
        return await event.answer("⚠️ هذا البوت متوقف بالفعل!", alert=True)
    
    # Delete webhook first
    await log_action("STOP_WEBHOOK", f"Deleting webhook for token {target_token[:8]}...")
    await delete_webhook_for_token(target_token)

    # Update bot status
    bots_data[target_token]['status'] = 'stopped'
    bots_data[target_token]['webhook_set'] = False # Mark webhook as deleted
    save_bots_data(bots_data)
    await log_action("STOP_SUCCESS", "Bot stopped and DB updated.")

    await event.answer("✅ تم إيقاف البوت بنجاح!", alert=True)
    await increment_stat(sender_id, 'bots_stopped')

    # Refresh the file menu view
    await file_menu_handler(event, file_name=file_name)


async def running_files_handler(event: events.CallbackQuery.Event):
    """Displays a list of running bots for the user."""
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    bots_data = load_bots_data()
    
    running_user_bots = []
    for token, info in bots_data.items():
        if info.get('owner') == sender_id and info.get('status') == 'running':
            running_user_bots.append(info)

    if not running_user_bots:
        message_text = "**ليس لديك أي ملفات قيد التشغيل حالياً.**"
        buttons = [[Button.inline("↩️ القائمة الرئيسية", data="main_menu")]]
        return await safe_edit_message(event, message_text, buttons=buttons)

    message_text = "**ملفاتك قيد التشغيل حالياً:**\n"
    buttons = []
    for info in running_user_bots:
        file_path = info['path']
        file_name = os.path.basename(file_path)
        # Create a button to stop the bot and another to go to its location
        buttons.append([
            Button.inline(f"🛑 إيقاف {file_name}", data=get_hashed_bot_data("stop_php", file_name)),
            Button.inline(f"📍 إلى الملف", data=get_hashed_bot_data("goto_file", file_name))
        ])
    
    buttons.append([Button.inline("↩️ القائمة الرئيسية", data="main_menu")])
    
    await safe_edit_message(event, message_text, buttons=buttons)


async def goto_file_handler(event: events.CallbackQuery.Event):
    """Navigates to the location of a specific file and shows its menu."""
    sender_id = event.sender_id
    log_step("goto_file_start", f"User {sender_id} navigating to file", {"data": event.data.decode()})
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
        
    raw_data = event.data.decode('utf-8').split(':', 1)[1]
    file_name = resolve_bot_data(raw_data)
    
    bots_data = load_bots_data()
    file_path = None
    for token, info in bots_data.items():
        if os.path.basename(info.get('path', '')) == file_name and info.get('owner') == sender_id:
            # Need to get the absolute path for set_current_path
            file_path = os.path.join(USER_BOTS_ROOT_DIR, info['path'])
            break

    if not file_path or not os.path.exists(file_path):
        log_step("goto_file_error", "File not found or path invalid", {"searched_name": file_name, "resolved_path": file_path})
        return await event.answer("❌ لم يتم العثور على الملف أو تم حذفه.", alert=True)

    # Set the user's CWD to the file's directory
    file_directory = os.path.dirname(file_path)
    set_current_path(sender_id, file_directory) # set_current_path needs absolute path

    # Call the file menu handler to display the options for that file
    log_step("goto_file_success", "Path set, opening menu", {"new_cwd": file_directory})
    # This might seem like a circular import, but it's a cross-handler call.
    # The loader handles this.
    await file_menu_handler(event)


async def stop_all_bots_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    bots_data = load_bots_data()
    stopped_count = 0
    
    for token, info in list(bots_data.items()): # Iterate over a copy
        if info.get('owner') == sender_id and info.get('status') == 'running':
            await delete_webhook_for_token(token)
            bots_data[token]['status'] = 'stopped'
            bots_data[token]['webhook_set'] = False
            stopped_count += 1
            await increment_stat(sender_id, 'bots_stopped')

    try:
        if stopped_count > 0:
            save_bots_data(bots_data)
            await event.answer(f"<b>✅ تم إيقاف {stopped_count} بوتات بنجاح!</b>", alert=True)
        else:
            await event.answer("<b>⚠️ لا توجد بوتات تعمل حالياً لإيقافها.</b>", alert=True)
    except errors.rpcerrorlist.QueryIdInvalidError:
        # This happens if the loop takes >30s; the action still completed.
        pass

    # Refresh the running files list
    await running_files_handler(event)


def setup(client_instance: "TelegramClient"):
    """Registers all bot lifecycle handlers with the TelegramClient."""
    client_instance.on(events.CallbackQuery(pattern=rb"run_php:(.+)"))(run_php_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"stop_php:(.+)"))(stop_php_handler)
    client_instance.on(events.CallbackQuery(pattern=b"running_files"))(running_files_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"goto_file:(.+)"))(goto_file_handler)
    client_instance.on(events.CallbackQuery(pattern=b"stop_all"))(stop_all_bots_handler)
    print("✅ Bot lifecycle handlers registered.")
