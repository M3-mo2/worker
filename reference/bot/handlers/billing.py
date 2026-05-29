# bot_v2/bot/handlers/billing.py
# This module handles paid plan features, code redemption, and points/referral system.

import time
from datetime import datetime, timedelta
from typing import Any, Optional, TYPE_CHECKING

from telethon import events
from telethon.tl.custom import Button

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.services.telegram import send_message_to_admin
from bot.core.config import settings
from bot.core.data_manager import load_all_users, save_all_users, load_giveaways, save_giveaways

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status, get_user_data, save_user_data
from bot.services.billing_service import check_subscription_expiry, update_user_bot_tiers

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message
from bot.utils.decorators import force_subscribe_required
from bot.utils.time import _now_ts, _TZ




# --- Billing System Configuration ---
POINTS_PER_REFERRAL = 100 # Points a user gets for a successful referral
SUBSCRIPTION_PACKAGES = {
    # 'key': (days, points_cost)
    '7_days': (7, 500),
    '30_days': (30, 1800),
}


# --- Handlers ---
@force_subscribe_required
async def redeem_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    user_id_str = str(sender_id)
    
    if check_user_status(sender_id) == 'banned': # Placeholder
        return await event.reply("🚫 **أنت محظور من استخدام هذا البوت.**")

    user_data = get_user_data(sender_id)
    
    # Check if user is already PRO
    if user_data.get('plan') == 'pro':
        if not user_data.get('plan_expiry'):
             return await event.reply("🎉 **أنت مشترك دائم بالفعل!** لست بحاجة لاستخدام أكواد.")
        if user_data.get('plan_expiry', 0) > time.time():
             return await event.reply("🎉 **لديك اشتراك مدفوع فعال بالفعل!**")

    try:
        code = event.pattern_match.group(1).strip()
        if not code:
            return await event.reply("❌ يرجى إرسال الكود مع الأمر. مثال: `/redeem 123abcde`")
    except Exception:
        return await event.reply("❌ صيغة الأمر خاطئة. مثال: `/redeem 123abcde`")

    giveaways = load_giveaways()
    if code not in giveaways:
        return await event.reply("❌ **الكود غير صالح أو غير موجود.**")

    code_data = giveaways[code]
    now = int(time.time())

    # Check code validity (24 hours)
    if now > code_data['created_at'] + 86400: # 24 * 60 * 60
        return await event.reply("⌛️ **عذراً، هذا الكود انتهت صلاحيته.**")

    # Check if already claimed by this user
    if user_id_str in code_data['claimed_by']:
        return await event.reply("🚫 **لقد قمت باستخدام هذا الكود من قبل.**")

    # Check claim limit
    if len(code_data['claimed_by']) >= code_data['limit']:
        winner_list_text = []
        claimed_user_ids = code_data['claimed_by']
        
        for i, claimed_user_id in enumerate(claimed_user_ids, 1):
            user_info = get_user_data(int(claimed_user_id))
            first_name = user_info.get('first_name', f'User {claimed_user_id}')
            winner_list_text.append(f"{i}. [{first_name}](tg://user?id={claimed_user_id})")
            
        winners_message = "\n".join(winner_list_text)
        
        reply_message = (
            "💔 **عذراً، لقد نفد العدد المسموح به لهذا الكود.**\n\n"
            "🎉 إليك قائمة الفائزين المحظوظين الذين سبقوك:\n"
            f"{winners_message}"
        )
        return await event.reply(reply_message, parse_mode='md')

    # --- Claim Code and Upgrade User ---
    
    # 1. Register user in code data
    code_data['claimed_by'].append(user_id_str)
    save_giveaways(giveaways)

    # 2. Calculate and grant subscription
    days_to_add = code_data['days']
    expiry_timestamp = now + (days_to_add * 86400)
    
    new_user_data = get_user_data(sender_id)
    if not new_user_data: # If user not found, create a new entry
        user_entity = await event.get_sender()
        new_user_data = {
            "first_name": user_entity.first_name,
            "username": user_entity.username,
            "plan": "free", # Default
            "notify_failures": True # Default
        }
    new_user_data['plan'] = 'pro'
    new_user_data['plan_expiry'] = expiry_timestamp
    new_user_data.pop('expiry_warning_sent', None)
    save_user_data(sender_id, new_user_data)
    
    # 3. Update user's bots tiers
    update_user_bot_tiers(user_id_str, 'pro') # Placeholder

    # 4. Send confirmation message
    expiry_date_str = datetime.fromtimestamp(expiry_timestamp, _TZ).strftime('%Y-%m-%d')
    await event.reply(
        f"**🎉 مبروك!**\n\n"
        f"✅ تم تفعيل اشتراك PRO لك بنجاح لمدة **{days_to_add} يوم**.\n"
        f"⏳ ينتهي اشتراكك في: `{expiry_date_str}`"
    )
    
    # 5. Notify admins
    try:
        user_entity = await event.get_sender()
        admin_msg = (
            f"🎁 **تم تفعيل كود مسابقة!**\n\n"
            f"👤 **المستخدم:** [{user_entity.first_name}](tg://user?id={sender_id})\n"
            f"🔑 **الكود:** `{code}`\n"
            f"🗓️ **المدة:** {days_to_add} يوم"
        )
        for admin_id in settings.telegram.SUDO_USERS:
            if not await send_message_to_admin(admin_id, admin_msg):
                print(f"[Giveaway] Failed to notify admin {admin_id}")
    except Exception as e:
        print(f"[Giveaway] Failed to notify admins: {e}")


