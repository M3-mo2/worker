# bot_v2/bot/handlers/admin/points.py
import time
import uuid
from telethon import events
from telethon.tl.custom import Button
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telethon import TelegramClient

from bot.core.state import conversation_manager
from bot.services.user_service import check_user_status
from bot.services.user_service import get_user_data, save_user_data
from bot.services.telegram import get_user_info
from bot.utils.telegram import safe_edit_message
from bot.utils.points import load_points_data, save_points_data, load_coupons, save_coupons

# --- UI Functions ---
def get_points_admin_buttons():
    data = load_points_data()
    reward = data.get('referral_reward', 1)
    fee = data.get('transfer_fee', 1)
    
    return [
        [Button.inline(f"⚙️ نقاط الدعوة: {reward}", data="admin:set_ref_reward"), Button.inline(f"⚙️ رسوم التحويل: {fee}", data="admin:set_transfer_fee")],
        [Button.inline("➕ إضافة نقاط", data="admin:add_points"), Button.inline("➖ خصم نقاط", data="admin:rem_points")],
        [Button.inline("🎟️ إنشاء قسيمة نقاط", data="admin:create_coupon")],
        [Button.inline("➕ إضافة باقة", data="admin:add_pkg"), Button.inline("✏️ تعديل باقة", data="admin:edit_pkg_menu")],
        [Button.inline("🗑️ حذف باقة", data="admin:del_pkg_menu"), Button.inline("📋 عرض الباقات", data="admin:list_pkgs")],
        [Button.inline("⬅️ رجوع", data="admin:main_menu")]
    ]

async def send_points_admin_panel(event):
    text = "**💎 إدارة نظام النقاط والمكافآت**\n\nتحكم في سعر النقاط والباقات المتاحة للمستخدمين."
    await safe_edit_message(event, text, buttons=get_points_admin_buttons())

# --- Handlers ---

async def points_admin_menu_callback(event):
    if check_user_status(event.sender_id) != 'sudo': return
    await send_points_admin_panel(event)

# 1. Set Referral Reward
async def set_ref_reward_prompt(event):
    sender_id = event.sender_id
    conversation_manager.set_state(sender_id, "awaiting_ref_reward", message_id=event.message_id)
    await safe_edit_message(event, "**⚙️ تحديد نقاط الدعوة**\n\nأرسل الرقم الجديد للنقاط التي يكسبها المستخدم عند دعوة شخص جديد.", buttons=[[Button.inline("إلغاء ❌", data="admin:points_menu")]])

# 1.5 Set Transfer Fee
async def set_transfer_fee_prompt(event):
    sender_id = event.sender_id
    conversation_manager.set_state(sender_id, "awaiting_transfer_fee", message_id=event.message_id)
    await safe_edit_message(event, "**⚙️ تحديد رسوم التحويل**\n\nأرسل الرقم الجديد للرسوم التي يتم خصمها عند تحويل النقاط بين المستخدمين.", buttons=[[Button.inline("إلغاء ❌", data="admin:points_menu")]])

# 1.6 Add/Rem Points Prompts
async def add_points_prompt(event):
    sender_id = event.sender_id
    conversation_manager.set_state(sender_id, "awaiting_add_points_user", message_id=event.message_id)
    await safe_edit_message(event, "**➕ إضافة نقاط لمستخدم**\n\nأرسل الآن **ID المستخدم** أو **المعرف (Username)**.", buttons=[[Button.inline("إلغاء ❌", data="admin:points_menu")]])

async def rem_points_prompt(event):
    sender_id = event.sender_id
    conversation_manager.set_state(sender_id, "awaiting_rem_points_user", message_id=event.message_id)
    await safe_edit_message(event, "**➖ خصم نقاط من مستخدم**\n\nأرسل الآن **ID المستخدم** أو **المعرف (Username)**.", buttons=[[Button.inline("إلغاء ❌", data="admin:points_menu")]])

