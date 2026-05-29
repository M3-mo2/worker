# bot_v2/bot/handlers/uploads.py
# This module handles all incoming document uploads, including ZIP file processing.

import os
import re
import html as html_lib
import zipfile
import shutil
import asyncio
import traceback
from typing import List, Dict, Any, Optional, TYPE_CHECKING

from telethon import events
from telethon.tl.custom import Button
from telethon.tl.types import DocumentAttributeFilename
from telethon.errors.rpcerrorlist import MessageNotModifiedError

if TYPE_CHECKING:
    from telethon import TelegramClient

from bot.services.telegram import send_message_to_admin

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_bots_data, save_bots_data, load_host_settings, load_all_users
from bot.core.state import conversation_manager

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status, get_user_data
from bot.core.database import increment_stat
from bot.services.file_service import get_user_root, get_current_path, set_current_path, USER_BOTS_ROOT_DIR
from bot.services.quota_service import get_user_usage, get_quota_limits, can_add_files
from bot.services.telegram import set_webhook_for_token

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message
from bot.utils.decorators import force_subscribe_required
from bot.utils.text import generate_recursive_tree_view

# Local Imports from bot_v2 handlers (for now, will be refactored later)
from bot.handlers.files import generate_hosting_view, file_menu_handler





# --- ZIP Extraction Constants ---
MAX_ZIP_FILES = 100
MAX_UNCOMPRESSED_SIZE = 25 * 1024 * 1024  # 25 MB
ALLOWED_EXTENSIONS_IN_ZIP = {'.php', '.json', '.txt', '.md'} # Note: main.py had only php, json, txt. Added .md from refactoring plan.
TOKEN_PATTERN = re.compile(r'(\d{6,14}:[\w\-]{35,75})')

# --- Error Handling Functions (from main.py) ---
async def handle_extraction_error(event: Any, status_message: Any, error: Exception):
    """Edits the user message to a generic error and forwards details to admins."""
    sender_id = event.sender_id
    try:
        await status_message.edit("❌ حدث خطأ ما أثناء معالجة الملف المضغوط.")
    except MessageNotModifiedError:
        pass # It's okay if the message is already showing the error
    except Exception as e:
        print(f"Failed to edit user message for error reporting: {e}")

    error_details = (
        f"⚠️ **Zip Extraction Error Report** ⚠️\n\n"
        f"👤 **User ID:** `{sender_id}`\n"
        f"💬 **Error:**\n`{str(error)}`\n\n"
        f"📜 **Traceback:**\n```\n{traceback.format_exc()}\n```"
    )
    for admin_id in settings.telegram.SUDO_USERS:
        if not await send_message_to_admin(admin_id, error_details):
            print(f"Failed to send error report to admin {admin_id}")

async def handle_general_error(event: Any, status_message: Optional[Any] = None, error: Optional[Exception] = None, custom_text: Optional[str] = None):
    """General error handler to notify user and admins."""
    sender_id = getattr(event, "sender_id", None)
    client_instance = getattr(event, "client", None)

    user_msg = custom_text or "❌ حدث خطأ غير متوقع أثناء تنفيذ العملية. يرجى المحاولة لاحقًا."
    try:
        if status_message:
            await status_message.edit(user_msg)
        elif hasattr(event, "answer"):
            await event.answer(user_msg, alert=True)
        elif client_instance and sender_id:
            await client_instance.send_message(sender_id, user_msg)
    except Exception as e:
        print(f"[ErrorHandler] Failed to notify user: {e}")

    error_report = (
        f"⚠️ **General Error Report** ⚠️\n\n"
        f"👤 **User ID:** `{sender_id}`\n"
        f"📄 **Context:** `{type(event).__name__}`\n\n"
        f"💬 **Error Message:**\n`{str(error)}`\n\n"
        f"📜 **Traceback:**\n```\n{traceback.format_exc()}\n```"
    )

    for admin_id in settings.telegram.SUDO_USERS:
        if not await send_message_to_admin(admin_id, error_report):
            print(f"[ErrorHandler] Failed to send report to admin {admin_id}")


