# bot_v2/bot/handlers/dev_tools.py
# This module contains developer-focused tools like linting, test runs, and webhook logs.

import os
import re
import time
import subprocess
import asyncio
import hashlib
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime

import aiosqlite # For webhook logs
from telethon import events, Button

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_all_users, load_bots_data, load_host_settings
from bot.core.state import conversation_manager
from bot.services.php_engine import execute_php_via_http
from bot.core.database import DB_NAME, get_or_create_dev_api_key
from bot.services.user_service import check_user_status, get_user_data
from bot.services.smart_path import resolve_file_path

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message
from bot.utils.text import sanitize_php_error, smart_split_simple, strip_html_tags
from bot.utils.time import _now_ts, _TZ

# Local Imports from bot_v2 handlers (for now, will be refactored later)
from bot.handlers.files import get_current_path, USER_BOTS_ROOT_DIR, get_user_root, file_menu_handler, resolve_file_data, get_hashed_data
from bot.handlers.main_menu import main_menu_callback_handler

# --- Centralized Navigation System ---
from bot.core.navigation import create_nav_button_data, resolve_nav_data

# --- Log Pagination Cache ---
LOG_PAGINATION_CACHE = {}

async def cleanup_log_cache(key: str, delay: int = 86400):
    """Removes a log pagination entry from the cache after a delay."""
    await asyncio.sleep(delay)
    if key in LOG_PAGINATION_CACHE:
        del LOG_PAGINATION_CACHE[key]

def get_back_nav_data(file_name: str) -> bytes:
    """Generates a hashed callback data for the back button."""
    key = resolve_nav_data(file_name) # Ensure it's hashed/stored if not already (though usually it is)
    # Actually, we want to CREATE a hash here.
    # Since create_nav_button_data returns bytes with prefix, we can use the helper directly or just get the hash.
    # But dev_tools uses "back_nav:HASH".
    return create_nav_button_data("back_nav", file_name)


# --- Handlers ---