# 1.7 Coupon Creation Prompt
async def create_coupon_prompt(event):
    sender_id = event.sender_id
    conversation_manager.set_state(sender_id, "awaiting_coupon_points", message_id=event.message_id)
    await safe_edit_message(event, "**🎟️ إنشاء قسيمة جديدة (1/3)**\n\nأرسل عدد **النقاط** التي تمنحها هذه القسيمة.", buttons=[[Button.inline("إلغاء ❌", data="admin:points_menu")]])

# 2. Add Package
async def add_pkg_prompt(event):
    sender_id = event.sender_id
    conversation_manager.set_state(sender_id, "awaiting_pkg_days", message_id=event.message_id)
    await safe_edit_message(event, "**➕ إضافة باقة جديدة (1/2)**\n\nأرسل عدد **الأيام** لهذه الباقة.", buttons=[[Button.inline("إلغاء ❌", data="admin:points_menu")]])

# 3. List/Delete/Edit Menus
async def list_pkgs_callback(event):
    data = load_points_data()
    pkgs = data.get('packages', {})
    if not pkgs:
        return await event.answer("لا توجد باقات.", alert=True)
    
    text = "**📋 الباقات الحالية:**\n\n"
    for pid, info in pkgs.items():
        text += f"▫️ **{info['days']} يوم** مقابل **{info['price']} نقطة**\n"
    
    await safe_edit_message(event, text, buttons=[[Button.inline("⬅️ رجوع", data="admin:points_menu")]])

async def edit_pkg_menu_callback(event):
    data = load_points_data()
    pkgs = data.get('packages', {})
    if not pkgs: return await event.answer("لا توجد باقات لتعديلها.", alert=True)
    
    buttons = []
    for pid, info in pkgs.items():
        buttons.append([Button.inline(f"✏️ {info['days']} يوم - {info['price']} نقطة", data=f"admin:edit_pkg_sel:{pid}")])
    buttons.append([Button.inline("⬅️ رجوع", data="admin:points_menu")])
    
    await safe_edit_message(event, "**✏️ اختر الباقة التي تريد تعديلها:**", buttons=buttons)

async def del_pkg_menu_callback(event):
    data = load_points_data()
    pkgs = data.get('packages', {})
    if not pkgs: return await event.answer("لا توجد باقات لحذفها.", alert=True)
    
    buttons = []
    for pid, info in pkgs.items():
        buttons.append([Button.inline(f"🗑️ {info['days']} يوم - {info['price']} نقطة", data=f"admin:del_pkg_confirm:{pid}")])
    buttons.append([Button.inline("⬅️ رجوع", data="admin:points_menu")])
    
    await safe_edit_message(event, "**🗑️ اختر الباقة لحذفها نهائياً:**", buttons=buttons)

# 4. Edit Package Selection
async def edit_pkg_select_handler(event):
    pkg_id = event.data.decode().split(':')[2]
    data = load_points_data()
    if pkg_id not in data['packages']:
        return await event.answer("الباقة غير موجودة.", alert=True)
    
    pkg = data['packages'][pkg_id]
    text = f"**✏️ تعديل الباقة:**\n\n🗓️ الأيام: `{pkg['days']}`\n💰 السعر: `{pkg['price']}` نقطة\n\nماذا تريد أن تعدل؟"
    buttons = [
        [Button.inline("تعديل الأيام 🗓️", data=f"admin:edit_pkg_days:{pkg_id}"), Button.inline("تعديل السعر 💰", data=f"admin:edit_pkg_price:{pkg_id}")],
        [Button.inline("⬅️ رجوع للقائمة", data="admin:edit_pkg_menu")]
    ]
    await safe_edit_message(event, text, buttons=buttons)