# --- ZIP File Processing Logic ---
async def process_zip_file(event: events.NewMessage.Event, file_path: str):
    """The main function to handle the entire zip file processing logic."""
    sender_id = event.sender_id
    status_message = await event.reply("**⏳ جارِ التحقق من الملف المضغوط...**")

    try:
        if not os.path.exists(file_path):
            await status_message.edit("❌ **خطأ:** الملف غير موجود، ربما تم حذفه أثناء التحميل.")
            return

        # === Step 1: Security Scan ===
        try:
            zip_file = zipfile.ZipFile(file_path)
        except zipfile.BadZipFile:
            await status_message.edit("❌ **خطأ:** الملف المضغوط تالف أو ليس بصيغة zip صالحة.")
            return
        except NotImplementedError:
            await status_message.edit("❌ **خطأ:** الملف المضغوط يستخدم صيغة تشفير أو ضغط غير مدعومة.")
            return

        member_list = zip_file.infolist()
        limits = get_quota_limits(sender_id)

        if len(member_list) > limits['max_zip_files']:
            await status_message.edit(f"**❌ تم رفض الملف:** يحتوي على **{len(member_list)}** ملف، والحد الأقصى هو **{limits['max_zip_files']}** ملف.")
            return

        total_uncompressed_size = sum(member.file_size for member in member_list)
        can_add, reason = can_add_files(sender_id, new_files_count=len(member_list), new_bytes=total_uncompressed_size)
        if not can_add:
            await status_message.edit(f"**❌ تم رفض الملف:** {reason}")
            return

        # --- Detailed scan ---
        await status_message.edit("**🔬 جارِ فحص محتويات الملف...**")
        valid_members = []
        skipped_files_report = []

        for member in member_list:
            if member.is_dir():
                continue
            if member.filename.startswith('/') or '..' in member.filename.split('/') or os.path.isabs(member.filename):
                skipped_files_report.append(f"- <code>{html_lib.escape(member.filename)}</code> (مسار غير صالح)")
                continue
            file_ext = os.path.splitext(member.filename)[1].lower()
            if file_ext and file_ext not in ALLOWED_EXTENSIONS_IN_ZIP:
                skipped_files_report.append(f"- <code>{html_lib.escape(member.filename)}</code> (امتداد غير مسموح)")
                continue
            valid_members.append(member)

        # === Step 2: Extraction ===
        user_data = get_user_data(sender_id)
        user_root = get_user_root(sender_id)
        upload_path = user_data.get('upload_folder', user_root)
        if not os.path.exists(upload_path): upload_path = user_root

        zip_filename = os.path.basename(file_path)
        target_dir_name = os.path.splitext(zip_filename)[0]
        target_path = os.path.join(upload_path, target_dir_name)

        if os.path.exists(target_path):
            counter = 1
            while os.path.exists(f"{target_path}_{counter}"):
                counter += 1
            target_path = f"{target_path}_{counter}"
            target_dir_name = os.path.basename(target_path)

        os.makedirs(target_path, exist_ok=True)
        try: os.chmod(target_path, 0o777)
        except: pass
        await status_message.edit(f"**⏳ جارِ فك ضغط الملفات...**")

        for i, member in enumerate(valid_members):
            try:
                zip_file.extract(member, target_path)
            except RuntimeError as e:
                if "encrypted" in str(e):
                    await status_message.edit("❌ **خطأ:** الملف مقفول بكلمة سر. يرجى رفعه بدون كلمة سر.")
                    shutil.rmtree(target_path, ignore_errors=True)
                    return
                else:
                    raise
            if (i + 1) % 10 == 0 or (i + 1) == len(valid_members):
                try:
                    await status_message.edit(f"**⏳ جارِ فك الضغط... ({i + 1}/{len(valid_members)})**")
                    await asyncio.sleep(0.5)
                except MessageNotModifiedError:
                    pass

        # Set permissions to 777 for all extracted files and folders
        for root, dirs, files in os.walk(target_path):
            for d in dirs:
                try: os.chmod(os.path.join(root, d), 0o777)
                except: pass
            for f in files:
                try: os.chmod(os.path.join(root, f), 0o777)
                except: pass

        # === Step 3: Smart Project Analysis 🧠 ===
        await status_message.edit("**🧠 جارِ تحليل المشروع واكتشاف البوتات...**")

        from bot.utils.bot_detector import analyze_project
        analysis = analyze_project(target_path)

        bots_found = [b for b in analysis['bots'] if b.get('token')]
        total_bots = len(bots_found)

        # === Step 4: Build smart report ===
        tree_view = generate_recursive_tree_view(target_path)

        final_message = (
            f"<b>✅ تم فك ضغط وتحليل <code>{html_lib.escape(zip_filename)}</code> بنجاح!</b>\n\n"
            f"<b>📁 هيكل الملفات:</b>\n"
            f"<blockquote expandable><code>{html_lib.escape(target_dir_name)}/\n{html_lib.escape(tree_view)}</code></blockquote>\n"
        )

        if skipped_files_report:
            final_message += (
                "\n<b>⚠️ ملفات تم تجاهلها:</b>\n"
                "<blockquote expandable>"
                + "\n".join(skipped_files_report)
                + "</blockquote>\n"
            )

        buttons = []

        if total_bots == 0:
            # --- No bots found ---
            final_message += (
                "\n<b>📊 نتيجة التحليل:</b>\n"
                f"📄 إجمالي ملفات PHP: <code>{analysis['total_php_files']}</code>\n"
                "❌ لم يتم العثور على بوت تيليجرام.\n\n"
                "💡 <i>تأكد أن الملفات تحتوي على توكن بوت وكود استقبال التحديثات.</i>"
            )
            buttons.append([Button.inline("📁 تصفح الملفات", data="my_hosting")])
            conversation_manager.delete_state(sender_id)

        elif total_bots == 1:
            # --- Single bot ---
            bot = bots_found[0]
            entry = bot['suggested_entry']

            final_message += (
                "\n<b>📊 نتيجة التحليل:</b>\n"
                f"📄 ملفات PHP: <code>{analysis['total_php_files']}</code>\n"
                f"🤖 تم اكتشاف: <b>بوت واحد</b>\n\n"
                f"🔑 التوكن: <code>{bot['masked_token']}</code>\n"
                f"⚡ الملف الرئيسي: <code>{html_lib.escape(entry['rel_path'])}</code>\n"
                f"📦 الملفات المرتبطة: <code>{entry['chain_size']}</code> ملف\n"
            )

            # Execution flow HTML
            if bot.get('execution_flow_html'):
                final_message += f"\n{bot['execution_flow_html']}\n"

            # Store context
            entry_points_ctx = [
                {'rel_path': ep['rel_path'], 'path': ep['path'], 'chain_size': ep['chain_size']}
                for ep in bot['entry_points']
            ]
            conversation_manager.set_state(
                sender_id, 'awaiting_zip_entry_select',
                context={'target_path': target_path, 'token': bot['token'], 'entry_points': entry_points_ctx},
                message_id=status_message.id
            )

            if len(bot['entry_points']) > 1:
                final_message += "\n<b>💡 نقاط دخول بديلة:</b>\n"
                for i, ep in enumerate(bot['entry_points']):
                    star = "⭐" if i == 0 else "📄"
                    label = f"{star} {ep['rel_path']} ({ep['chain_size']} ملفات)"
                    buttons.append([Button.inline(label, data=f"zip_smart_entry:{i}")])
                buttons.append([Button.inline("❌ إلغاء", data="cancel_zip_setup")])
            else:
                buttons.append([Button.inline("▶️ تشغيل البوت", data="zip_smart_entry:0")])
                buttons.append([Button.inline("📁 تصفح فقط", data="cancel_zip_setup_keep")])

        else:
            # --- Multiple bots ---
            final_message += (
                "\n<b>📊 نتيجة التحليل:</b>\n"
                f"📄 ملفات PHP: <code>{analysis['total_php_files']}</code>\n"
                f"🤖 تم اكتشاف: <b>{total_bots} بوتات منفصلة</b>\n"
            )

            bots_context = []
            for i, bot in enumerate(bots_found):
                entry = bot['suggested_entry']
                n = i + 1
                final_message += (
                    f"\n<b>🤖 بوت #{n}:</b>\n"
                    f"  🔑 <code>{bot['masked_token']}</code>\n"
                    f"  ⚡ <code>{html_lib.escape(entry['rel_path'])}</code>\n"
                    f"  📦 <code>{entry['chain_size']}</code> ملف\n"
                )
                if bot.get('execution_flow_html'):
                    final_message += f"\n{bot['execution_flow_html']}\n"

                buttons.append([Button.inline(
                    f"▶️ تشغيل بوت #{n} ({entry['rel_path']})",
                    data=f"zip_smart_bot:{i}"
                )])
                bots_context.append({
                    'token': bot['token'],
                    'entry_rel_path': entry['rel_path'],
                    'entry_path': entry['path'],
                })

            conversation_manager.set_state(
                sender_id, 'awaiting_zip_multi_bot',
                context={'target_path': target_path, 'bots': bots_context},
                message_id=status_message.id
            )
            buttons.append([Button.inline("📁 تصفح فقط", data="cancel_zip_setup_keep")])
            buttons.append([Button.inline("❌ إلغاء وحذف", data="cancel_zip_setup")])

        # Send with HTML + collapsed blockquotes
        from telethon.extensions import html as telethon_html
        from telethon.tl import types as telethon_types

        parsed_text, entities = telethon_html.parse(final_message)
        for entity in entities:
            if isinstance(entity, telethon_types.MessageEntityBlockquote):
                entity.collapsed = True

        try:
            await status_message.edit(parsed_text, buttons=buttons, parse_mode=None, formatting_entities=entities)
        except Exception as e:
            print(f"[ZIP] Error sending analysis: {e}")
            try:
                await safe_edit_message(status_message, final_message, buttons=buttons, parse_mode='html')
            except Exception as e2:
                print(f"[ZIP] Fallback error: {e2}")

    except Exception as e:
        await handle_extraction_error(event, status_message, e)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# --- Handlers for ZIP processing conversation ---
