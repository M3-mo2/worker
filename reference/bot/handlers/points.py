# bot_v2/bot/handlers/points.py
import time
from datetime import datetime
from telethon import events
from telethon.tl.custom import Button
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telethon import TelegramClient

from bot.core.client import client
from bot.core.config import settings
from bot.core.state import conversation_manager
from bot.services.user_service import get_user_data, save_user_data, check_user_status
from bot.services.telegram import get_user_info
from bot.services.billing_service import update_user_bot_tiers
from bot.utils.telegram import safe_edit_message
from bot.utils.points import load_points_data, load_coupons, save_coupons
from bot.utils.time import _TZ

async def process_coupon(user_id: int, code: str) -> str:
    """Processes a coupon redemption request."""
    user_id_str = str(user_id)
    code = code.strip().lower()
    
    coupons = load_coupons()
    if code not in coupons:
        return "❌ **الكود غير صالح أو غير موجود.**"

    coupon = coupons[code]
    now = int(time.time())

    if now > coupon['expiry_ts']:
        return "⌛️ **عذراً، هذا الكود انتهت صلاحيته.**"

    if user_id_str in coupon['claimed_by']:
        return "🚫 **لقد قمت باستخدام هذا الكود من قبل.**"

    if len(coupon['claimed_by']) >= coupon['limit']:
        return "💔 **عذراً، لقد نفد العدد المسموح به لهذا الكود.**"

    # --- Claim Coupon ---
    coupon['claimed_by'].append(user_id_str)
    save_coupons(coupons)

    user_data = get_user_data(user_id)
    if not user_data:
         return "❌ حدث خطأ: بيانات المستخدم غير موجودة."

    points_to_add = coupon['points']
    user_data['points'] = user_data.get('points', 0) + points_to_add
    save_user_data(user_id, user_data)

    return f"🎉 **مبروك!**\n\n✅ تم إضافة **{points_to_add}** نقطة إلى رصيدك بنجاح!"