async def lint_file_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    raw_data = event.pattern_match.group(1).decode()
    file_name = resolve_file_data(raw_data)
    file_path = resolve_file_path(sender_id, file_name)

    # Security check: ensure file is within user's root
    user_root = USER_BOTS_ROOT_DIR # User root is derived from the main UPLOAD_DIR
    try:
        if not os.path.commonpath([user_root, file_path]).startswith(user_root): # Check if prefix matches
            await event.answer("🚫 مسار غير مصرح به", alert=True)
            return
    except Exception as e:
        print(f"Path check error for lint_file: {e}")
        await event.answer("🚫 خطأ في التحقق من المسار", alert=True)
        return

    if not os.path.exists(file_path):
        await event.answer(f"❌ الملف غير موجود:\n`{file_path}`", alert=True)
        return

    report_lines = []

    # ===== 1) PHP Syntax Check (`php -l`) =====
    try:
        php_flags = ["-l"]
        return_code, stdout, stderr = await execute_php_via_http(
            file_path_host=file_path,
            php_flags=php_flags,
            timeout=10
        )
        # Simulate result object for consistency with original code logic
        result = type('obj', (object,), {'returncode': return_code, 'stdout': stdout, 'stderr': stderr})()
    except Exception as e:
        print(f"Subprocess error in lint_file_handler for user {sender_id}: {e}")
        report_lines.append("⚠️ تعذر تشغيل أداة فحص الكود (php -l).")
        text = "\n".join(report_lines)
        back_buttons = [[Button.inline("⬅️ رجوع", data=get_back_nav_data(file_name))]]
        await safe_edit_message(event, text, buttons=back_buttons)
        return

    if result.returncode != 0:
        # If syntax error, display it and stop
        stderr = (result.stderr or result.stdout or "").strip()
        clean_err = sanitize_php_error(stderr)
        report_lines.append(f"❌ خطأ PHP:\n```php\n{clean_err}\n```")
        text = "\n".join(report_lines)
        back_buttons = [[Button.inline("⬅️ رجوع", data=get_back_nav_data(file_name))]]
        await safe_edit_message(event, text, buttons=back_buttons)
        return

    report_lines.append("✔️ كود PHP سليم (no syntax errors).")

    # ===== 2) Read File Content =====
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        report_lines.append(f"⚠️ تعذر قراءة الملف: {e}")
        content = ""

    # ===== 3) Forbidden Functions List (from custom.ini logic) =====
    forbidden_funcs = {
        "stream_wrapper_restore","stream_wrapper_register","unserialize","ini_set","glob","proc_terminate",
        "fsockopen","stream_socket_client","ini_get","get_cfg_var","create_function","getenv","get_defined_vars",
        "get_defined_functions","get_loaded_extensions","get_current_user","ini_get_all","escapeshellarg","assert",
        "eval","exec","passthru","shell_exec","system","proc_open","popen","parse_ini_file","show_source",
        "pcntl_exec","pcntl_alarm","pcntl_fork","pcntl_waitpid","pcntl_wait","pcntl_wifexited","pcntl_wifstopped",
        "pcntl_wifsignaled","pcntl_wexitstatus","pcntl_wtermsig","pcntl_wstopsig","pcntl_signal",
        "pcntl_signal_dispatch","pcntl_get_last_error","pcntl_strerror","pcntl_sigprocmask","pcntl_sigwaitinfo",
        "putenv","apache_setenv","dl","posix_kill","posix_mkfifo","posix_setpgid","posix_setsid","posix_setuid",
        "ini_alter","ini_restore","openlog","syslog","highlight_file","phpinfo","readlink","symlink","link",
        "call_user_func","call_user_func_array"
    }
    forbidden_lower = {f.lower() for f in forbidden_funcs}

    # ===== 4) Safe Alternatives (from custom.ini logic) =====
    safe_alternatives = {
        "stream_wrapper_restore": ["fopen", "file_get_contents", "stream_context_create"],
        "stream_wrapper_register": ["fopen", "file_get_contents"],
        "unserialize": ["json_decode"],
        "glob": ["scandir", "DirectoryIterator"],
        "fsockopen": ["curl_init / curl_exec (use cURL)"],
        "stream_socket_client": ["curl_init / curl_exec (use cURL)"],
        "create_function": ["use anonymous functions (closures)"],
        "getenv": ["$_ENV", "$_SERVER"],
        "get_loaded_extensions": ["extension_loaded('extname')"],
        "assert": ["use explicit checks (if + throw)"],
        "eval": ["include", "require", "use defined callables/closures"],
        "exec": ["use background worker / job queue or native PHP libs"],
        "passthru": ["use background worker / job queue or native PHP libs"],
        "shell_exec": ["use background worker / job queue or native PHP libs"],
        "system": ["use background worker / job queue or native PHP libs"],
        "proc_open": ["use background worker / job queue (do not open raw processes from web)"],
        "popen": ["use background worker / job queue"],
        "parse_ini_file": ["use json_decode (JSON config) or YAML parser"],
        "openlog": ["use Monolog (PSR-3 logging)"],
        "syslog": ["use Monolog (PSR-3 logging)"],
        "readlink": ["realpath"],
        "symlink": ["create links during deployment or use copy() where acceptable"],
        "link": ["copy"],
        "call_user_func": ["callable invocation ($callable(...))"],
        "call_user_func_array": ["callable with spread: $callable(...$args)"],
        "pcntl_fork": ["use supervisor/worker/queue architecture"],
        "pcntl_exec": ["use supervisor/worker/queue architecture"],
        "pcntl_*": ["use supervisor/worker/queue architecture"],
    }

    # ===== 5) Exclude strings and comments from detection =====
    spans = []
    # string literals (single & double, with escapes)
    for m in re.finditer(r'(?s)("([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')', content):
        spans.append(m.span())
    # heredoc/nowdoc (approximate)
    for m in re.finditer(r'(?s)<<<[ \t]*([a-zA-Z_]\w*)\b.*?\n\1;', content):
        spans.append(m.span())
    # block comments
    for m in re.finditer(r'(?s)/\*.*?\*/', content):
        spans.append(m.span())
    # line comments
    for m in re.finditer(r'(?m)//.*?$|#.*?$', content):
        spans.append(m.span())

    spans.sort()
    merged = []
    for s0, s1 in spans:
        if not merged or s0 > merged[-1][1]:
            merged.append([s0, s1])
        else:
            merged[-1][1] = max(merged[-1][1], s1)
    spans = merged

    def inside_spans(pos: int) -> bool:
        import bisect
        i = bisect.bisect_right(spans, [pos, float('inf')]) - 1
        return i >= 0 and spans[i][0] <= pos < spans[i][1]

    # ===== 6) Detect actual function calls excluding strings/comments =====
    detected = set()

    func_regex = re.compile(r'(?<![\w\.\:/\$\->])([a-zA-Z_]\w*)\s*\(', re.IGNORECASE)
    for m in func_regex.finditer(content):
        start = m.start(1)
        if inside_spans(start):
            continue
        detected.add(m.group(1).lower())

    var_regex = re.compile(r'(?<![\w\.\:/\$\->])\$([a-zA-Z_]\w*)\s*\(', re.IGNORECASE)
    for m in var_regex.finditer(content):
        start = m.start(0)
        if inside_spans(start):
            continue
        detected.add(m.group(1).lower())

    cu_regex = re.compile(r'\bcall_user_func(?:_array)?\s*\(\s*(["\'])([a-zA-Z_]\w*)\1', re.IGNORECASE)
    for m in cu_regex.finditer(content):
        start = m.start(0)
        if inside_spans(start):
            continue
        detected.add(m.group(2).lower())
        detected.add('call_user_func') # Mark call_user_func itself as used

    # Exclude obvious keywords that are not functions
    ignore_names = {
        "if","else","elseif","for","foreach","while","switch","case","break","continue","return",
        "echo","print","function","class","namespace","use","new","try","catch","finally","throw",
        "list","array","var","public","protected","private","const","static","global","unset","exit"
    }
    detected = {d for d in detected if d not in ignore_names}

    # ===== 7) Filter forbidden functions =====
    found = sorted([f for f in detected if f in forbidden_lower])

    if not found:
        report_lines.append("\n\nℹ️ لا توجد دوال ممنوعة مستخدمة.")
    else:
        lines = []
        for f in found:
            line = f"- `{f}`"
            alts = []
            raw_alts = safe_alternatives.get(f, [])
            for alt in raw_alts:
                alt_key = alt.split()[0].strip().lower()
                if alt_key and alt_key not in forbidden_lower:
                    alts.append(alt)
            if alts:
                line += "  💡 بديل مقترح: " + "; ".join(alts)
            lines.append(line)
        report_lines.append("\n\n🚫 دوال ممنوعة مستخدمة:\n" + "\n".join(lines))

    # ===== 8) Send Result =====
    token_re = re.compile(r'\d{6,14}:[A-Za-z0-9_\-]{35,75}')
    def mask_tokens(s: str) -> str:
        return token_re.sub('<TOKEN_REDACTED>', s)

    text = "\n".join(report_lines)
    back_buttons = [[Button.inline("⬅️ رجوع", data=get_back_nav_data(file_name))]]

    await safe_edit_message(event, mask_tokens(text), buttons=back_buttons)