async def cancel_zip_setup_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    status = conversation_manager.get_status(sender_id) or ''
    if status.startswith('awaiting_zip'):
        state = conversation_manager.get_state(sender_id)
        target_path = state.get('context', {}).get('target_path')
        if target_path and os.path.exists(target_path):
            shutil.rmtree(target_path, ignore_errors=True)
            print(f"Removed partially extracted ZIP folder: {target_path}")
        conversation_manager.delete_state(sender_id)
    await safe_edit_message(event, "**👍 تم الإلغاء وحذف الملفات.**", buttons=[[Button.inline("📁 عرض الملفات", data="my_hosting")]])


async def cancel_zip_setup_keep_handler(event: events.CallbackQuery.Event):
    """Cancel ZIP setup but KEEP the extracted files."""
    sender_id = event.sender_id
    conversation_manager.delete_state(sender_id)
    await safe_edit_message(event, "**👍 تم حفظ الملفات. يمكنك تصفحها الآن.**", buttons=[[Button.inline("📁 عرض الملفات", data="my_hosting")]])


async def zip_select_token_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != 'awaiting_zip_token':
        return await event.answer("انتهت هذه الجلسة، يرجى رفع الملف مرة أخرى.", alert=True)

    try:
        chosen_token = event.data.decode().split(':', 1)[1]
        context = state['context'] # Renamed from 'zip_context'
        
        context['chosen_token'] = chosen_token
        conversation_manager.set_state(sender_id, 'awaiting_zip_file', context=context, message_id=event.message_id)

        message = "🔒 **ممتاز!** الآن، **اختر ملف الويبهوك** (الملف الرئيسي الذي سيتم تشغيله):"
        buttons = []
        
        all_files = context['all_php_files']
        # Simple pagination: display up to 20 files per page
        page_size = 20
        start_index = 0 
        end_index = start_index + page_size
        
        for i, rel_php_path in enumerate(all_files[start_index:end_index]):
            actual_index = start_index + i 
            buttons.append([Button.inline(f"🐘 {rel_php_path}", data=f"zip_select_idx:{actual_index}")])
        
        # Add pagination buttons if needed (not implemented in main.py, but good for future)
        if len(all_files) > page_size:
            buttons.append([Button.inline("➡️ المزيد", data=f"zip_file_page:1:{page_size}")]) # Example for next page
        
        buttons.append([Button.inline("❌ إلغاء", data="cancel_zip_setup")])
        
        await safe_edit_message(event, message, buttons=buttons)
    except Exception as e:
        await handle_general_error(event, await event.get_message(), e, "❌ حدث خطأ أثناء اختيار التوكن.")