async def user_points_panel_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_data = get_user_data(sender_id)
    points = user_data.get('points', 0)
    
    bot_username = (await client.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref_{sender_id}"
    
    points_data = load_points_data()
    packages = points_data.get('packages', {})
    reward = points_data.get('referral_reward', 1)

    text = (
        f"**💰 رصيد المكافآت**\n\n"
        f"💎 **رصيدك الحالي:** `{points}` نقطة\n\n"
        f"� **رابط الدعوة:**\n`{ref_link}`\n\n"
        f"🎟️ **لديك قسيمة؟** اضغط على رابط القسيمة لتفعيلها.\n\n"
        f"� **كيف تكسب؟**\n"
        f"شارك الرابط مع أصدقائك. ستحصل على **{reward} نقطة** لكل صديق جديد ينضم للبوت.\n\n"
        f"🎁 **استبدال النقاط:**\n"
        f"اختر باقة من الأسفل لتفعيل اشتراك PRO فوراً:"
    )

    buttons = []
    # عرض الباقات كأزرار
    if packages:
        for pkg_id, pkg_info in packages.items():
            days = pkg_info['days']
            price = pkg_info['price']
            # التحقق مما إذا كان الرصيد يكفي لإظهار الزر بشكل مختلف (اختياري)
            btn_text = f"📅 {days} يوم ({price} نقطة)"
            buttons.append([Button.inline(btn_text, data=f"buy_pkg:{pkg_id}")])
    else:
        text += "\n\n🚫 لا توجد باقات متاحة حالياً."

    buttons.append([Button.inline("💸 تحويل نقاط", data="transfer_points")])
    buttons.append([Button.inline("↩️ القائمة الرئيسية", data="main_menu")])
    
    await safe_edit_message(event, text, buttons=buttons)

async def buy_package_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    pkg_id = event.data.decode('utf-8').split(':')[1]
    
    points_data = load_points_data()
    packages = points_data.get('packages', {})
    
    if pkg_id not in packages:
        return await event.answer("❌ هذه الباقة لم تعد متاحة.", alert=True)
    
    pkg = packages[pkg_id]
    cost = pkg['price']
    days = pkg['days']
    
    user_data = get_user_data(sender_id)
    current_points = user_data.get('points', 0)
    
    if current_points < cost:
        return await event.answer(f"❌ رصيدك غير كافٍ! تحتاج {cost} نقطة.", alert=True)
    
    # خصم النقاط
    user_data['points'] = current_points - cost
    
    # تفعيل الاشتراك
    now = int(time.time())
    current_expiry = user_data.get('plan_expiry')
    
    # إذا كان مشتركاً بالفعل ولم ينتهِ اشتراكه، نضيف الأيام للوقت المتبقي
    if user_data.get('plan') == 'pro' and current_expiry and current_expiry > now:
        new_expiry = current_expiry + (days * 86400)
    else:
        new_expiry = now + (days * 86400)
        
    user_data['plan'] = 'pro'
    user_data['plan_expiry'] = new_expiry
    user_data.pop('expiry_warning_sent', None) # إعادة تعيين التحذير
    
    save_user_data(sender_id, user_data)
    update_user_bot_tiers(str(sender_id), 'pro') # تحديث البوتات
    
    expiry_date = datetime.fromtimestamp(new_expiry, _TZ).strftime('%Y-%m-%d')
    
    await event.answer(f"🎉 تم شراء الباقة بنجاح! ({days} يوم)", alert=True)
    
    # تحديث الرسالة
    await user_points_panel_handler(event)
    
    # إشعار برسالة منفصلة
    await client.send_message(
        sender_id,
        f"✅ **تم تفعيل اشتراك PRO بنجاح!**\n\n"
        f"💎 تم خصم: `{cost}` نقطة\n"
        f"🗓️ المدة المضافة: `{days}` يوم\n"
        f"⏳ ينتهي في: `{expiry_date}`"
    )

async def transfer_points_prompt(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    points_data = load_points_data()
    fee = points_data.get('transfer_fee', 1)
    
    user_data = get_user_data(sender_id)
    points = user_data.get('points', 0)
    
    if points <= fee:
        return await event.answer(f"❌ رصيدك غير كافٍ للتحويل. الحد الأدنى: {fee + 1} نقطة.", alert=True)

    conversation_manager.set_state(sender_id, "awaiting_transfer_recipient", message_id=event.message_id)
    await safe_edit_message(event, f"**💸 تحويل نقاط**\n\n💰 رصيدك الحالي: `{points}`\n🧾 رسوم التحويل: `{fee}` نقطة\n\nأرسل الآن **ID المستخدم** أو **المعرف (Username)** للشخص الذي تريد التحويل له.", buttons=[[Button.inline("إلغاء ❌", data="main_menu")]])

async def user_points_conversation_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    status = state.get('status')
    msg_id = state.get('message_id')
    
    if status == "awaiting_transfer_recipient":
        user_input = event.text.strip()
        recipient_info = await get_user_info(user_input)
        
        if not recipient_info:
            return await event.reply("❌ لم أتمكن من العثور على هذا المستخدم. تأكد من المعرف وحاول مرة أخرى.")
        
        if recipient_info['id'] == sender_id:
            return await event.reply("❌ لا يمكنك تحويل النقاط لنفسك!")
            
        conversation_manager.set_state(sender_id, "awaiting_transfer_amount", context={'recipient': recipient_info}, message_id=msg_id)
        await event.reply(f"👤 المستلم: **{recipient_info['first_name']}**\n\n🔢 أرسل الآن **عدد النقاط** التي تريد تحويلها.")

    elif status == "awaiting_transfer_amount":
        try:
            amount = int(event.text.strip())
            if amount <= 0: return await event.reply("❌ يجب أن يكون المبلغ أكبر من صفر.")
            
            points_data = load_points_data()
            fee = points_data.get('transfer_fee', 1)
            total_deduction = amount + fee
            
            sender_data = get_user_data(sender_id)
            if sender_data.get('points', 0) < total_deduction:
                return await event.reply(f"❌ رصيدك غير كافٍ!\nالمطلوب: {total_deduction} (شامل الرسوم)\nالمتوفر: {sender_data.get('points', 0)}")
            
            recipient_info = state['context']['recipient']
            recipient_id = recipient_info['id']
            recipient_data = get_user_data(recipient_id)
            
            if not recipient_data: # Ensure recipient exists in DB
                recipient_data = {"first_name": recipient_info['first_name'], "username": recipient_info['username'], "points": 0}
            
            # Execute Transfer
            sender_data['points'] -= total_deduction
            recipient_data['points'] = recipient_data.get('points', 0) + amount
            
            save_user_data(sender_id, sender_data)
            save_user_data(recipient_id, recipient_data)
            
            await event.reply(f"✅ **تم التحويل بنجاح!**\n\n📤 المبلغ المحول: `{amount}`\n🧾 الرسوم: `{fee}`\n💰 رصيدك المتبقي: `{sender_data['points']}`")
            
            # Notify Recipient
            try:
                await client.send_message(recipient_id, f"💸 **استلمت حوالة نقاط جديدة!**\n\n👤 من: {sender_data.get('first_name')}\n💰 المبلغ: `{amount}` نقطة")
            except: pass
            
            conversation_manager.delete_state(sender_id)
        except ValueError:
            await event.reply("❌ الرجاء إرسال رقم صحيح.")

async def redeem_coupon_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    user_id_str = str(sender_id)
    
    try:
        code = event.pattern_match.group(1).strip().lower()
        if not code:
            return await event.reply("❌ يرجى إرسال الكود مع الأمر. مثال: `/redeem_coupon mycode123`")
    except:
        return await event.reply("❌ صيغة الأمر خاطئة. مثال: `/redeem_coupon mycode123`")

    msg = await process_coupon(sender_id, code)
    await event.reply(msg)

def setup(client_instance: "TelegramClient"):
    client_instance.on(events.CallbackQuery(pattern=b"my_points"))(user_points_panel_handler)
    client_instance.on(events.CallbackQuery(pattern=rb"buy_pkg:(.+)"))(buy_package_handler)
    client_instance.on(events.CallbackQuery(pattern=b"transfer_points"))(transfer_points_prompt)
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.get_status(e.sender_id) in ["awaiting_transfer_recipient", "awaiting_transfer_amount"]))(user_points_conversation_handler)
    client_instance.on(events.NewMessage(pattern=r'/redeem_coupon(?: (.*))?'))(redeem_coupon_handler)
    print("✅ Points User handlers registered.")