async def edit_pkg_field_prompt(event):
    sender_id = event.sender_id
    parts = event.data.decode().split(':')
    field = parts[1] # edit_pkg_days or edit_pkg_price
    pkg_id = parts[2]
    
    field_name = "الأيام" if "days" in field else "السعر"
    state_key = "awaiting_edit_days" if "days" in field else "awaiting_edit_price"
    
    conversation_manager.set_state(sender_id, state_key, context={'pkg_id': pkg_id}, message_id=event.message_id)
    await safe_edit_message(event, f"**✏️ تعديل {field_name}**\n\nأرسل القيمة الجديدة الآن.", buttons=[[Button.inline("إلغاء ❌", data="admin:points_menu")]])

# 5. Delete Confirmation & Action
async def del_pkg_confirm_handler(event):
    pkg_id = event.data.decode().split(':')[2]
    data = load_points_data()
    if pkg_id not in data['packages']:
        return await event.answer("الباقة غير موجودة.", alert=True)
    
    pkg = data['packages'][pkg_id]
    text = f"**🗑️ هل أنت متأكد من حذف هذه الباقة؟**\n\n`{pkg['days']} يوم مقابل {pkg['price']} نقطة`\n\n**لا يمكن التراجع عن هذا الإجراء.**"
    buttons = [
        [Button.inline("✅ نعم، احذف", data=f"admin:del_pkg_do:{pkg_id}")],
        [Button.inline("❌ لا، تراجع", data="admin:del_pkg_menu")]
    ]
    await safe_edit_message(event, text, buttons=buttons)

async def del_pkg_do_handler(event):
    pkg_id = event.data.decode().split(':')[2]
    data = load_points_data()
    if pkg_id in data['packages']:
        del data['packages'][pkg_id]
        save_points_data(data)
        await event.answer("✅ تم حذف الباقة بنجاح.", alert=True)
    else:
        await event.answer("⚠️ الباقة تم حذفها بالفعل.", alert=True)
    await del_pkg_menu_callback(event)