async def zip_select_file_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != 'awaiting_zip_file':
        return await event.answer("انتهت هذه الجلسة، يرجى رفع الملف مرة أخرى.", alert=True)

    status_message = await event.client.get_messages(sender_id, ids=event.message_id)
    try:
        chosen_index = int(event.pattern_match.group(1).decode('utf-8'))
        context = state['context']
        all_files = context['all_php_files']
        
        if not 0 <= chosen_index < len(all_files):
            return await event.answer("❌ فهرس الملف غير صالح.", alert=True)
            
        chosen_rel_path = all_files[chosen_index]
        token = context['chosen_token']
        target_path = context['target_path']
        
        webhook_file_abs_path = os.path.join(target_path, chosen_rel_path)

        # --- Finalization Step ---
        await safe_edit_message(status_message, "**⚙️ جارِ الإعداد النهائي...**")
        
        bots_data = load_bots_data()
        rel_path_for_json = os.path.relpath(webhook_file_abs_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')
        
        secret = os.urandom(24).hex() # Generate a new secret token
        bots_data[token] = {
            'path': rel_path_for_json,
            'status': 'running',
            'owner': sender_id,
            'webhook_set': False,
            'secret': secret,
            'tier': get_user_data(sender_id).get('plan', 'free')
        }
        
        resp = await set_webhook_for_token(token, secret_token=secret) # From bot.services.telegram
        
        if resp and ("\"ok\":true" in resp or "'ok': True" in resp):
            bots_data[token]['webhook_set'] = True
            await event.answer("✅ تم ضبط الويبهوك بنجاح!")
        else:
            await event.answer("⚠️ فشل ضبط الويبهوك، ولكن تم حفظ البوت.", alert=True)

        save_bots_data(bots_data)
        await increment_stat(sender_id, 'bots_started')

        set_current_path(sender_id, target_path) # From bot.handlers.files
        message = "**✅ اكتمل الإعداد!** تم ربط التوكن بالملف المحدد وتشغيل الويبهوك."
        buttons = [
            [Button.inline("▶️ عرض خيارات الملف", data=f"file:{chosen_rel_path}")],
            [Button.inline("📁 العودة إلى مدير الملفات", data="my_hosting")]
        ]
        await safe_edit_message(status_message, message, buttons=buttons)

    except Exception as e:
        await handle_general_error(event, status_message, e, "❌ حدث خطأ أثناء إعداد البوت.")
    finally:
        conversation_manager.delete_state(sender_id)


# --- Smart ZIP handlers (new) ---
async def _finalize_bot_setup(event, sender_id, token, entry_path, target_path):
    """Shared logic: set webhook and register bot."""
    status_message = await event.client.get_messages(sender_id, ids=event.message_id)
    await safe_edit_message(status_message, "**⚙️ جارِ الإعداد النهائي...**")

    bots_data = load_bots_data()
    rel_path_for_json = os.path.relpath(entry_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')

    secret = os.urandom(24).hex()
    bots_data[token] = {
        'path': rel_path_for_json,
        'status': 'running',
        'owner': sender_id,
        'webhook_set': False,
        'secret': secret,
        'tier': get_user_data(sender_id).get('plan', 'free')
    }

    resp = await set_webhook_for_token(token, secret_token=secret)

    if resp and ('"ok":true' in resp or "'ok': True" in resp):
        bots_data[token]['webhook_set'] = True
        await event.answer("✅ تم ضبط الويبهوك بنجاح!", alert=True)
    else:
        await event.answer("⚠️ فشل ضبط الويبهوك، ولكن تم حفظ البوت.", alert=True)

    save_bots_data(bots_data)
    await increment_stat(sender_id, 'bots_started')

    set_current_path(sender_id, os.path.dirname(entry_path))
    chosen_file_name = os.path.basename(entry_path)
    message = "✅ **اكتمل الإعداد!** تم ربط التوكن بالملف وتشغيل الويبهوك."
    from bot.handlers.files import get_hashed_data
    buttons = [
        [Button.inline("▶️ عرض خيارات الملف", data=get_hashed_data("file", chosen_file_name))],
        [Button.inline("📁 العودة إلى مدير الملفات", data="my_hosting")]
    ]
    await safe_edit_message(status_message, message, buttons=buttons)


async def zip_smart_entry_handler(event: events.CallbackQuery.Event):
    """Handle single-bot entry point selection."""
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != 'awaiting_zip_entry_select':
        return await event.answer("انتهت هذه الجلسة، يرجى رفع الملف مرة أخرى.", alert=True)

    try:
        chosen_index = int(event.data.decode().split(':', 1)[1])
        context = state['context']
        entry_points = context['entry_points']

        if not 0 <= chosen_index < len(entry_points):
            return await event.answer("❌ فهرس غير صالح.", alert=True)

        chosen = entry_points[chosen_index]
        token = context['token']
        target_path = context['target_path']
        entry_path = chosen['path']

        await _finalize_bot_setup(event, sender_id, token, entry_path, target_path)
    except Exception as e:
        await handle_general_error(event, await event.get_message(), e, "❌ حدث خطأ.")
    finally:
        conversation_manager.delete_state(sender_id)


async def zip_smart_bot_handler(event: events.CallbackQuery.Event):
    """Handle multi-bot selection."""
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state or state.get('status') != 'awaiting_zip_multi_bot':
        return await event.answer("انتهت هذه الجلسة، يرجى رفع الملف مرة أخرى.", alert=True)

    try:
        chosen_index = int(event.data.decode().split(':', 1)[1])
        context = state['context']
        bots = context['bots']

        if not 0 <= chosen_index < len(bots):
            return await event.answer("❌ فهرس غير صالح.", alert=True)

        chosen_bot = bots[chosen_index]
        token = chosen_bot['token']
        entry_path = chosen_bot['entry_path']
        target_path = context['target_path']

        await _finalize_bot_setup(event, sender_id, token, entry_path, target_path)
    except Exception as e:
        await handle_general_error(event, await event.get_message(), e, "❌ حدث خطأ.")
    finally:
        conversation_manager.delete_state(sender_id)


# --- Main Handler for Documents ---
@force_subscribe_required
async def handle_document(event: events.NewMessage.Event):
    """Handles all incoming documents, routing them to the correct processor."""
    sender_id = event.sender_id
    
    # Check if user is in marketplace upload mode
    from bot.handlers.marketplace.upload import STATE_UPLOAD_STEP
    upload_step = conversation_manager.get_value(sender_id, STATE_UPLOAD_STEP)
    if upload_step == 4:
        # User is uploading to marketplace, ignore here
        return
    
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.reply("🚫 **أنت محظور من استخدام هذا البوت.**")

    doc = event.document
    try:
        file_name = next(
            attr for attr in doc.attributes if isinstance(attr, DocumentAttributeFilename)
        ).file_name
    except StopIteration:
        file_name = "untitled_file" # Default name if not found

    file_ext = os.path.splitext(file_name)[1].lower()

    host_settings = load_host_settings()
    
    allowed_regular_exts = set()
    if host_settings.get('allow_php', True): allowed_regular_exts.add('.php')
    if host_settings.get('allow_json', True): allowed_regular_exts.add('.json')
    if host_settings.get('allow_txt', True): allowed_regular_exts.add('.txt')

    if file_ext == '.zip':
        status_msg = await event.reply(f"**📥 جاري تنزيل `{file_name}`...**")
        current_dir = get_current_path(sender_id)
        os.makedirs(current_dir, exist_ok=True)
        download_path = os.path.join(current_dir, file_name) # Use user's current path
        try:
            downloaded_path = await client.download_media(doc, download_path)
            if not downloaded_path or not os.path.exists(downloaded_path):
                raise FileNotFoundError("فشل تحميل الملف أو لم يتم العثور عليه.")
            await status_msg.delete()
            await process_zip_file(event, downloaded_path)
        except Exception as e:
            await status_msg.delete()
            await handle_general_error(event, await event.reply("حدث خطأ أثناء فك الضغط."), e)

    elif file_ext in allowed_regular_exts:
        user_data = get_user_data(sender_id)
        user_root = get_user_root(sender_id)
        upload_path = user_data.get('upload_folder', user_root)
        if not os.path.exists(upload_path): upload_path = user_root
        
        file_path = os.path.join(upload_path, file_name)

        if os.path.exists(file_path):
            # Ask user: overwrite or cancel
            message = f"⚠️ **يوجد ملف بنفس الاسم**\n\n"
            message += f"الملف: `{file_name}`\n"
            message += f"المجلد: `{os.path.relpath(upload_path, user_root)}`\n\n"
            message += f"ماذا تريد أن تفعل؟"
            
            buttons = [
                [Button.inline("🔄 تحديث الملف (استبدال)", f"overwrite_file:{file_name}".encode())],
                [Button.inline("❌ إلغاء الرفع", b"cancel_upload")]
            ]
            
            # Store file info for later
            conversation_manager.set_value(sender_id, 'pending_upload_file', {
                'file_path': file_path,
                'file_name': file_name,
                'message_id': event.message.id
            })
            
            return await event.reply(message, buttons=buttons, parse_mode='md')

        # Limit file uploads based on quota
        can_add, reason = can_add_files(sender_id, new_files_count=1, new_bytes=doc.size)
        if not can_add:
            return await event.reply(f"❌ **لا يمكن رفع الملف:** {reason}")


        await client.download_media(doc, file_path)
        try: os.chmod(file_path, 0o777)
        except: pass
        await increment_stat(sender_id, 'file_uploads')
        
        # === Enhanced Upload Success Message ===
        # Get bot info if this file is linked to a bot
        bots_data = load_bots_data()
        rel_path = os.path.relpath(file_path, USER_BOTS_ROOT_DIR).replace(os.path.sep, '/')
        
        bot_info = None
        for token, info in bots_data.items():
            if info.get('owner') == sender_id and info.get('path') == rel_path:
                bot_info = {
                    'token': token,
                    'id': token.split(':')[0] if ':' in token else 'Unknown',
                    'name': info.get('name', 'بوت بدون اسم')
                }
                break
        
        # Get relative path from user's root for display
        rel_display_path = os.path.relpath(file_path, user_root).replace(os.path.sep, '/')
        
        # Build the enhanced message
        message = f"✅ **تم رفع الملف بنجاح!**\n\n"
        message += f"📄 **اسم الملف:** `{file_name}`\n"
        message += f"📁 **المسار:** `{rel_display_path}`\n"
        message += f"💾 **الحجم:** `{os.path.getsize(file_path) / 1024:.2f} KB`\n"
        
        if bot_info:
            message += f"\n🤖 **البوت المرتبط:**\n"
            message += f"   • **الاسم:** {bot_info['name']}\n"
            message += f"   • **المعرف:** `#{bot_info['id']}`\n"
        
        # Build buttons based on whether file is linked to a bot
        buttons = []
        
        if bot_info:
            # File is linked to a bot - show relevant options
            buttons.append([
                Button.inline("⚙️ إعدادات الملف", data=f"file:{file_name}".encode()),
                Button.inline("📋 السجلات", data=f"webhook_log:{file_name}".encode())
            ])
        
        buttons.append([
            Button.inline("📂 قائمة الملفات", data="my_hosting"),
            Button.inline("🏠 القائمة الرئيسية", data="main_menu")
        ])
        
        await event.reply(message, buttons=buttons, parse_mode='md')
    else:
        allowed_str = ", ".join(ext.replace('.', '') for ext in allowed_regular_exts)
        await event.reply(
            f"❌ امتداد الملف `{file_ext}` غير مسموح به. "
            f"الامتدادات المسموحة هي: `zip`, {allowed_str}."
        )


async def overwrite_file_handler(event: events.CallbackQuery.Event):
    """Handle file overwrite confirmation."""
    sender_id = event.sender_id
    
    # Get pending upload info
    upload_info = conversation_manager.get_value(sender_id, 'pending_upload_file')
    if not upload_info:
        return await event.answer("❌ انتهت صلاحية العملية", alert=True)
    
    file_path = upload_info['file_path']
    file_name = upload_info['file_name']
    message_id = upload_info['message_id']
    
    try:
        # Get the original message with the file
        original_msg = await event.client.get_messages(sender_id, ids=message_id)
        if not original_msg or not original_msg.document:
            conversation_manager.clear_value(sender_id, 'pending_upload_file')
            return await event.answer("❌ لم يتم العثور على الملف", alert=True)
        
        # Delete old file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Download new file
        await event.answer("⏳ جاري تحديث الملف...", alert=True)
        await original_msg.download_media(file=file_path)
        try: os.chmod(file_path, 0o777)
        except: pass
        
        # Clear state
        conversation_manager.clear_value(sender_id, 'pending_upload_file')
        
        # Update stats
        await increment_stat(sender_id, 'file_uploads')
        
        await event.edit(
            f"✅ تم تحديث الملف `{file_name}` بنجاح!",
            buttons=[[Button.inline("⬅️ رجوع", data="my_hosting")]]
        )
    except Exception as e:
        print(f"Error overwriting file: {e}")
        await event.answer("❌ حدث خطأ أثناء تحديث الملف", alert=True)


async def cancel_upload_handler(event: events.CallbackQuery.Event):
    """Handle upload cancellation."""
    sender_id = event.sender_id
    
    # Clear state
    conversation_manager.clear_value(sender_id, 'pending_upload_file')
    
    await event.edit(
        "❌ تم إلغاء رفع الملف",
        buttons=[[Button.inline("⬅️ رجوع", data="my_hosting")]]
    )


def setup(client_instance: "TelegramClient"):
    """Registers all upload handlers with the TelegramClient."""
    
    def should_handle_document(e):
        """Check if document should be handled by regular upload handler."""
        if not (e.is_private and e.document):
            return False
        from bot.handlers.marketplace.upload import STATE_UPLOAD_STEP
        upload_step = conversation_manager.get_value(e.sender_id, STATE_UPLOAD_STEP)
        return upload_step != 4
    
    client_instance.on(events.NewMessage(func=should_handle_document))(handle_document)
    # ZIP handlers (legacy)
    client_instance.on(events.CallbackQuery(pattern=rb"zip_select_token:(.+)"))(zip_select_token_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"zip_select_idx:(\d+)"))(zip_select_file_handler)
    # ZIP handlers (smart - new)
    client_instance.on(events.CallbackQuery(pattern=rb"zip_smart_entry:(\d+)"))(zip_smart_entry_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"zip_smart_bot:(\d+)"))(zip_smart_bot_handler)
    client_instance.on(events.CallbackQuery(pattern=b"cancel_zip_setup_keep"))(cancel_zip_setup_keep_handler)
    client_instance.on(events.CallbackQuery(pattern=b"cancel_zip_setup"))(cancel_zip_setup_handler)
    # File handlers
    client_instance.on(events.CallbackQuery(pattern=rb"overwrite_file:.+"))(overwrite_file_handler)
    client_instance.on(events.CallbackQuery(pattern=b"cancel_upload"))(cancel_upload_handler)
    print("✅ Upload handlers registered.")