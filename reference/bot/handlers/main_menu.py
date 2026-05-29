# bot_v2/bot/handlers/main_menu.py
# This module handles the /start command and the main menu interface.

import os
import time
from datetime import datetime
from typing import TYPE_CHECKING

from telethon import events
from telethon.tl.custom import Button
from telethon.tl.types import KeyboardButtonCallback
from telethon.errors.rpcerrorlist import UserIsBlockedError, PeerIdInvalidError

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_admin_settings, load_all_users
from bot.services.telegram import send_message_to_admin
from bot.core.state import conversation_manager
from bot.core.data_manager import STATS_FILE # To be used by StatsService later

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status, get_user_data, save_user_data
from bot.core.database import increment_stat, get_or_create_dev_api_key
from bot.services.billing_service import check_subscription_expiry
from bot.services.file_service import get_user_root, get_current_path, set_current_path, user_current_working_directory, USER_BOTS_ROOT_DIR

# Local Imports from bot_v2 utilities
from bot.utils.decorators import force_subscribe_required, maintenance_check
from bot.utils.telegram import safe_edit_message
from bot.utils.time import _now_ts, _TZ
from bot.utils.points import load_points_data, get_pending_referral, clear_pending_referral # Import points util
from bot.handlers.points import process_coupon # Import coupon processor
from bot.handlers import forwarding # <-- تسجيل هاندلر التوجيه

# Import telebot and web_app utilities for Web App Buttons
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from bot.handlers.web_app import generate_auth_url

tb = telebot.TeleBot(settings.telegram.BOT_TOKEN)

# Local Imports from bot_v2 handlers (for now, will be refactored later)

# --- Handlers ---