# --- Conversation Handler ---
async def points_conversation_handler(event):
    sender_id = event.sender_id
    state = conversation_manager.get_state(sender_id)
    if not state: 
        return
        
    status = state.get('status')
    msg_id = state.get('message_id')
    text = event.text.strip()
    
    data = load_points_data()

    # --- 1. Handle Text-based Inputs (Usernames, Codes) ---
    
    # Add/Rem Points: User selection
    if status in ["awaiting_add_points_user", "awaiting_rem_points_user"]:
        user_input = text
        user_info = await get_user_info(user_input)
        
        if not user_info:
            return await event.reply("❌ لم أتمكن من العثور على هذا المستخدم. حاول مرة أخرى.")
        
        next_state = "awaiting_add_points_amount" if status == "awaiting_add_points_user" else "awaiting_rem_points_amount"
        conversation_manager.set_state(sender_id, next_state, context={'target_user': user_info}, message_id=msg_id)
        
        action_text = "إضافتها إلى" if "add" in status else "خصمها من"
        return await event.reply(f"👤 المستخدم: **{user_info['first_name']}** (`{user_info['id']}`)\n\n🔢 أرسل الآن كمية النقاط التي تريد {action_text} رصيده.")

    # Coupon Creation: Custom Code
    if status == "awaiting_coupon_code":
        code = text.lower()
        if code == 'auto':
            code = f"p-{uuid.uuid4().hex[:8]}"
        
        coupons = load_coupons()
        if code in coupons:
            return await event.reply("❌ هذا الكود مستخدم بالفعل. يرجى اختيار كود آخر.")

        context = state['context']
        coupons[code] = {
            "points": context['points'],
            "limit": context['limit'],
            "expiry_ts": int(time.time()) + (context['expiry_hours'] * 3600),
            "created_at": int(time.time()),
            "claimed_by": []
        }
        save_coupons(coupons)
        
        bot_username = (await event.client.get_me()).username
        coupon_link = f"https://t.me/{bot_username}?start=coupon_{code}"

        await event.reply(
            f"✅ **تم إنشاء القسيمة بنجاح!**\n\n"
            f"🔑 **الكود:** `{code}` (اضغط للنسخ)\n"
            f"🔗 **الرابط:** `{coupon_link}` (اضغط للنسخ)\n"
            f"💎 **النقاط:** {context['points']}\n"
            f"👥 **الحد:** {context['limit']} مستخدم\n"
            f"⏳ **الصلاحية:** {context['expiry_hours']} ساعة"
        )
        conversation_manager.delete_state(sender_id)
        return await send_points_admin_panel(await event.client.get_messages(sender_id, ids=msg_id))

    # --- 2. Handle Numeric Inputs ---
    
    if not text.isdigit():
        return await event.reply("❌ الرجاء إرسال أرقام فقط.")
    
    val = int(text)

    if status == "awaiting_ref_reward":
        data['referral_reward'] = val
        save_points_data(data)
        await event.reply(f"✅ تم تحديث نقاط الدعوة إلى: {val}")
        conversation_manager.delete_state(sender_id)
        await send_points_admin_panel(await event.client.get_messages(sender_id, ids=msg_id))

    elif status == "awaiting_transfer_fee":
        data['transfer_fee'] = val
        save_points_data(data)
        await event.reply(f"✅ تم تحديث رسوم التحويل إلى: {val}")
        conversation_manager.delete_state(sender_id)
        await send_points_admin_panel(await event.client.get_messages(sender_id, ids=msg_id))

    elif status == "awaiting_pkg_days":
        conversation_manager.set_state(sender_id, "awaiting_pkg_price", context={'days': val}, message_id=msg_id)
        await event.reply(f"🗓️ الأيام: {val}\n💰 أرسل الآن **سعر الباقة** بالنقاط.")
        
    elif status == "awaiting_pkg_price":
        days = state['context']['days']
        pkg_id = f"pkg_{uuid.uuid4().hex[:6]}"
        data['packages'][pkg_id] = {"days": days, "price": val}
        save_points_data(data)
        await event.reply(f"✅ تم إضافة الباقة: {days} يوم مقابل {val} نقطة.")
        conversation_manager.delete_state(sender_id)
        await send_points_admin_panel(await event.client.get_messages(sender_id, ids=msg_id))

    elif status in ["awaiting_edit_days", "awaiting_edit_price"]:
        pkg_id = state['context']['pkg_id']
        if pkg_id in data['packages']:
            if status == "awaiting_edit_days":
                data['packages'][pkg_id]['days'] = val
            else:
                data['packages'][pkg_id]['price'] = val
            save_points_data(data)
            await event.reply("✅ تم التعديل بنجاح.")
        else:
            await event.reply("❌ الباقة لم تعد موجودة.")
        
        conversation_manager.delete_state(sender_id)
        await send_points_admin_panel(await event.client.get_messages(sender_id, ids=msg_id))

    elif status in ["awaiting_add_points_amount", "awaiting_rem_points_amount"]:
        target_user = state['context']['target_user']
        amount = val
        
        user_data = get_user_data(target_user['id'])
        if not user_data:
            user_data = {"first_name": target_user['first_name'], "username": target_user['username'], "points": 0}
        
        current_points = user_data.get('points', 0)
        
        if status == "awaiting_add_points_amount":
            new_points = current_points + amount
            msg = f"✅ تم إضافة **{amount}** نقطة.\n💰 الرصيد الجديد: **{new_points}**"
            try:
                await event.client.send_message(target_user['id'], f"🎁 **تم إضافة {amount} نقطة إلى رصيدك بواسطة الأدمن.**\n💰 رصيدك الحالي: `{new_points}`")
            except: pass
        else:
            new_points = max(0, current_points - amount)
            msg = f"✅ تم خصم **{amount}** نقطة.\n💰 الرصيد الجديد: **{new_points}**"
            try:
                await event.client.send_message(target_user['id'], f"⚠️ **تم خصم {amount} نقطة من رصيدك بواسطة الأدمن.**\n💰 رصيدك الحالي: `{new_points}`")
            except: pass
            
        user_data['points'] = new_points
        save_user_data(target_user['id'], user_data)
        
        await event.reply(msg)
        conversation_manager.delete_state(sender_id)
        await send_points_admin_panel(await event.client.get_messages(sender_id, ids=msg_id))

    elif status == "awaiting_coupon_points":
        points = val
        conversation_manager.set_state(sender_id, "awaiting_coupon_limit", context={'points': points}, message_id=msg_id)
        await event.reply(f"🎟️ النقاط: {points}\n\n👥 أرسل الآن **عدد المستخدمين** المسموح لهم باستخدام هذه القسيمة.")

    elif status == "awaiting_coupon_limit":
        limit = val
        points = state['context']['points']
        conversation_manager.set_state(sender_id, "awaiting_coupon_expiry", context={'points': points, 'limit': limit}, message_id=msg_id)
        await event.reply(f"👥 الحد الأقصى: {limit}\n\n⏳ أرسل الآن **مدة صلاحية القسيمة بالساعات** (مثال: 24).")

    elif status == "awaiting_coupon_expiry":
        expiry_hours = val
        limit = state['context']['limit']
        points = state['context']['points']
        conversation_manager.set_state(sender_id, "awaiting_coupon_code", context={'points': points, 'limit': limit, 'expiry_hours': expiry_hours}, message_id=msg_id)
        await event.reply(f"⏳ الصلاحية: {expiry_hours} ساعة\n\n🔑 أرسل الآن **كود القسيمة** (نص من اختيارك) أو أرسل `auto` لإنشاء كود عشوائي.")