async def test_run_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    user_data = get_user_data(sender_id)
    plan = user_data.get('plan', 'free')

    # التحقق من الوضع العام
    host_settings = load_host_settings()
    is_global_free = host_settings.get('bot_mode', 'paid') == 'free'

    if plan != 'pro' and not is_global_free:
        return await event.answer("🚫 هذه الميزة (التشغيل التجريبي) متاحة للخطة المدفوعة (PRO) فقط.", alert=True)

    raw_data = event.pattern_match.group(1).decode()
    file_name = resolve_file_data(raw_data)
    file_path = resolve_file_path(sender_id, file_name)

    if not os.path.exists(file_path):
        return await event.answer(f"❌ الملف غير موجود:\n`{file_path}`", alert=True)

    await event.answer("🔬 جاري التشغيل التجريبي...", cache_time=60)
    status_msg = await event.edit(f"**🔬 جاري التشغيل التجريبي للملف:** `{file_name}`\n\n**النتيجة:**")

    try:
        return_code, stdout, stderr = await execute_php_via_http(
            file_path_host=file_path,
            php_flags=None,
            timeout=15
        )
        # Assign outputs to match original code structure
        result = type('obj', (object,), {'returncode': return_code, 'stdout': stdout, 'stderr': stderr})()
        
        output = result.stdout.strip()
        errors = result.stderr.strip()

        report = ""
        if output:
            report += "```\n" + output + "\n```\n"
        if errors:
            report += "\n**❌ الأخطاء:**\n```\n" + sanitize_php_error(errors) + "\n```\n"
        
        if not output and not errors:
            report = "✅ تم التنفيذ بنجاح، ولا يوجد مخرجات أو أخطاء."

        await safe_edit_message(
            status_msg,
            f"**🔬 نتيجة التشغيل التجريبي لـ** `{file_name}`:\n{report}",
            buttons=[[Button.inline("⬅️ رجوع", data=get_back_nav_data(file_name))]]
        )

    except subprocess.TimeoutExpired:
        await safe_edit_message(
            status_msg,
            f"❌ فشل التشغيل التجريبي لـ `{file_name}`: انتهت مدة التنفيذ (Timeout).",
            buttons=[[Button.inline("⬅️ رجوع", data=get_back_nav_data(file_name))]]
        )
    except Exception as e:
        await safe_edit_message(
            status_msg,
            f"❌ فشل التشغيل التجريبي لـ `{file_name}`: {e}",
            buttons=[[Button.inline("⬅️ رجوع", data=get_back_nav_data(file_name))]]
        )