async def show_upgrade_info_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    message = (
        "**🚀 الترقية إلى الخطة المدفوعة PRO 🚀**\n\n"
        "لماذا الترقية؟ لأنك تحصل على القوة الكاملة:\n\n"
        "- **أداء أسرع 20 ضعف (20x):**\n"
        "    - بوتاتك تعمل على موارد (معالج وذاكرة) أقوى بـ 20 مرة من الخطة المجانية، مما يعني استجابة فورية.\n\n"
        "- **بوتات صافية (بدون إضافات):**\n"
        "    - بوتاتك المستضافة على الخطة (PRO) تعمل **كما هي** بدون أي تدخل.\n"
        "    - **تنبيه:** البوتات على الخطة المجانية قد يتم إضافة **اشتراكات إجبارية** أو **إعلانات** *بداخلها* (أي داخل بوتاتك أنت) بشكل تلقائي لدعم الخدمة.\n\n"
        "- **ميزات حصرية (PRO):**\n"
        "    - **محرر أكواد 📝:** تعديل ملفاتك مباشرة من البوت.\n"
        "    - **تشغيل تجريبي 🔬:** لاكتشاف الأخطاء المتقدمة.\n\n"
        "- **أولوية تنفيذ:**\n"
        "    - يتم تنفيذ طلبات بوتاتك دائماً قبل المستخدمين المجانيين.\n"
        "- **حدود أعلى:**\n"
        "    - إمكانية رفع ملفات ومجلدات وبوتات أكثر.\n\n"
        f"**للدعم الفني:** تواصل مع مالك البوت: [اضغط هنا](tg://user?id={settings.telegram.SUDO_USERS[0]})"
    )
    buttons = [[Button.inline("↩️ القائمة الرئيسية", data="main_menu")]]
    await safe_edit_message(event, message, buttons=buttons, parse_mode='md')

async def pro_feature_locked_handler(event: events.CallbackQuery.Event):
    """Handles clicks on PRO-only features for free users."""
    feature = event.data.decode('utf-8').split(':')[1]
    feature_names = {
        'editor': 'محرر الأكواد',
        'test_run': 'التشغيل التجريبي',
        'webhook_log': 'سجل الويبهوك (Webhook)'
    }
    feature_name = feature_names.get(feature, 'هذه الميزة')
    
    await event.answer(f"🚫 {feature_name} متاحة فقط للمشتركين (PRO).", alert=True)
    await show_upgrade_info_handler(event)

def setup(client_instance: "TelegramClient"):
    """Registers all billing handlers with the TelegramClient."""
    client_instance.on(events.NewMessage(pattern=r'(?i)/redeem (.*)'))(redeem_handler)
    client_instance.on(events.CallbackQuery(pattern=b"show_upgrade_info"))(show_upgrade_info_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"pro_feature_locked:(.+)"))(pro_feature_locked_handler)
    # Add other handlers related to points/referrals here later.
    print("✅ Billing handlers registered.")