def setup(client):
    client.on(events.CallbackQuery(pattern=b"admin:points_menu"))(points_admin_menu_callback)
    client.on(events.CallbackQuery(pattern=b"admin:set_ref_reward"))(set_ref_reward_prompt)
    client.on(events.CallbackQuery(pattern=b"admin:set_transfer_fee"))(set_transfer_fee_prompt)
    client.on(events.CallbackQuery(pattern=b"admin:add_points"))(add_points_prompt)
    client.on(events.CallbackQuery(pattern=b"admin:rem_points"))(rem_points_prompt)
    client.on(events.CallbackQuery(pattern=b"admin:create_coupon"))(create_coupon_prompt)
    client.on(events.CallbackQuery(pattern=b"admin:add_pkg"))(add_pkg_prompt)
    client.on(events.CallbackQuery(pattern=b"admin:list_pkgs"))(list_pkgs_callback)
    client.on(events.CallbackQuery(pattern=b"admin:edit_pkg_menu"))(edit_pkg_menu_callback)
    client.on(events.CallbackQuery(pattern=b"admin:del_pkg_menu"))(del_pkg_menu_callback)
    client.on(events.CallbackQuery(pattern=rb"admin:edit_pkg_sel:(.+)"))(edit_pkg_select_handler)
    client.on(events.CallbackQuery(pattern=rb"admin:edit_pkg_(days|price):(.+)"))(edit_pkg_field_prompt)
    client.on(events.CallbackQuery(pattern=rb"admin:del_pkg_confirm:(.+)"))(del_pkg_confirm_handler)
    client.on(events.CallbackQuery(pattern=rb"admin:del_pkg_do:(.+)"))(del_pkg_do_handler)
    
    client.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.get_status(e.sender_id) in [
        "awaiting_ref_reward", "awaiting_transfer_fee", "awaiting_pkg_days", "awaiting_pkg_price", 
        "awaiting_edit_days", "awaiting_edit_price", "awaiting_add_points_user", "awaiting_rem_points_user",
        "awaiting_add_points_amount", "awaiting_rem_points_amount", "awaiting_coupon_points",
        "awaiting_coupon_limit", "awaiting_coupon_expiry", "awaiting_coupon_code"
    ]))(points_conversation_handler)
    print("✅ Admin Points handlers registered.")