@force_subscribe_required
@maintenance_check
async def start_command_handler(event: events.NewMessage.Event):
    """Handler for the /start command. Displays the main menu."""
    sender_id = event.sender_id
    
    # Check for deep link (marketplace product)
    message_text = event.message.text or ""
    if message_text.startswith('/start mp_'):
        product_id = message_text.replace('/start mp_', '').strip()
        if product_id:
            try:
                from bot.core import database
                from bot.services import marketplace_service
                from bot.handlers.marketplace.reviews import get_product_buttons
                from bot.services.profanity_filter import check_user_ban
                
                # Check marketplace ban
                is_banned, ban_reason = await check_user_ban(sender_id, 'any')
                if is_banned:
                    await event.reply(ban_reason)
                    return
                
                # Get product
                product = await database.get_marketplace_product(product_id)
                if not product:
                    await event.reply("❌ المنتج غير موجود.")
                    return
                
                # Increment views
                await database.increment_product_views(product_id, sender_id)
                
                # Format and send
                message = await marketplace_service.format_product_details(product, sender_id)
                buttons = await get_product_buttons(product['product_id'], sender_id)
                
                return await event.respond(message, buttons=buttons, parse_mode='md')
                
            except Exception as e:
                print(f"[Deep Link Error] {e}")
                import traceback
                traceback.print_exc()
                await event.reply("❌ حدث خطأ في عرض المنتج.")
                return
    
    # --- User Status Check ---
    # Will be imported from bot.handlers.admin.users or a dedicated service
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.reply("🚫 **أنت محظور من استخدام هذا البوت.**")

    # --- Plan Info Display ---
    user_data = get_user_data(sender_id)
    try:
        # check_subscription_expiry from bot.handlers.billing
        demoted, user_data = check_subscription_expiry(str(sender_id), user_data, current_time=_now_ts())
        if demoted:
            save_user_data(sender_id, user_data)
            await event.reply("⚠️ **انتهى اشتراكك المدفوع.**\n\nتم إعادتك إلى الخطة المجانية.")
    except Exception as e:
        print(f"[Expiry Check Error] Failed during start: {e}")
    plan = user_data.get('plan', 'free')

    plan_quote_text = ""
    if plan == 'pro':
        expiry_ts = user_data.get('plan_expiry')
        plan_source = user_data.get('plan_source', '')
        
        if plan_source == 'top_developer':
            expiry_str = "👑 مجاني طالما أنت في Top 3"
        elif expiry_ts:
            try:
                expiry_date = datetime.fromtimestamp(expiry_ts, _TZ).strftime('%Y-%m-%d')
                expiry_str = f"ينتهي في: {expiry_date}"
            except:
                expiry_str = "تاريخ غير صالح"
        else:
            expiry_str = "اشتراك دائم"
            
        plan_quote_text = f"<blockquote>🚀 <b>نوع الخطة:</b> مدفوعة (PRO)\n⏳ <b>الصلاحية:</b> {expiry_str}</blockquote>\n"
    else:
        plan_quote_text = f"<blockquote>⭐️ <b>نوع الخطة:</b> مجانية</blockquote>\n"

    # User's current working directory setup
    user_root = get_user_root(sender_id)
    # os.makedirs(user_root, exist_ok=True) # Handled by get_user_root
    try:
        os.chmod(user_root, 0o777) # Ensure permissions, might need adjustment for container
    except Exception as e:
        print(f"Could not set permissions for {user_root}: {e}")
    user_current_working_directory[sender_id] = user_root # Update global state
    display_path = f"./{os.path.relpath(user_root, USER_BOTS_ROOT_DIR)}"

    # --- Auto-Provision Helper Functions (host_bootstrap.php) ---
    bootstrap_path = os.path.join(user_root, 'host_bootstrap.php')
    bootstrap_restored = False # Flag to check if we restored it
    
    # إذا الملف مش موجود، نكريته تلقائي
    if not os.path.exists(bootstrap_path):
        try:
            source_path = os.path.join(settings.PROJECT_ROOT, 'bot_v2', 'config', 'host_bootstrap.php')
            if not os.path.exists(source_path):
                 source_path = os.path.join(settings.PROJECT_ROOT, 'config', 'host_bootstrap.php')
            
            if os.path.exists(source_path):
                api_key = await get_or_create_dev_api_key(sender_id)
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                content = content.replace('{USER_API_KEY_PLACEHOLDER}', api_key)
                content = content.replace('{INTERNAL_API_ENDPOINT}',
                    f"http://127.0.0.1:{settings.web.INTERNAL_API_PORT}/api/request_action")
                with open(bootstrap_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                bootstrap_restored = True # تم الاستعادة
        except Exception as e:
            print(f"Failed to auto-provision bootstrap for {sender_id}: {e}")

    bootstrap_exists = os.path.exists(bootstrap_path)
    
    warning_message = ""
    if not bootstrap_exists:
        warning_message = "‼️‼️ **تنبيه هام:** دوال المساعد غير مفعلة (فشل الإنشاء التلقائي). اضغط على الزر أدناه لتفعيلها.\n\n"
    elif bootstrap_restored:
        # تنبيه المستخدم بأنه تم استعادة الملف
        warning_message = "♻️ **ملاحظة:** تم اكتشاف حذف ملف النظام `host_bootstrap.php` وتمت استعادته تلقائياً لضمان عمل البوت.\n\n"
        
    bootstrap_button_text = "🔄 تحديث دوال المساعد" if bootstrap_exists else "✅ تفعيل دوال المساعد"

    start_message = (
        f"{warning_message}{plan_quote_text}"
        f"<b>أهلاً بك في لوحة تحكم الاستضافة الخاصة بك!</b>\n\n"
        f"🗂️ <b>الموقع الحالي:</b> <code>{display_path}</code>\n\n"
        "اختر أحد الخيارات من القائمة للبدء:"
    )
    notify_status = user_data.get('notify_failures', True)
    notify_icon = "🔔" if notify_status else "🔕"
    
    # Build Telebot InlineKeyboardMarkup
    markup = InlineKeyboardMarkup()
    
    if plan == 'free':
        markup.add(InlineKeyboardButton("🚀 الترقية إلى الخطة المدفوعة PRO 🚀", callback_data="show_upgrade_info"))
        
    markup.row(InlineKeyboardButton("استضافتي 📂", callback_data="my_hosting"))
    markup.row(
        InlineKeyboardButton("الملفات قيد التشغيل 🏃", callback_data="running_files"),
        InlineKeyboardButton("ايقاف الكل 🛑", callback_data="stop_all")
    )
    markup.row(
        InlineKeyboardButton("انشاء مجلد ➕", callback_data="create_folder"),
        InlineKeyboardButton("حذف مجلد 🗑️", callback_data="delete_folder")
    )
    markup.row(InlineKeyboardButton("🛒 الماركت", callback_data="marketplace_home"))
    markup.row(
        InlineKeyboardButton("💰 رصيد المكافآت", callback_data="my_points"),
        InlineKeyboardButton("📊 إحصائياتي", callback_data="my_stats")
    )
    markup.row(
        InlineKeyboardButton("🤖 دوال المطور", callback_data="dev_api_menu"),
        InlineKeyboardButton("تعليمات ℹ️", callback_data="help")
    )
    markup.row(
        InlineKeyboardButton("مفاتيح AI 🔑", callback_data="my_api_keys")
    )
    markup.row(
        InlineKeyboardButton(f"تنبيهات الأعطال {notify_icon}", callback_data="toggle_failure_notify"),
        InlineKeyboardButton(bootstrap_button_text, callback_data="provision_bootstrap")
    )

    # --- Web App Button Integration ---
    try:
        user_entity = await event.get_sender()
        webapp_url = generate_auth_url(user_entity.id, user_entity.first_name, getattr(user_entity, 'username', None))
        markup.row(
            InlineKeyboardButton(
                text="🌐 لوحة الويب", 
                web_app=WebAppInfo(url=webapp_url)
            )
        )
    except Exception as e:
        print(f"Failed to generate webapp url in /start handler: {e}")

    # Use telebot to send/edit the message to support Web App buttons properly
    if isinstance(event, events.CallbackQuery.Event):
        try:
            tb.edit_message_text(
                chat_id=event.chat_id,
                message_id=event.message_id,
                text=start_message,
                reply_markup=markup,
                parse_mode='html'
            )
        except telebot.apihelper.ApiTelegramException as e:
            if "message is not modified" not in str(e).lower():
                print(f"Telebot edit_message_text failed: {e}")
    else:
        tb.send_message(
            chat_id=event.chat_id,
            text=start_message,
            reply_markup=markup,
            parse_mode='html'
        )
        
        # إرسال لوحة الأدمن كرسالة منفصلة للمشرفين (فقط عند إرسال أمر start)
        user_status_admin = check_user_status(sender_id)
        if sender_id in settings.telegram.SUDO_USERS or user_status_admin == 'admin':
            from bot.handlers.admin.main import send_main_admin_panel
            await send_main_admin_panel(event, edit=False)

    # User registration logic
    user_data_exists = get_user_data(sender_id)
    if not user_data_exists:
        # --- Referral Logic ---
        referrer_id = None
        
        # 1. Check pending referrals (saved by force_subscribe_required)
        pending_ref = get_pending_referral(sender_id)
        if pending_ref:
            referrer_id = pending_ref
            clear_pending_referral(sender_id)
        
        # 2. If no pending, check current message args (direct join)
        if not referrer_id:
            # This logic is only for NewMessage events (/start ref_123)
            if isinstance(event, events.NewMessage.Event) and event.message and event.message.message:
                args = event.message.message.split()
                if len(args) > 1 and args[1].startswith('ref_'):
                    try:
                        referrer_id = int(args[1].split('_')[1])
                    except: pass
        
        # 3. Process Referral
        if referrer_id:
            try:
                # Ensure referrer exists and is not the user themselves
                if referrer_id != sender_id and get_user_data(referrer_id):
                    points_data = load_points_data()
                    reward = points_data.get('referral_reward', 1)
                    
                    # Credit the referrer
                    ref_user_data = get_user_data(referrer_id)
                    ref_user_data['points'] = ref_user_data.get('points', 0) + reward
                    save_user_data(referrer_id, ref_user_data)
                    
                    # Notify referrer
                    try:
                        await client.send_message(referrer_id, f"🎉 **مبروك!** انضم مستخدم جديد عبر رابطك.\n💎 تمت إضافة **{reward}** نقطة إلى رصيدك.")
                    except: pass
            except Exception as e:
                print(f"Referral error: {e}")
        # ----------------------

        user_entity = await event.get_sender()
        new_user_data = {
            "first_name": user_entity.first_name,
            "username": user_entity.username,
            "plan": "free", # New users start on free plan
            "notify_failures": True, # Default to notifying failures
            "points": 0 # Initialize points
        }
        save_user_data(sender_id, new_user_data)
        try:
            await increment_stat(sender_id, 'user_join')
        except Exception as e:
            print(f"[stats] failed to record user_join for {sender_id}: {e}")

        # Notify admins
        user_link = f"[{user_entity.first_name}](tg://user?id={sender_id})"
        all_users_for_count = load_all_users() # Load again to get updated count
        total_users = len(all_users_for_count)
        notification_text = (
            f"✨ **عضو جديد انضم للبوت!** ✨\n\n"
            f"👤 **الاسم:** {user_link}\n"
            f"🆔 **الأيدي:** `{sender_id}`\n"
            f"🗣️ **المعرف:** `@{user_entity.username or 'لا يوجد'}`\n\n"
            f"👥 **إجمالي الأعضاء الآن:** {total_users}"
        )
        for admin_id in settings.telegram.SUDO_USERS:
            if not await send_message_to_admin(admin_id, notification_text):
                print(f"Could not send new user notification to admin {admin_id}")

    # --- Coupon Redemption Logic (Start Link) ---
    # This logic is only for NewMessage events (/start coupon_CODE)
    if isinstance(event, events.NewMessage.Event) and event.message and event.message.message:
        args = event.message.message.split()
        if len(args) > 1 and args[1].startswith('coupon_'):
            try:
                code = args[1].split('_', 1)[1]
                msg = await process_coupon(sender_id, code)
                await event.reply(msg)
            except Exception as e:
                print(f"Coupon redemption error via start link: {e}")


async def main_menu_callback_handler(event: events.CallbackQuery.Event):
    """Handler for the main_menu callback, shows the main menu."""
    # --- Maintenance Mode Check ---
    admin_settings_check = load_admin_settings()
    if not admin_settings_check.get('bot_status', True):
        sender_id_check = event.sender_id
        if sender_id_check not in settings.telegram.SUDO_USERS and check_user_status(sender_id_check) != 'admin':
            await event.answer("🔧 البوت حالياً في وضع الصيانة.", alert=True)
            return
    await event.answer()
    
    sender_id = event.sender_id
    
    # --- User Status Check ---
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.edit("🚫 **أنت محظور من استخدام هذا البوت.**")

    # --- Plan Info Display ---
    user_data = get_user_data(sender_id)
    try:
        demoted, user_data = check_subscription_expiry(str(sender_id), user_data, current_time=_now_ts())
        if demoted:
            save_user_data(sender_id, user_data)
    except Exception as e:
        print(f"[Expiry Check Error] Failed during main_menu: {e}")
    
    plan = user_data.get('plan', 'free')

    plan_quote_text = ""
    if plan == 'pro':
        expiry_ts = user_data.get('plan_expiry')
        plan_source = user_data.get('plan_source', '')
        
        if plan_source == 'top_developer':
            expiry_str = "👑 مجاني طالما أنت في Top 3"
        elif expiry_ts:
            try:
                expiry_date = datetime.fromtimestamp(expiry_ts, _TZ).strftime('%Y-%m-%d')
                expiry_str = f"ينتهي في: {expiry_date}"
            except:
                expiry_str = "تاريخ غير صالح"
        else:
            expiry_str = "اشتراك دائم"
            
        plan_quote_text = f"<blockquote>🚀 <b>نوع الخطة:</b> مدفوعة (PRO)\n⏳ <b>الصلاحية:</b> {expiry_str}</blockquote>\n"
    else:
        plan_quote_text = f"<blockquote>⭐️ <b>نوع الخطة:</b> مجانية</blockquote>\n"

    user_root = get_user_root(sender_id)
    try:
        os.chmod(user_root, 0o777)
    except Exception as e:
        print(f"Could not set permissions for {user_root}: {e}")
    user_current_working_directory[sender_id] = user_root
    display_path = f"./{os.path.relpath(user_root, USER_BOTS_ROOT_DIR)}"

    # Check bootstrap
    bootstrap_path = os.path.join(user_root, 'host_bootstrap.php')
    bootstrap_exists = os.path.exists(bootstrap_path)
    bootstrap_button_text = "🔄 تحديث دوال المساعد" if bootstrap_exists else "✅ تفعيل دوال المساعد"

    start_message = (
        f"{plan_quote_text}"
        f"<b>أهلاً بك في لوحة تحكم الاستضافة الخاصة بك!</b>\n\n"
        f"🗂️ <b>الموقع الحالي:</b> <code>{display_path}</code>\n\n"
        "اختر أحد الخيارات من القائمة للبدء:"
    )
    
    notify_status = user_data.get('notify_failures', True)
    notify_icon = "🔔" if notify_status else "🔕"
    
    markup = InlineKeyboardMarkup()
    
    if plan == 'free':
        markup.add(InlineKeyboardButton("🚀 الترقية إلى الخطة المدفوعة PRO 🚀", callback_data="show_upgrade_info"))
        
    markup.row(InlineKeyboardButton("استضافتي 📂", callback_data="my_hosting"))
    markup.row(
        InlineKeyboardButton("الملفات قيد التشغيل 🏃", callback_data="running_files"),
        InlineKeyboardButton("ايقاف الكل 🛑", callback_data="stop_all")
    )
    markup.row(
        InlineKeyboardButton("انشاء مجلد ➕", callback_data="create_folder"),
        InlineKeyboardButton("حذف مجلد 🗑️", callback_data="delete_folder")
    )
    markup.row(InlineKeyboardButton("🛒 الماركت", callback_data="marketplace_home"))
    markup.row(
        InlineKeyboardButton("💰 رصيد المكافآت", callback_data="my_points"),
        InlineKeyboardButton("📊 إحصائياتي", callback_data="my_stats")
    )
    markup.row(
        InlineKeyboardButton("🤖 دوال المطور", callback_data="dev_api_menu"),
        InlineKeyboardButton("تعليمات ℹ️", callback_data="help")
    )
    markup.row(
        InlineKeyboardButton("مفاتيح AI 🔑", callback_data="my_api_keys")
    )
    markup.row(
        InlineKeyboardButton(f"تنبيهات الأعطال {notify_icon}", callback_data="toggle_failure_notify"),
        InlineKeyboardButton(bootstrap_button_text, callback_data="provision_bootstrap")
    )

    # --- Web App Button Integration ---
    try:
        user_entity = await event.get_sender()
        webapp_url = generate_auth_url(user_entity.id, user_entity.first_name, getattr(user_entity, 'username', None))
        markup.row(
            InlineKeyboardButton(
                text="🌐 لوحة الويب", 
                web_app=WebAppInfo(url=webapp_url)
            )
        )
    except Exception as e:
        print(f"Failed to generate webapp url in callback handler: {e}")

    # Edit the message using telebot
    try:
        tb.edit_message_text(
            chat_id=event.chat_id,
            message_id=event.message_id,
            text=start_message,
            reply_markup=markup,
            parse_mode='html'
        )
    except telebot.apihelper.ApiTelegramException as e:
        if "message is not modified" not in str(e).lower():
            print(f"Telebot edit_message_text failed in callback: {e}")


def setup(client_instance: "TelegramClient"):
    """Registers all main menu handlers with the TelegramClient."""
    # The force_subscribe_required decorator will be added back once bot.utils.decorators is implemented.
    client_instance.on(events.NewMessage(pattern='/start'))(start_command_handler)
    client_instance.on(events.CallbackQuery(pattern=b"main_menu"))(main_menu_callback_handler)
    forwarding.setup(client_instance) # <-- تفعيل هاندلر التوجيه
    
    # Register /web command handler (via setup to avoid duplicate registration)
    from bot.handlers import web_app as web_app_module
    web_app_module.setup(client_instance)
    
    print("✅ Main Menu handlers registered (bot/handlers/main_menu.py).")

print("✅ bot_v2/bot/handlers/main_menu.py initialized.")
