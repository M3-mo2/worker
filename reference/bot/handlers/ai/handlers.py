# bot_v2/bot/handlers/ai/handlers.py
# Contains AI-related event handlers and helper functions for simple text-based file modification.

import asyncio
import logging
import os
import re
import time
import hashlib
import difflib
import sys
from typing import Optional, TYPE_CHECKING

from telethon import events, Button
from telethon.errors.rpcerrorlist import MessageNotModifiedError

if TYPE_CHECKING:
    from telethon import TelegramClient

from bot.core.config import settings
from bot.core.data_manager import load_admin_settings
from bot.core.state import conversation_manager

# Local Imports from bot_v2 services
from bot.services.php_engine import execute_php_via_http
from bot.services.user_service import check_user_status, get_user_data, save_user_data
from bot.services.file_service import get_user_root, get_current_path

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message
from bot.utils.time import _now_ts, _start_of_day, _TZ
from bot.utils.text import sanitize_php_error, format_diff_with_line_numbers, smart_split_simple, build_pagination_buttons

# Import the WebApp's Free AI Service
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from webapp.backend.services.ai_service import AIService

# --- Logger Setup ---
ai_logger = logging.getLogger(__name__)

AI_CORRECTION_CACHE = {}
TEST_RUN_PAGE_CACHE = {}

# --- Cache Cleanup Function ---
async def cleanup_ai_cache(key: str, cache_name: str, delay: int = 3600):
    """Removes an entry from a specified global cache after a delay."""
    await asyncio.sleep(delay)
    
    CACHE = None
    if cache_name == "AI_CORRECTION_CACHE":
        CACHE = AI_CORRECTION_CACHE
    elif cache_name == "TEST_RUN_PAGE_CACHE":
        CACHE = TEST_RUN_PAGE_CACHE
    else:
        ai_logger.warning(f"Unknown cache_name for cleanup: {cache_name}")
        return

    if key in CACHE:
        entry = CACHE.get(key, {})
        draft_path = entry.get("draft_path")
        if draft_path and os.path.exists(draft_path):
            try:
                os.remove(draft_path)
            except OSError as e:
                ai_logger.error(f"Error removing draft file '{draft_path}' during cache cleanup: {e}")
        
        CACHE.pop(key, None)
        ai_logger.info(f"Cleaned up expired cache key: {key} from {cache_name}")