async def webhook_log_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    user_data = get_user_data(sender_id)
    plan = user_data.get('plan', 'free')

    # التحقق من الوضع العام
    host_settings = load_host_settings()
    is_global_free = host_settings.get('bot_mode', 'paid') == 'free'

    if plan != 'pro' and not is_global_free:
        return await event.answer("🚫 هذه الميزة (عرض السجلات) متاحة للخطة المدفوعة (PRO) فقط.", alert=True)

    raw_data = event.pattern_match.group(1).decode()
    filter_type = event.pattern_match.group(2).decode() if event.pattern_match.lastindex >= 2 else 'all'
    
    file_name = resolve_file_data(raw_data)
    # Fix: Resolve full path to ensure we target the correct bot file (handle duplicates in diff folders)
    abs_file_path = resolve_file_path(sender_id, file_name)
    rel_path = os.path.relpath(abs_file_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')
    
    bots_data = load_bots_data()
    target_token = None
    for token, info in bots_data.items():
        if info.get('owner') == sender_id and info.get('path') == rel_path:
            target_token = token
            break
    
    if not target_token:
        return await event.answer("❌ هذا الملف غير مرتبط ببوت نشط.", alert=True)

    try:
        db_path = os.path.abspath(DB_NAME) 
        async with aiosqlite.connect(db_path, timeout=30) as db:
            async with db.execute(
                "SELECT ts, status, response FROM webhook_logs WHERE token = ? ORDER BY id DESC LIMIT 100",
                (target_token,)
            ) as cursor:
                all_logs = await cursor.fetchall()
    except Exception as e:
        return await event.answer(f"❌ فشل قراءة السجلات: {e}", alert=True)

    # تطبيق الفلتر
    if filter_type == 'errors':
        logs = [log for log in all_logs if log[1] >= 400 or log[1] == 0]
        filter_label = "الأخطاء فقط"
    elif filter_type == 'warnings':
        logs = [log for log in all_logs if 300 <= log[1] < 400]
        filter_label = "التحذيرات فقط"
    elif filter_type == 'success':
        logs = [log for log in all_logs if 200 <= log[1] < 300]
        filter_label = "النجاح فقط"
    else:
        logs = all_logs[:30]
        filter_label = "الكل"

    if not logs:
        return await event.answer(f"ℹ️ لا توجد سجلات ({filter_label}).", alert=True)

    report_header = f"**📡 سجل الويبهوك ({filter_label}) - {len(logs)} سجل**\n`{file_name}`\n\n"
    
    # ── Text grouping & paging ──
    # Group logs by max 10 entries per page to avoid cutting long updates across pages.
    ENTRIES_PER_PAGE = 10
    pages_list = []
    
    current_page_text = report_header
    entries_in_current_page = 0
    
    for ts, status, response in logs:
        time_str = datetime.fromtimestamp(ts, _TZ).strftime('%Y-%m-%d %H:%M:%S')
        status_icon = "✅"
        status_text = f"OK ({status})"
        if status >= 500:
            status_icon = "🔥"
            status_text = f"Fatal Error ({status})"
        elif status >= 400:
            status_icon = "❌"
            status_text = f"Client Error ({status})"
        elif status >= 300:
            status_icon = "⚠️"
            status_text = f"Warning ({status})"
        elif status == 0:
            status_icon = "⏳"
            status_text = "Timeout/Error"
             
        log_entry = f"{status_icon} `{time_str}` ➜ **{status_text}**\n"

        if status >= 300 and response:
             clean_resp = strip_html_tags(sanitize_php_error(response))
             if clean_resp:
                 log_entry += f"   ╚ **الاستجابة:**\n     ```\n{clean_resp.strip()}\n     ```\n"
        log_entry += "—" * 20 + "\n"
        
        # If adding this entry pushes us over Telegraph limits, or max entries per page met, switch to next page
        if len(current_page_text) + len(log_entry) > 4000 or entries_in_current_page >= ENTRIES_PER_PAGE:
             pages_list.append(current_page_text)
             current_page_text = report_header + log_entry
             entries_in_current_page = 1
        else:
             current_page_text += log_entry
             entries_in_current_page += 1
             
    # Append the last active page
    if current_page_text.strip() != report_header.strip():
        pages_list.append(current_page_text)
        
    if not pages_list:
        pages_list = [report_header]

    total_pages = len(pages_list)

    # --- Pagination Buttons & Logic ---
    filter_buttons = [
        Button.inline("📋 الكل" if filter_type == 'all' else "📋", data=f"webhook_log_filter:{raw_data}:all".encode()),
        Button.inline("❌ أخطاء" if filter_type == 'errors' else "❌", data=f"webhook_log_filter:{raw_data}:errors".encode()),
        Button.inline("⚠️ تحذيرات" if filter_type == 'warnings' else "⚠️", data=f"webhook_log_filter:{raw_data}:warnings".encode()),
        Button.inline("✅ نجاح" if filter_type == 'success' else "✅", data=f"webhook_log_filter:{raw_data}:success".encode())
    ]
    
    control_buttons = [
        Button.inline("🔄 تحديث", data=f"webhook_log_filter:{raw_data}:{filter_type}".encode()),
        Button.inline("🗑 حذف", data=get_hashed_data("webhook_log_clear", raw_data))
    ]
    
    if total_pages <= 1:
        await safe_edit_message(event, pages_list[0], buttons=[
            filter_buttons,
            control_buttons,
            [Button.inline("⬅️ رجوع للملف", data=get_back_nav_data(file_name))]
        ])
    else:
        log_key = hashlib.sha1(report_header.encode('utf-8')).hexdigest()[:12]
        
        LOG_PAGINATION_CACHE[log_key] = {
            "pages": pages_list,
            "owner": sender_id,
            "file_name": file_name,
            "file_data": raw_data,
            "filter_type": filter_type
        }
        asyncio.create_task(cleanup_log_cache(log_key))

        nav_buttons = []
        if total_pages > 1:
            nav_buttons.append(Button.inline(f"صفحة 1/{total_pages}", data="noop"))
            nav_buttons.append(Button.inline("التالي ➡️", data=f"log_page:{log_key}:2"))
        
        buttons = [
            filter_buttons,
            control_buttons,
            nav_buttons,
            [Button.inline("⬅️ رجوع للملف", data=get_back_nav_data(file_name))]
        ]
        
        await safe_edit_message(event, pages_list[0], buttons=buttons)


async def log_page_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    try:
        match = event.pattern_match
        key = match.group(1).decode()
        page = int(match.group(2).decode())
    except (ValueError, IndexError):
        return await event.answer("❌ بيانات الصفحة غير صالحة.", alert=True)

    if key not in LOG_PAGINATION_CACHE:
        return await event.answer("⌛️ انتهت صلاحية جلسة السجل هذه.", alert=True)
    
    log_data = LOG_PAGINATION_CACHE[key]
    
    if log_data["owner"] != sender_id:
        return await event.answer("🚫 هذا السجل لا يخصك.", alert=True)
        
    pages = log_data["pages"]
    total_pages = len(pages)
    file_name = log_data["file_name"]
    file_data = log_data.get("file_data", file_name)
    filter_type = log_data.get("filter_type", "all")
    
    if not 1 <= page <= total_pages:
        return await event.answer("❌ رقم الصفحة غير صالح.", alert=True)

    # أزرار الفلتر
    filter_buttons = [
        Button.inline("📋 الكل" if filter_type == 'all' else "📋", data=f"webhook_log_filter:{file_data}:all".encode()),
        Button.inline("❌ أخطاء" if filter_type == 'errors' else "❌", data=f"webhook_log_filter:{file_data}:errors".encode()),
        Button.inline("⚠️ تحذيرات" if filter_type == 'warnings' else "⚠️", data=f"webhook_log_filter:{file_data}:warnings".encode()),
        Button.inline("✅ نجاح" if filter_type == 'success' else "✅", data=f"webhook_log_filter:{file_data}:success".encode())
    ]
    
    # أزرار التحكم
    control_buttons = [
        Button.inline("🔄 تحديث", data=f"webhook_log_filter:{file_data}:{filter_type}".encode()),
        Button.inline("🗑 حذف", data=get_hashed_data("webhook_log_clear", file_data))
    ]

    # Build new buttons
    nav_buttons = []
    if page > 1:
        nav_buttons.append(Button.inline("⬅️ السابق", data=f"log_page:{key}:{page-1}"))
    
    nav_buttons.append(Button.inline(f"صفحة {page}/{total_pages}", data="noop"))

    if page < total_pages:
        nav_buttons.append(Button.inline("التالي ➡️", data=f"log_page:{key}:{page+1}"))
    
    buttons = [
        filter_buttons,
        control_buttons,
        nav_buttons,
        [Button.inline("⬅️ رجوع للملف", data=get_back_nav_data(file_name))]
    ]
    
    await safe_edit_message(event, pages[page-1], buttons=buttons)


async def webhook_log_clear_handler(event: events.CallbackQuery.Event):
    """حذف سجل الويب هوك للبوت"""
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    raw_data = event.pattern_match.group(1).decode()
    file_name = resolve_file_data(raw_data)
    
    # Fix: Resolve full path to ensure we target the correct bot file
    abs_file_path = resolve_file_path(sender_id, file_name)
    rel_path = os.path.relpath(abs_file_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')
    
    bots_data = load_bots_data()
    target_token = None
    for token, info in bots_data.items():
        if info.get('owner') == sender_id and info.get('path') == rel_path:
            target_token = token
            break
    
    if not target_token:
        return await event.answer("❌ هذا الملف غير مرتبط ببوت نشط (التوكن غير موجود).", alert=True)

    try:
        db_path = os.path.abspath(DB_NAME)
        async with aiosqlite.connect(db_path, timeout=30) as db:
            await db.execute("DELETE FROM webhook_logs WHERE token = ?", (target_token,))
            await db.commit()
        
        await event.answer("✅ تم حذف السجل بنجاح!", alert=True)
        
        # إعادة عرض الصفحة (فارغة)
        report = f"**📡 سجل الويبهوك (Webhook Logs)**\n`{file_name}`\n\nℹ️ لا توجد سجلات حديثة لهذا البوت."
        
        # أزرار الفلتر
        filter_buttons = [
            Button.inline("📋 الكل", data=f"webhook_log_filter:{raw_data}:all".encode()),
            Button.inline("❌ أخطاء", data=f"webhook_log_filter:{raw_data}:errors".encode()),
            Button.inline("⚠️ تحذيرات", data=f"webhook_log_filter:{raw_data}:warnings".encode()),
            Button.inline("✅ نجاح", data=f"webhook_log_filter:{raw_data}:success".encode())
        ]
        
        await safe_edit_message(event, report, buttons=[
            filter_buttons,
            [Button.inline("🔄 تحديث", data=f"webhook_log_filter:{raw_data}:all".encode())],
            [Button.inline("⬅️ رجوع للملف", data=get_back_nav_data(file_name))]
        ])
        
    except Exception as e:
        return await event.answer(f"❌ فشل حذف السجل: {e}", alert=True)


async def token_info_handler(event: events.CallbackQuery.Event):
    """Fetches and displays token info using the new bot detector (traces include chains)."""
    sender_id = event.sender_id
    raw_data = event.data.decode('utf-8').split(':', 1)[1]
    file_name = resolve_file_data(raw_data)
    file_path = resolve_file_path(sender_id, file_name)

    if not os.path.exists(file_path):
        return await event.answer("❌ الملف لم يعد موجوداً!", alert=True)

    await event.answer("ℹ️ جاري تحليل الملف...", cache_time=10)

    # Use the new bot detector to trace the entire include chain
    from bot.utils.bot_detector import detect_telegram_bot, generate_execution_flow_html, _build_dependency_map, _find_all_php_files

    detection = detect_telegram_bot(file_path)

    if not detection['has_token']:
        return await safe_edit_message(
            event,
            f"**ℹ️ تحليل التوكن للملف** `{file_name}`\n\n"
            f"❌ لم يتم العثور على أي توكن بوت في الملف أو الملفات المرتبطة به.\n\n"
            f"📦 **ملفات تم فحصها:** `{len(detection['include_chain'])}`",
            buttons=[[Button.inline("⬅️ رجوع", data=get_back_nav_data(file_name))]]
        )

    # Read the token from the source file
    token = None
    token_source = detection['token_source']
    token_pattern = re.compile(r'(\d{6,14}:[a-zA-Z0-9_\-]{35,75})')
    if token_source:
        try:
            with open(token_source, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            match = token_pattern.search(content)
            if match:
                token = match.group(1)
        except Exception:
            pass

    if not token:
        return await safe_edit_message(
            event,
            f"**ℹ️ تحليل التوكن للملف** `{file_name}`\n\n❌ فشل قراءة التوكن.",
            buttons=[[Button.inline("⬅️ رجوع", data=get_back_nav_data(file_name))]]
        )

    masked_token = f"{token[:8]}...{token[-4:]}"
    token_file_rel = os.path.basename(token_source) if token_source else 'غير معروف'
    input_file_rel = os.path.basename(detection['input_source']) if detection['input_source'] else 'غير معروف'

    # Call Telegram API to verify token
    api_url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        import httpx
        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(api_url, timeout=10)

        if response.status_code == 200:
            bot_info = response.json().get('result', {})
            bot_section = (
                f"\n**🤖 معلومات البوت:**\n"
                f"• **الاسم:** `{bot_info.get('first_name', '-')}`\n"
                f"• **المعرف:** `@{bot_info.get('username', '-')}`\n"
                f"• **الأيدي:** `{bot_info.get('id', '-')}`\n"
                f"• **مجموعات:** {'✅' if bot_info.get('can_join_groups') else '❌'}\n"
                f"• **يقرأ كل الرسائل:** {'✅' if bot_info.get('can_read_all_group_messages') else '❌'}\n"
                f"• **وضع مضمن (Inline):** {'✅' if bot_info.get('supports_inline_queries') else '❌'}"
            )
        else:
            bot_section = (
                f"\n**⚠️ التوكن غير صالح** (كود {response.status_code})"
            )
    except Exception as e:
        bot_section = f"\n⚠️ فشل الاتصال بتيليجرام: {e}"

    # Build execution flow
    project_dir = os.path.dirname(file_path)
    chain_count = len(detection['include_chain'])

    message = (
        f"**ℹ️ تحليل التوكن للملف** `{file_name}`\n\n"
        f"🔑 **التوكن:** `{masked_token}`\n"
        f"📄 **موجود في:** `{token_file_rel}`\n"
        f"📡 **استقبال التحديثات:** `{input_file_rel}`\n"
        f"📦 **سلسلة الملفات:** `{chain_count}` ملف"
        f"{bot_section}"
    )

    await safe_edit_message(
        event, message,
        buttons=[[Button.inline("⬅️ رجوع", data=get_back_nav_data(file_name))]]
    )


async def change_token_handler(event: events.CallbackQuery.Event):
    """Starts conversation to change a bot token — detects token via include chain."""
    sender_id = event.sender_id
    raw_data = event.data.decode('utf-8').split(':', 1)[1]
    file_name = resolve_file_data(raw_data)
    file_path = resolve_file_path(sender_id, file_name)

    # Use bot detector to find the actual token and which file it's in
    from bot.utils.bot_detector import detect_telegram_bot
    detection = detect_telegram_bot(file_path)

    token_source = detection.get('token_source')
    token_source_name = os.path.basename(token_source) if token_source else None

    if not detection['has_token'] or not token_source:
        return await safe_edit_message(
            event,
            f"**🔄 تغيير التوكن للملف** `{file_name}`\n\n"
            f"❌ لم يتم العثور على توكن في الملف أو الملفات المرتبطة به.\n"
            f"📦 ملفات تم فحصها: `{len(detection['include_chain'])}`",
            buttons=[[Button.inline("⬅️ رجوع", data=get_back_nav_data(file_name))]]
        )

    # Read current token for display
    token_pattern = re.compile(r'(\d{6,14}:[a-zA-Z0-9_\-]{35,75})')
    try:
        with open(token_source, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        old_match = token_pattern.search(content)
        old_token = old_match.group(1) if old_match else None
    except Exception:
        old_token = None

    masked_old = f"`{old_token[:8]}...{old_token[-4:]}`" if old_token else 'غير معروف'

    conversation_manager.set_state(
        sender_id,
        "awaiting_new_token",
        context={
            'file_name': file_name,
            'token_source': token_source,  # The actual file containing the token
        },
        message_id=event.message_id
    )

    await safe_edit_message(
        event,
        f"**🔄 تغيير التوكن للملف** `{file_name}`\n\n"
        f"🔑 التوكن الحالي: {masked_old}\n"
        f"📄 موجود في: `{token_source_name}`\n\n"
        f"أرسل الآن التوكن الجديد.",
        buttons=[[Button.inline("❌ إلغاء", data="cancel_action")]]
    )

async def token_change_conversation_handler(event: events.NewMessage.Event):
    """Handles user input for the new token — replaces in the chain's source file."""
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != "awaiting_new_token":
        return

    new_token = event.text.strip()
    file_name = state['context']['file_name']
    token_source = state['context'].get('token_source')  # New: actual file with the token
    message_id_to_edit = state['message_id']

    # If no token_source from new system, fallback to entry file
    if not token_source:
        token_source = resolve_file_path(sender_id, file_name)

    token_pattern = re.compile(r'\d{6,14}:[a-zA-Z0-9_\-]{35,75}')
    if not token_pattern.match(new_token):
        await event.reply("❌ التوكن الذي أرسلته غير صالح. يرجى التأكد وإرساله مجدداً.")
        return

    if not os.path.exists(token_source):
        await event.reply("❌ الملف الذي يحتوي على التوكن لم يعد موجوداً. تم إلغاء العملية.")
    else:
        try:
            with open(token_source, 'r', encoding='utf-8') as f:
                content = f.read()

            old_token_match = token_pattern.search(content)
            if not old_token_match:
                await event.reply("❌ لم أجد توكناً قديماً في الملف لاستبداله.")
            else:
                old_token = old_token_match.group(0)
                new_content = content.replace(old_token, new_token, 1)

                with open(token_source, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                source_name = os.path.basename(token_source)
                await event.reply(
                    f"✅ تم تغيير التوكن بنجاح!\n"
                    f"📄 الملف المعدّل: `{source_name}`"
                )

        except Exception as e:
            await event.reply(f"❌ فشلت عملية تغيير التوكن: {e}")

    conversation_manager.delete_state(sender_id)

    # Refresh the file menu
    from bot.handlers.files import file_menu_handler
    status_msg = await event.client.get_messages(sender_id, ids=message_id_to_edit)
    await file_menu_handler(status_msg)


async def provision_bootstrap_handler(event: events.CallbackQuery.Event):
    """Copies the host_bootstrap.php file to the user's root and injects their API key."""
    sender_id = event.sender_id
    # await event.answer("✅ جاري تفعيل دوال المساعد...") # Removed to avoid double toast

    try:
        from bot.core.database import get_or_create_dev_api_key
        from bot.services.file_service import get_user_root
        
        # Define paths
        source_path = os.path.abspath('bot_v2/config/host_bootstrap.php') # Adjusted path if needed, or keep relative
        if not os.path.exists(source_path):
             # Fallback to try finding it in current dir or standard config location
             source_path = os.path.abspath('config/host_bootstrap.php')

        user_root = get_user_root(sender_id)
        destination_path = os.path.join(user_root, 'host_bootstrap.php')

        # Get user's API key
        api_key = await get_or_create_dev_api_key(sender_id)

        # Read, replace, and write
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('{USER_API_KEY_PLACEHOLDER}', api_key)
        content = content.replace('{INTERNAL_API_ENDPOINT}',
            f"http://127.0.0.1:{settings.web.INTERNAL_API_PORT}/api/request_action")

        with open(destination_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Instead of calling main_menu_callback_handler which might send a new message,
        # we edit the current message to show success.
        await safe_edit_message(
            event,
            "✅ **تم تفعيل/تحديث دوال المساعد بنجاح!**\n\nيمكنك الآن استخدام الدوال الجاهزة في ملفات PHP الخاصة بك.",
            buttons=[[Button.inline("↩️ القائمة الرئيسية", data="main_menu")]]
        )

    except Exception as e:
        await event.answer(f"❌ فشل تفعيل دوال المساعد: {e}", alert=True)
        print(f"Error provisioning bootstrap for user {sender_id}: {e}")


async def dev_api_menu_handler(event: events.CallbackQuery.Event):
    # This handler can be expanded to show a menu for developer tools if needed.
    # For now, it can just provide info.
    message = (
        "**🛠️ دوال المطور (host_bootstrap)**\n\n"
        "**ما هذه الميزة؟**\n"
        "ملف فيه بعض الدوال (`host_bootstrap.php`) يتم زرعه تلقائياً في مساحتك. يمنحك قدرات اكثر تطورا للتحكم في السيرفر من داخل كود PHP الخاص بك.\n\n"
        "**كيف أستخدمها؟**\n"
        "لا تحتاج الى استدعاء ولا الى اي شيء فقط استخدم هذه الدوال مباشرة في ملفات PHP الخاصة بك بعد تفعيلها.\n\n"
        "`تم زرعها داخل php فلا تحتاج الى استدعاء او تضمين الملف.`\n\n"
        "**الدوال المتاحة (تحديث 1):**\n"
        "`setBotWebhook($token, $path)`\n"
        "• **الوظيفة:** تشغيل بوت وربطه بملف PHP برمجياً.\n"
        "• **الاستخدام (مصانع البوتات 🏭):** هذه هي **الطريقة الوحيدة** لربط ملفاتك بالبوتات (لأن السيرفر داخلي ولا يقبل ويبهوك خارجي).\n"
        "• **الميزة:** تتيح لك إنشاء بوتات تلقائياً من داخل الكود دون تدخل يدوي.\n\n"
        "**مثال عملي:**\n"
        "`setBotWebhook('123456:ABC...', 'bots/user_1.php');`\n"
        "(هذا السطر كفيل بتشغيل البوت فوراً!)"
    )
    await safe_edit_message(event, message, buttons=[[Button.inline("↩️ القائمة الرئيسية", data="main_menu")]])

async def back_nav_handler(event: events.CallbackQuery.Event):
    """Handles the hashed back button navigation."""
    key = event.pattern_match.group(1).decode()
    file_name = resolve_nav_data(key)
    if file_name and file_name != key:
        await file_menu_handler(event, file_name=file_name)
    else:
        await event.answer("❌ انتهت الجلسة أو الملف غير معروف.", alert=True)

def setup(client_instance: "TelegramClient"):
    """Registers all developer tools handlers with the TelegramClient."""
    client_instance.on(events.CallbackQuery(pattern=rb"lint_file:(.+)"))(lint_file_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"test_run:(.+)"))(test_run_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"webhook_log:(.+)"))(webhook_log_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"webhook_log_filter:(.+):(all|errors|warnings|success)"))(webhook_log_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"webhook_log_clear:(.+)"))(webhook_log_clear_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"log_page:(\w+):(\d+)"))(log_page_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"token_info:(.+)"))(token_info_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"change_token:(.+)"))(change_token_handler)
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.get_status(e.sender_id) == "awaiting_new_token"))(token_change_conversation_handler)
    client_instance.on(events.CallbackQuery(pattern=b"provision_bootstrap"))(provision_bootstrap_handler)
    client_instance.on(events.CallbackQuery(pattern=b"dev_api_menu"))(dev_api_menu_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"back_nav:(.+)"))(back_nav_handler)
    print("✅ Developer Tools handlers registered.")