def extract_php_code(text: str) -> str:
    """Extracts PHP code from a markdown-formatted AI response."""
    match = re.search(r"```php\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback to general code blocks
    match = re.search(r"```.*?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


async def process_ai_edit(event, status_msg, file_path_host, file_name, file_content, prompt, sender_id):
    """Core logic to send the full file and the prompt to the WebApp AI service and process the diff."""
    
    # 1. Compile the prompt
    full_prompt = (
        f"You are a Senior PHP Developer. Do NOT converse. Reply ONLY with the complete modified PHP code.\n\n"
        f"--- File: {file_name} ---\n"
        f"```php\n{file_content}\n```\n\n"
        f"--- TASK ---\n"
        f"{prompt}\n\n"
        f"Return the entire modified file inside a ```php ... ``` block."
    )

    try:
        # 2. Call WebApp's free AI Service
        ai_logger.info(f"Sending prompt to WebApp AIService for {file_name} by user {sender_id}")
        result = await AIService.chat(
            message=full_prompt,
            user_id=sender_id
        )

        if not result.get("success"):
            error_msg = result.get("error", "Unknown Error")
            return await safe_edit_message(status_msg, f"❌ فشل الاتصال بالذكاء الاصطناعي:\n`{error_msg}`")

        ai_response = result["response"]
        new_code = extract_php_code(ai_response)

        if not new_code or new_code == file_content:
            return await safe_edit_message(status_msg, "⚠️ لم يقم الذكاء الاصطناعي بإجراء أي تغييرات على الملف.")

        # 3. Save to Draft
        draft_path = file_path_host + ".draft"
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(new_code)

        # 4. Generate Diff
        original_lines = file_content.splitlines()
        new_lines = new_code.splitlines()
        diff_lines = list(difflib.unified_diff(original_lines, new_lines, lineterm=""))
        formatted_diff = format_diff_with_line_numbers(diff_lines)

        if not formatted_diff.strip():
             return await safe_edit_message(status_msg, "⚠️ لم يقم الذكاء الاصطناعي بإجراء أي تغييرات ملحوظة.")

        # 5. Cache for Pagination
        hash_key = hashlib.sha1(formatted_diff.encode('utf-8')).hexdigest()[:10]
        AI_CORRECTION_CACHE[hash_key] = {
            "original_code": file_content,
            "new_code": new_code,
            "diff_pages": smart_split_simple(formatted_diff),
            "file_path": file_path_host,
            "draft_path": draft_path,
            "owner_id": sender_id
        }

        # 6. Show First Page
        buttons = build_pagination_buttons(1, len(AI_CORRECTION_CACHE[hash_key]["diff_pages"]), hash_key, file_name, is_correction=True)
        await safe_edit_message(status_msg, f"**✅ تم التعديل بواسطة الذكاء الاصطناعي!**\n\n```diff\n{AI_CORRECTION_CACHE[hash_key]['diff_pages'][0]}\n```", buttons=buttons)

    except Exception as e:
        ai_logger.error(f"Error during AI processing: {e}", exc_info=True)
        await safe_edit_message(status_msg, f"❌ حدث خطأ غير متوقع:\n`{str(e)}`")


# --- Event Handlers for AI Features ---
async def ai_debug_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    ai_logger.info(f"[AI_DEBUG] Handler triggered for user {sender_id}")

    try:
        await event.answer("🚀 جاري بدء عملية التصحيح...", cache_time=5)
        
        raw_data = event.data.decode("utf-8")
        payload = raw_data.split(":", 1)[1]
        
        from bot.handlers.files import get_current_path, resolve_file_data
        file_name = resolve_file_data(payload)
        current_path = get_current_path(sender_id)
        file_path_host = os.path.abspath(os.path.join(current_path, file_name))
        
        if not os.path.exists(file_path_host):
            return await event.answer("❌ الملف غير موجود!", alert=True)

        status_msg = await event.edit(f"**🤖 AI Debugger**\n\n⚙️ جاري تشغيل الملف لاستخراج الأخطاء...")

        # 1. Run PHP (Test Run) to get errors
        try:
            return_code, stdout, stderr = await execute_php_via_http(
                file_path_host=file_path_host,
                php_flags=None,
                timeout=10
            )
            debug_context = f"EXIT_CODE: {return_code}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        except Exception as e:
            debug_context = f"EXECUTION_FAILED: {e}"

        await safe_edit_message(status_msg, f"**🤖 AI Debugger**\n\n⚙️ جاري تحليل الأخطاء وتصحيح الكود عبر الذكاء الاصطناعي...")

        # 2. Read File
        with open(file_path_host, "r", encoding="utf-8") as f:
            file_content = f.read()

        prompt = (
            f"The above PHP file has errors. When I executed it, I received the following logs:\n"
            f"```\n{debug_context}\n```\n\n"
            f"Please identify the root cause of the error and provide the fully corrected PHP file."
        )

        # 3. Process Edit
        await process_ai_edit(event, status_msg, file_path_host, file_name, file_content, prompt, sender_id)

    except Exception as e:
        ai_logger.error(f"[AI_DEBUG] CRITICAL ERROR: {e}", exc_info=True)
        try:
            await event.edit(f"❌ حدث خطأ غير متوقع:\n`{str(e)}`")
        except:
            pass


async def ai_modify_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    raw_data = event.data.decode("utf-8")
    payload = raw_data.split(":", 1)[1]
    
    from bot.handlers.files import get_current_path, resolve_file_data
    file_name = resolve_file_data(payload)
    current_path = get_current_path(sender_id)
    file_path_host = os.path.abspath(os.path.join(current_path, file_name))

    if not os.path.exists(file_path_host):
        return await event.answer("❌ الملف غير موجود!", alert=True)

    # Store state to wait for user prompt
    conversation_manager.set_state(
        sender_id,
        "awaiting_ai_modification_prompt",
        context={"file_path": file_path_host, "file_name": file_name},
        message_id=event.message_id
    )

    await safe_edit_message(
        event,
        f"**✨ تعديل بالذكاء الاصطناعي**\n\nالملف: `{file_name}`\n\nأرسل الآن وصفاً للتعديل الذي تريده (مثلاً: 'أضف دالة لحساب المجموع' أو 'غير رسالة الترحيب').",
        buttons=[[Button.inline("❌ إلغاء", data=f"ai_cancel_correct:{file_name}")]]
    )


async def ai_modification_prompt_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    
    if not state or state.get('status') != "awaiting_ai_modification_prompt":
        return

    user_prompt = event.text
    context = state['context']
    file_path_host = context['file_path']
    file_name = context['file_name']
    msg_id = state['message_id']
    
    conversation_manager.delete_state(sender_id)
    
    status_msg = await event.client.get_messages(sender_id, ids=msg_id)
    await safe_edit_message(status_msg, f"**🤖 AI Modify**\n\n⚙️ جاري تنفيذ التعديلات عبر الذكاء الاصطناعي...")

    try:
        with open(file_path_host, "r", encoding="utf-8") as f:
            file_content = f.read()

        prompt = f"Please modify the code strictly according to this user request:\n\n\"{user_prompt}\""
        await process_ai_edit(event, status_msg, file_path_host, file_name, file_content, prompt, sender_id)

    except Exception as e:
        ai_logger.error(f"Modify Error: {e}", exc_info=True)
        await safe_edit_message(status_msg, f"❌ حدث خطأ: {e}")


async def ai_diff_page_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    match = event.pattern_match
    hash_key = match.group(1).decode()
    page = int(match.group(2).decode())

    if hash_key not in AI_CORRECTION_CACHE:
        return await event.answer("انتهت صلاحية الجلسة.", alert=True)

    cache_entry = AI_CORRECTION_CACHE[hash_key]

    if cache_entry["owner_id"] != sender_id:
        return await event.answer("ليس لديك صلاحية الوصول لهذه الجلسة.", alert=True)

    diff_pages = cache_entry["diff_pages"]
    total_pages = len(diff_pages)
    file_name = os.path.basename(cache_entry["file_path"])

    if not 1 <= page <= total_pages:
        return await event.answer("رقم الصفحة غير صالح.", alert=True)
    
    buttons = build_pagination_buttons(page, total_pages, hash_key, file_name, is_correction=True)

    await safe_edit_message(
        event,
        f"**🤖 اقتراح التعديل (صفحة {page}/{total_pages})**\n\n```diff\n{diff_pages[page-1]}\n```",
        buttons=buttons,
        parse_mode='Markdown'
    )


async def ai_cancel_correct_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    file_name = event.pattern_match.group(1).decode()
    
    # Clean up cache entry if found
    keys_to_delete = [k for k, v in AI_CORRECTION_CACHE.items() if v.get("owner_id") == sender_id and os.path.basename(v.get("file_path")) == file_name]
    for key in keys_to_delete:
        cache_entry = AI_CORRECTION_CACHE.pop(key, None)
        if cache_entry and os.path.exists(cache_entry["draft_path"]):
            os.remove(cache_entry["draft_path"])
        ai_logger.info(f"AI correction for user {sender_id} cancelled and draft removed: {file_name}")

    await event.answer("تم إلغاء عملية AI.", alert=True)

    await safe_edit_message(
        event,
        f"**تم إلغاء عملية AI.**\n\nللملف: `{file_name}`",
        buttons=[[Button.inline("⬅️ رجوع إلى الملف", data=f"file:{file_name}")]]
    )


async def ai_confirm_correct_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    hash_key = event.pattern_match.group(1).decode()

    if hash_key not in AI_CORRECTION_CACHE:
        return await event.answer("انتهت صلاحية الجلسة أو تم تطبيق التغييرات بالفعل.", alert=True)

    cache_entry = AI_CORRECTION_CACHE.pop(hash_key)

    if cache_entry["owner_id"] != sender_id:
        return await event.answer("ليس لديك صلاحية لتطبيق هذه التغييرات.", alert=True)

    file_path = cache_entry["file_path"]
    draft_path = cache_entry["draft_path"]
    file_name = os.path.basename(file_path)

    if not os.path.exists(draft_path):
        return await event.answer("ملف المسودة غير موجود. ربما تم حذفه.", alert=True)

    try:
        import shutil 
        backup_path = file_path + ".bak"
        if os.path.exists(file_path):
            shutil.copyfile(file_path, backup_path)
            ai_logger.info(f"Backup created for {file_name} at {backup_path}")
        
        shutil.copyfile(draft_path, file_path)
        ai_logger.info(f"AI changes applied to {file_name} for user {sender_id}")

        await event.answer("✅ تم تطبيق التغييرات بنجاح!", alert=True)
        await safe_edit_message(
            event,
            f"**✅ تم تطبيق التغييرات المقترحة من الـ AI بنجاح!**\n\nللملف: `{file_name}`\n\n(تم حفظ نسخة احتياطية باسم `{file_name}.bak`)",
            buttons=[[Button.inline("⬅️ رجوع إلى الملف", data=f"file:{file_name}")]]
        )
    except Exception as e:
        ai_logger.error(f"Failed to apply AI changes for user {sender_id}, file {file_name}: {e}")
        await event.answer("❌ فشل تطبيق التغييرات.", alert=True)
        await safe_edit_message(
            event,
            f"**❌ فشل تطبيق التغييرات المقترحة من الـ AI!**\n\n`{e}`\n\nللملف: `{file_name}`",
            buttons=[[Button.inline("⬅️ رجوع إلى الملف", data=f"file:{file_name}")]]
        )
    finally:
        if os.path.exists(draft_path):
            os.remove(draft_path)


async def ai_restore_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    file_name = event.pattern_match.group(1).decode()

    from bot.handlers.files import get_current_path 
    current_path = get_current_path(sender_id)
    file_path_host = os.path.abspath(os.path.join(current_path, file_name))
    backup_path = file_path_host + ".bak"

    if not os.path.exists(backup_path):
        return await event.answer("❌ لا يوجد ملف احتياطي للاستعادة.", alert=True)

    try:
        import shutil 
        shutil.copyfile(backup_path, file_path_host)
        os.remove(backup_path) 
        ai_logger.info(f"User {sender_id} restored {file_name} from backup.")
        await event.answer("✅ تم استعادة الملف من النسخة الاحتياطية بنجاح!", alert=True)
        await safe_edit_message(
            event,
            f"**✅ تم استعادة الملف بنجاح من النسخة الاحتياطية!**\n\nللملف: `{file_name}`",
            buttons=[[Button.inline("⬅️ رجوع إلى الملف", data=f"file:{file_name}")]]
        )
    except Exception as e:
        ai_logger.error(f"Failed to restore {file_name} for user {sender_id}: {e}")
        await event.answer("❌ فشلت عملية الاستعادة.", alert=True)


def setup(client: "TelegramClient"):
    """Registers all AI handlers with the TelegramClient."""
    client.on(events.CallbackQuery(pattern=rb"ai_debug:(.+)"))(ai_debug_handler)
    client.on(events.CallbackQuery(pattern=rb"ai_modify:(.+)"))(ai_modify_handler)
    client.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.get_status(e.sender_id) == "awaiting_ai_modification_prompt"))(ai_modification_prompt_handler)
    client.on(events.CallbackQuery(pattern=rb"ai_diff_page:(\w+):(\d+)"))(ai_diff_page_handler)
    client.on(events.CallbackQuery(pattern=rb"ai_cancel_correct:(.+)"))(ai_cancel_correct_handler)
    client.on(events.CallbackQuery(pattern=rb"ai_confirm_correct:(\w+)"))(ai_confirm_correct_handler)
    client.on(events.CallbackQuery(pattern=rb"ai_restore:(.+)"))(ai_restore_handler)

print("✅ bot_v2/bot/handlers/ai/handlers.py initialized.")
