import telebot
from telebot import types
import requests
import random
import json
import re
import datetime
import time
import os
import traceback
import uuid
import threading
import schedule
from threading import Thread
from http.client import RemoteDisconnected

asia_sessions = {}
tok = '8223292937:AAF-tn3ay6Vl42hzQnoojW0_NP2uuYGFSOA'
bot = telebot.TeleBot(tok)
('Connection aborted.', RemoteDisconnected(...))



ADMIN_GROUP_ID = -1005206605776
CHANNEL_ID = -1002411534115
AUCTION_ADMIN = "@iTeo1"
ASIA_CELL_RECEIVER = "07776798777"

ID_AD = [-1005206605776, 6702239314, 56392509]

USERS_FILE = 'users.json'
PENDING_REQUESTS_FILE = 'pending_requests.json'
CODES_FILE = 'codes.json'
SETTINGS_FILE = 'settings.json'
ACTIVE_AUCTIONS_FILE = 'active_auctions.json'
PAYMENT_SETTINGS_FILE = 'payment_settings.json'
USER_STATES_FILE = 'user_states.json'
REFERRAL_FILE = 'referrals.json'
PAYMENT_METHODS_FILE = 'payment_methods.json'
PUBLISH_COOLDOWN_FILE = 'publish_cooldown.json'
SUBSCRIPTION_FILE = 'subscription_channels.json'

def init_files():
    os.makedirs("user_states", exist_ok=True)
    
    files = [
        (USERS_FILE, {}),
        (PENDING_REQUESTS_FILE, {"requests": {}, "next_id": 1}),
        (CODES_FILE, {}),
        (SETTINGS_FILE, {
            "channel_id": CHANNEL_ID,
            "admin_group": ADMIN_GROUP_ID,
            "auction_admin": AUCTION_ADMIN,
            "asia_number": ASIA_CELL_RECEIVER,
            "master_card_text": "💳 الدفع بـ ماستر كارد\n\nالرجاء التحويل إلى الرقم التالي:\nXXXX XXXX XXXX XXXX\n\nأرسل إيصال الدفع بعد التحويل",
            "zain_cash_text": "📲 الدفع بـ زين كاش\n\nالرجاء التحويل إلى الرقم التالي:\n0770XXXXXXX\n\nأرسل إيصال الدفع بعد التحويل",
            "terms_text": "<b>📜 شروط استخدام البوت:</b>\n\n1. يحق للإدارة تعديل الشروط دون إشعار\n2. يمنع استخدام البوت لأغراض غير قانونية\n3. جميع المبيعات نهائية\n4. النقاط غير قابلة للاسترجاع",
            "referral_points": 1
        }),
        (ACTIVE_AUCTIONS_FILE, {}),
        (PAYMENT_SETTINGS_FILE, {
            "asia_points_per_1000": 1.0,
            "stars_points_per_star": 1,
            "master_card_rate": 1000,
            "zain_cash_rate": 1000,
            "stars_price_per_100": 1.0,
        }),
        (USER_STATES_FILE, {}),
        (REFERRAL_FILE, {}),
        (PAYMENT_METHODS_FILE, {
            "methods": {
                "asia": {"name": "📱 آسيا سيل تلقائي", "enabled": True},
                "stars": {"name": "⭐ النجوم", "enabled": True},
                "master": {"name": "💳 ماستر كارد", "enabled": True},
                "zain": {"name": "📲 زين كاش", "enabled": True},
                "code": {"name": "💳 شحن برمز", "enabled": True}
            }
        }),
        (PUBLISH_COOLDOWN_FILE, {"last_publish": 0}),
        (SUBSCRIPTION_FILE, {
            "channels": [],
            "enabled": False
        })
    ]
    
    for file_path, default_data in files:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, indent=4, ensure_ascii=False)

def read_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def save_user_state(user_id, state_data):
    states = read_json(USER_STATES_FILE)
    states[str(user_id)] = state_data
    write_json(USER_STATES_FILE, states)

def load_user_state(user_id):
    states = read_json(USER_STATES_FILE)
    return states.get(str(user_id))

def clear_user_state(user_id):
    states = read_json(USER_STATES_FILE)
    if str(user_id) in states:
        del states[str(user_id)]
        write_json(USER_STATES_FILE, states)

def get_user_data(user_id):
    users = read_json(USERS_FILE)
    user_id = str(user_id)
    if user_id not in users:
        users[user_id] = {"points": 0, "balance": 0, "referrals": 0, "referral_code": str(user_id)}
    return users[user_id]

def update_user_data(user_id, **kwargs):
    users = read_json(USERS_FILE)
    user_id = str(user_id)
    
    if user_id not in users:
        users[user_id] = {"points": 0, "balance": 0, "referrals": 0, "referral_code": str(user_id)}
    
    users[user_id].update(kwargs)
    write_json(USERS_FILE, users)
    return users[user_id]

def add_user_points(user_id, points):
    user = get_user_data(user_id)
    user["points"] = user.get("points", 0) + points
    update_user_data(user_id, **user)
    return user["points"]

def subtract_user_points(user_id, points):
    user = get_user_data(user_id)
    current_points = user.get("points", 0)
    if current_points >= points:
        user["points"] = current_points - points
        update_user_data(user_id, **user)
        return True
    return False

def generate_code(amount):
    code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
    codes = read_json(CODES_FILE)
    codes[code] = {"amount": amount, "used": False, "generated_at": time.time()}
    write_json(CODES_FILE, codes)
    return code

def use_code(code, user_id):
    codes = read_json(CODES_FILE)
    code = code.upper()
    if code in codes and not codes[code]["used"]:
        amount = codes[code]["amount"]
        codes[code]["used"] = True
        codes[code]["user_id"] = user_id
        codes[code]["used_at"] = time.time()
        write_json(CODES_FILE, codes)
        return amount
    return 0

def save_request(req_type, user_id, data, points_required=0):
    requests_db = read_json(PENDING_REQUESTS_FILE)
    
    if "requests" not in requests_db:
        requests_db["requests"] = {}
    
    if "next_id" not in requests_db:
        requests_db["next_id"] = 1
    
    request_id = str(requests_db["next_id"])
    requests_db["next_id"] += 1
    
    requests_db["requests"][request_id] = {
        "id": request_id,
        "type": req_type,
        "user_id": user_id,
        "data": data,
        "status": "pending",
        "points_required": points_required,
        "timestamp": time.time(),
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    write_json(PENDING_REQUESTS_FILE, requests_db)
    return request_id

def update_request_status(request_id, status):
    requests_db = read_json(PENDING_REQUESTS_FILE)
    
    if "requests" not in requests_db:
        return False
    
    if request_id in requests_db["requests"]:
        requests_db["requests"][request_id]["status"] = status
        write_json(PENDING_REQUESTS_FILE, requests_db)
        return True
    return False

def get_request_data(request_id):
    requests_db = read_json(PENDING_REQUESTS_FILE)
    
    if "requests" not in requests_db:
        return None
    
    return requests_db["requests"].get(request_id)

def save_active_auction(message_id, gift_link, end_time, gift_type="forced"):
    auctions = read_json(ACTIVE_AUCTIONS_FILE)
    auctions[str(message_id)] = {
        "gift_link": gift_link,
        "end_time": end_time,
        "gift_type": gift_type,
        "start_time": time.time(),
        "last_update": time.time(),
        "active": True
    }
    write_json(ACTIVE_AUCTIONS_FILE, auctions)
    return message_id

def remove_active_auction(message_id):
    auctions = read_json(ACTIVE_AUCTIONS_FILE)
    if str(message_id) in auctions:
        del auctions[str(message_id)]
        write_json(ACTIVE_AUCTIONS_FILE, auctions)
        return True
    return False

def get_active_auction(message_id):
    auctions = read_json(ACTIVE_AUCTIONS_FILE)
    return auctions.get(str(message_id))

def update_auction_time(message_id, remaining_time):
    auctions = read_json(ACTIVE_AUCTIONS_FILE)
    if str(message_id) in auctions:
        auctions[str(message_id)]["last_update"] = time.time()
        write_json(ACTIVE_AUCTIONS_FILE, auctions)
        return True
    return False

def can_publish():
    cooldown_data = read_json(PUBLISH_COOLDOWN_FILE)
    last_publish = cooldown_data.get("last_publish", 0)
    current_time = time.time()
    
    if current_time - last_publish >= 300:  # 5 دقائق
        return True
    return False

def set_last_publish():
    cooldown_data = read_json(PUBLISH_COOLDOWN_FILE)
    cooldown_data["last_publish"] = time.time()
    write_json(PUBLISH_COOLDOWN_FILE, cooldown_data)

def publish_gift_to_channel(gift_link, gift_type):
    if not can_publish():
        return "cooldown"
    
    settings = read_json(SETTINGS_FILE)
    channel_id = settings.get("channel_id", CHANNEL_ID)
    
    try:
        if gift_type == "forced":
            total_seconds = 900
            end_time = time.time() + total_seconds
            mins, secs = divmod(total_seconds, 60)
            
            base_text = f"""<blockquote><b>مزاد  - ‏ Auction • <a href="{gift_link}">Click</a> ⌛ {mins:02d}:{secs:02d}</b></blockquote>

<blockquote><b>"ركز اجباري لمدة 15 دقيقة فقط ويتم بيعها لأعلى سعر اجباري"</b></blockquote>

<blockquote><b>"(1as / 1ton) رجائا حط سعرك فقط مثل"</b></blockquote>

‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎"""
            
            msg = bot.send_message(
                channel_id,
                base_text,
                parse_mode='HTML',
                disable_web_page_preview=False
            )
            
            auction_id = save_active_auction(msg.message_id, gift_link, end_time, gift_type)
            set_last_publish()
            
            thread = threading.Thread(target=update_auction_timer, args=(channel_id, msg.message_id, gift_link, total_seconds))
            thread.daemon = True
            thread.start()
            
            return msg.message_id
            
        else:
            base_text = f"""<b>مزاد  - ‏ Auction • <a href="{gift_link}">Click</a></b>

<blockquote>(1as / 1ton) رجائا حط سعرك فقط مثل</blockquote>

‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎"""
            
            msg = bot.send_message(
                channel_id,
                base_text,
                parse_mode='HTML',
                disable_web_page_preview=False
            )
            
            set_last_publish()
            return msg.message_id
            
    except Exception as e:
        print(f"خطأ في نشر الهدية: {e}")
        return None

def publish_username_to_channel(username, username_type):
    if not can_publish():
        return "cooldown"
    
    settings = read_json(SETTINGS_FILE)
    channel_id = settings.get("channel_id", CHANNEL_ID)
    
    try:
        if username_type == "nft":
            auction_text = f"""<blockquote><b>Tele Username (NFT): @{username}</b></blockquote>

<blockquote>- ممنوع الكلام داخل المناقشة 
- ممنوع تعطي سعر اقل من يلي قبلك
- حدد السعر مع العملة 

User Auction : @iTeo_Auction </blockquote>"""
        else:
            auction_text = f"""<blockquote><b>Tele Username: @{username}</b></blockquote>

<blockquote>- ممنوع الكلام داخل المناقشة 
- ممنوع تعطي سعر اقل من يلي قبلك
- حدد السعر مع العملة 

User Auction : @iTeo_Auction </blockquote>"""
        
        msg = bot.send_message(
            channel_id,
            auction_text,
            parse_mode='HTML'
        )
        
        set_last_publish()
        return msg.message_id
        
    except Exception as e:
        print(f"خطأ في نشر المعرف: {e}")
        return None

def update_auction_timer(channel_id, message_id, gift_link, total_seconds):
    auction_active = True
    update_count = 0
    
    while auction_active and update_count < 45:
        try:
            auction_data = get_active_auction(message_id)
            if not auction_data or not auction_data.get("active", True):
                auction_active = False
                break
            
            current_time = time.time()
            remaining = int(auction_data["end_time"] - current_time)
            
            if remaining <= 0:
                remaining = 0
                auction_active = False
            
            mins, secs = divmod(remaining, 60)
            
            base_text = f"""<blockquote><b>مزاد  - ‏ Auction • <a href="{gift_link}">Click</a> ⌛ {mins:02d}:{secs:02d}</b></blockquote>

<blockquote><b>"ركز اجباري لمدة 15 دقيقة فقط ويتم بيعها لأعلى سعر اجباري"</b></blockquote>

<blockquote><b>"(1as / 1ton) رجائا حط سعرك فقط مثل"</b></blockquote>
‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎"""
            
            bot.edit_message_text(
                chat_id=channel_id,
                message_id=message_id,
                text=base_text,
                parse_mode='HTML',
                disable_web_page_preview=False
            )
            
            update_auction_time(message_id, remaining)
            
            if remaining <= 0:
                auction_active = False
                break
            
            update_count += 1
            time.sleep(20)
            
        except telebot.apihelper.ApiTelegramException as e:
            if "message is not modified" in str(e):
                pass
            elif "message to edit not found" in str(e):
                auction_active = False
            else:
                print(f"خطأ في تحديث المؤقت: {e}")
                break
        except Exception as e:
            print(f"خطأ في تحديث المؤقت: {e}")
            break
    
    if update_count >= 45:
        try:
            final_text = f"""<blockquote><b>مزاد  - ‏ Auction • <a href="{gift_link}">Click</a> ⌛ 00:00</b></blockquote>

<blockquote><b>"ركز اجباري لمدة 15 دقيقة فقط ويتم بيعها لأعلى سعر اجباري"</b></blockquote>

<blockquote><b>"(1as / 1ton) رجائا حط سعرك فقط مثل"</b></blockquote>
‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎‏‏‎ ‎"""
            
            bot.edit_message_text(
                chat_id=channel_id,
                message_id=message_id,
                text=final_text,
                parse_mode='HTML',
                disable_web_page_preview=False
            )
        except:
            pass
    
    remove_active_auction(message_id)

def check_subscription(user_id):
    subscription_data = read_json(SUBSCRIPTION_FILE)
    
    if not subscription_data.get("enabled", False):
        return True
    
    channels = subscription_data.get("channels", [])
    
    for channel in channels:
        try:
            chat_member = bot.get_chat_member(channel, user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    
    return True

@bot.message_handler(commands=['start'])
def start_command(message):
    
    if not check_subscription(message.chat.id):
        subscription_data = read_json(SUBSCRIPTION_FILE)
        channels = subscription_data.get("channels", [])
        
        markup = types.InlineKeyboardMarkup()
        for channel in channels:
            try:
                channel_info = bot.get_chat(channel)
                btn = types.InlineKeyboardButton(f"اشترك في {channel_info.title}", url=f"https://t.me/{channel_info.username}")
                markup.add(btn)
            except:
                btn = types.InlineKeyboardButton(f"اشترك في القناة", url=f"https://t.me/{channel.replace('@', '')}")
                markup.add(btn)
        
        btn_check = types.InlineKeyboardButton("√ تحقق من الاشتراك", callback_data="check_subscription")
        markup.add(btn_check)
        
        bot.send_message(message.chat.id, "<b>⚠️ يجب الاشتراك في القنوات التالية لاستخدام البوت:</b>", parse_mode='HTML', reply_markup=markup)
        return
    
    
    if len(message.text.split()) > 1:
        referrer_id = message.text.split()[1]
        if referrer_id.isdigit() and int(referrer_id) != message.chat.id:
            referrals = read_json(REFERRAL_FILE)
            user_id = str(message.chat.id)
            
            if user_id not in referrals:
                referrals[user_id] = {"referrer": referrer_id, "joined_at": time.time()}
                write_json(REFERRAL_FILE, referrals)
                
                settings = read_json(SETTINGS_FILE)
                referral_points = settings.get("referral_points", 1)
                
                add_user_points(int(referrer_id), referral_points)
                referrer_data = get_user_data(int(referrer_id))
                referrer_data["referrals"] = referrer_data.get("referrals", 0) + 1
                update_user_data(int(referrer_id), **referrer_data)
    
    user = get_user_data(message.chat.id)
    
    welcome_msg = f"""<b>🎁 اهلا بك في بوت الهدايا</b>

<blockquote>🆔 ايديك: {message.chat.id}</blockquote>
<blockquote>💎 نقاطك: {user['points']}</blockquote>"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('💰 شحن رصيدي', callback_data='charge_menu')
    btn2 = types.InlineKeyboardButton('🎁 نشر هدية', callback_data='publish_gift_menu')
    btn3 = types.InlineKeyboardButton('📜 نشر معرف', callback_data='publish_username_menu')
    btn4 = types.InlineKeyboardButton('🔗 رابط المشاركة', callback_data='referral_link')
    btn5 = types.InlineKeyboardButton('📜 الشروط', callback_data='show_terms')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.send_message(message.chat.id, welcome_msg, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'check_subscription')
def check_subscription_callback(call):
    if check_subscription(call.message.chat.id):
        start_command(call.message)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        bot.answer_callback_query(call.id, "✗ لم تشترك في جميع القنوات المطلوبة", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == 'show_terms')
def show_terms(call):
    settings = read_json(SETTINGS_FILE)
    terms_text = settings.get("terms_text", "<b>📜 شروط استخدام البوت:</b>\n\n1. يحق للإدارة تعديل الشروط دون إشعار\n2. يمنع استخدام البوت لأغراض غير قانونية\n3. جميع المبيعات نهائية\n4. النقاط غير قابلة للاسترجاع")
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⤺ رجوع", callback_data="main_menu"))
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=terms_text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'referral_link')
def referral_link(call):
    user = get_user_data(call.message.chat.id)
    referral_url = f"https://t.me/{bot.get_me().username}?start={call.message.chat.id}"
    
    stats_text = f"""<b>🔗 رابط الدعوة 🔗</b>

<blockquote><b>👥 إحصائيات دعواتك:</b>
• عدد المدعوين: {user.get('referrals', 0)} شخص
• النقاط المكتسبة: {user.get('referrals', 0) * user.get('referrals', 0)} نقطة
• رصيدك الحالي: {user.get('points', 0)} نقطة</blockquote>

<blockquote><b>📋 كيفية كسب النقاط:</b>
• شارك الرابط مع أصدقائك
• كل صديق يدخل عبر رابطك يحصل على نقطة</blockquote>

<blockquote><b>📎 رابط الدعوة الخاص بك:</b>
{referral_url}</blockquote>"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⤺ رجوع", callback_data="main_menu"))
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=stats_text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def main_menu(call):
    user = get_user_data(call.message.chat.id)
    
    welcome_msg = f"""<b>🎁 اهلا بك في بوت الهدايا</b>

<blockquote>🆔 ايديك: {call.message.chat.id}</blockquote>
<blockquote>💎 نقاطك: {user['points']}</blockquote>"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('💰 شحن رصيدي', callback_data='charge_menu')
    btn2 = types.InlineKeyboardButton('🎁 نشر هدية', callback_data='publish_gift_menu')
    btn3 = types.InlineKeyboardButton('📜 نشر معرف', callback_data='publish_username_menu')
    btn4 = types.InlineKeyboardButton('🔗 رابط المشاركة', callback_data='referral_link')
    btn5 = types.InlineKeyboardButton('📜 الشروط', callback_data='show_terms')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=welcome_msg,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'charge_menu')
def charge_menu(call):
    payment_methods = read_json(PAYMENT_METHODS_FILE)

    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []

    if payment_methods["methods"]["asia"]["enabled"]:
        buttons.append(types.InlineKeyboardButton('اسياسيل📱 تلقائي', callback_data='charge_asia'))

    if payment_methods["methods"]["stars"]["enabled"]:
        buttons.append(types.InlineKeyboardButton('⭐ النجوم', callback_data='charge_stars'))

    if payment_methods["methods"]["master"]["enabled"]:
        buttons.append(types.InlineKeyboardButton('💳 ماستر كارد', callback_data='charge_master'))

    if payment_methods["methods"]["zain"]["enabled"]:
        buttons.append(types.InlineKeyboardButton('📲 زين كاش', callback_data='charge_zain'))

    if payment_methods["methods"]["code"]["enabled"]:
        buttons.append(types.InlineKeyboardButton('💳 شحن بكود', callback_data='charge_code'))

    if buttons:
        markup.add(*buttons)

    markup.add(types.InlineKeyboardButton('⤺ رجوع', callback_data='main_menu'))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>💰 اختر طريقة الشحن:</b>",
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'charge_code')
def charge_with_code(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>💳 أرسل رمز الشحن:</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, process_code)

def process_code(message):
    if message.text is None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ المحاولة مرة أخرى", callback_data="charge_code"))
        bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال نص</b>", parse_mode='HTML', reply_markup=markup)
        return
    
    code = message.text.strip().upper()
    amount = use_code(code, message.chat.id)
    
    if amount > 0:
        new_balance = add_user_points(message.chat.id, amount)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ القائمة الرئيسية", callback_data="main_menu"))
        
        bot.send_message(message.chat.id, 
                        f"""<b>√ تم الشحن بنجاح!</b>

<blockquote><b>📊 التفاصيل:</b>
• الكود: {code}
• المبلغ: {amount} نقطة
• رصيدك الجديد: {new_balance} نقطة</blockquote>""", 
                        parse_mode='HTML',
                        reply_markup=markup)
        
        try:
            bot.send_message(ADMIN_GROUP_ID,
                           f"""<b>🔔 إشعار شحن جديد</b>

<blockquote>👤 المستخدم: {message.chat.id}
🔢 الكود: {code}
💎 النقاط: {amount}
💰 الرصيد الجديد: {new_balance}</blockquote>""",
                           parse_mode='HTML')
        except:
            pass
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ المحاولة مرة أخرى", callback_data="charge_code"))
        bot.send_message(message.chat.id, "<b>✗ الرمز غير صالح أو مستخدم مسبقاً</b>", parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'charge_stars')
def charge_with_stars(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    instructions = """<b>⭐ شحن بالنجوم</b>

<blockquote>📌 أرسل عدد النجوم التي تريد شحنها:</blockquote>

<blockquote><i>ملاحظة: بعد إرسال العدد، سيطلب منك إرسال النجوم إلى حساب المسؤول</i></blockquote>"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⤺ رجوع", callback_data="charge_menu"))
    
    msg = bot.send_message(call.message.chat.id, instructions, parse_mode='HTML', reply_markup=markup)
    bot.register_next_step_handler(msg, process_stars_amount)

def process_stars_amount(message):
    try:
        if message.text is None:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ المحاولة مرة أخرى", callback_data="charge_stars"))
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال العدد</b>", parse_mode='HTML', reply_markup=markup)
            return
        
        stars_amount = int(message.text.strip())
        if stars_amount <= 0:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ المحاولة مرة أخرى", callback_data="charge_stars"))
            bot.send_message(message.chat.id, "<b>✗ العدد يجب أن يكون أكبر من صفر</b>", parse_mode='HTML', reply_markup=markup)
            return
        
        payment_settings = read_json(PAYMENT_SETTINGS_FILE)
        stars_rate = payment_settings.get("stars_points_per_star", 1)
        points_to_add = stars_amount * stars_rate
        
        request_id = save_request(
            "stars",
            message.chat.id,
            {"stars_amount": stars_amount, "points": points_to_add},
            0
        )
        
        settings = read_json(SETTINGS_FILE)
        auction_admin = settings.get("auction_admin", AUCTION_ADMIN)
        
        instructions = f"""<b>⭐ أرسل {stars_amount} نجمة إلى الحساب التالي:</b>

<blockquote>{auction_admin}</blockquote>

<blockquote>بعد الإرسال، اضغط على زر 'لقد أرسلت'</blockquote>"""
        
        markup = types.InlineKeyboardMarkup()
        btn_sent = types.InlineKeyboardButton("√ لقد أرسلت", callback_data=f"stars_sent_{request_id}")
        markup.add(btn_sent)
        
        bot.send_message(message.chat.id, instructions, parse_mode='HTML', reply_markup=markup)
        
    except ValueError:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ المحاولة مرة أخرى", callback_data="charge_stars"))
        bot.send_message(message.chat.id, "<b>✗ الرجاء إدخال رقم صحيح</b>", parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('stars_sent_'))
def stars_sent_confirmation(call):
    request_id = call.data.replace('stars_sent_', '')
    request_info = get_request_data(request_id)
    
    if not request_info:
        bot.answer_callback_query(call.id, "✗ الطلب غير موجود", show_alert=True)
        return
    
    user_id = call.from_user.id
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>√ تم إرسال طلبك للمراجعة! سيتم إعلامك بالقرار.</b>",
        parse_mode='HTML'
    )
    
    settings = read_json(SETTINGS_FILE)
    admin_group = settings.get("admin_group", ADMIN_GROUP_ID)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_approve = types.InlineKeyboardButton("√ موافقة", callback_data=f"stars_approve_{request_id}")
    btn_reject = types.InlineKeyboardButton("✗ رفض", callback_data=f"stars_reject_{request_id}")
    markup.add(btn_approve, btn_reject)
    
    request_text = f"""<b>⭐ طلب شحن بالنجوم</b>

<blockquote>👤 المستخدم: {user_id}
⭐ عدد النجوم: {request_info['data']['stars_amount']}
💎 النقاط المستحقة: {request_info['data']['points']}
📋 طلب ID: {request_id}</blockquote>"""
    
    bot.send_message(admin_group, request_text, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('stars_approve_', 'stars_reject_')))
def handle_stars_approval(call):
    if call.data.startswith('stars_approve_'):
        request_id = call.data.replace('stars_approve_', '')
        action = 'approve'
    else:
        request_id = call.data.replace('stars_reject_', '')
        action = 'reject'
    
    request_info = get_request_data(request_id)
    
    if not request_info:
        bot.answer_callback_query(call.id, "<b>✗ الطلب غير موجود</b>", show_alert=True)
        return
    
    user_id = int(request_info["user_id"])
    
    if action == 'approve':
        points_to_add = request_info["data"]["points"]
        new_balance = add_user_points(user_id, points_to_add)
        
        bot.send_message(user_id, 
                        f"""<b>√ تمت الموافقة على طلب الشحن!</b>

<blockquote><b>📊 التفاصيل:</b>
• النجوم: {request_info['data']['stars_amount']} نجمة
• النقاط المضافة: {points_to_add} نقطة
• رصيدك الجديد: {new_balance} نقطة</blockquote>""",
                        parse_mode='HTML')
        
        update_request_status(request_id, "approved")
        bot.answer_callback_query(call.id, "<b>√ تمت الموافقة على الطلب</b>", show_alert=True)
        
        
        try:
            new_text = f"""<b>⭐ طلب شحن بالنجوم - تمت الموافقة</b>

<blockquote>👤 المستخدم: {user_id}
⭐ عدد النجوم: {request_info['data']['stars_amount']}
💎 النقاط المستحقة: {request_info['data']['points']}
📋 طلب ID: {request_id}</blockquote>

<blockquote><i>√ تمت الموافقة من قبل: {call.from_user.first_name}</i></blockquote>"""
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode='HTML'
            )
        except:
            pass
        
    else:
        bot.send_message(user_id, "<b>✗ تم رفض طلب الشحن. يرجى التواصل مع المسؤول.</b>", parse_mode='HTML')
        update_request_status(request_id, "rejected")
        bot.answer_callback_query(call.id, "<b>✗ تم رفض الطلب</b>", show_alert=True)
        
        
        try:
            new_text = f"""<b>⭐ طلب شحن بالنجوم - تم الرفض</b>

<blockquote>👤 المستخدم: {user_id}
⭐ عدد النجوم: {request_info['data']['stars_amount']}
💎 النقاط المستحقة: {request_info['data']['points']}
📋 طلب ID: {request_id}</blockquote>

<blockquote><i>✗ تم الرفض من قبل: {call.from_user.first_name}</i></blockquote>"""
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode='HTML'
            )
        except:
            pass

@bot.callback_query_handler(func=lambda call: call.data == 'charge_master')
def charge_with_master(call):
    settings = read_json(SETTINGS_FILE)
    master_text = settings.get("master_card_text", "💳 الدفع بـ ماستر كارد\n\nالرجاء التحويل إلى الرقم التالي:\nXXXX XXXX XXXX XXXX\n\nأرسل إيصال الدفع بعد التحويل")
    
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("⤺ رجوع", callback_data="charge_menu")
    markup.add(btn_back)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"<b>{master_text}</b>",
        parse_mode='HTML',
        reply_markup=markup
    )
    
    user_state = {"state": "await_master_amount", "timestamp": time.time()}
    save_user_state(call.from_user.id, user_state)
    
    msg = bot.send_message(call.message.chat.id, 
                          "<b>💵 أرسل مبلغ التحويل (بالدينار):</b>",
                          parse_mode='HTML',
                          reply_markup=types.ReplyKeyboardRemove())
    
    bot.register_next_step_handler(msg, process_master_amount)

def process_master_amount(message):
    user_state = load_user_state(message.chat.id)
    
    if not user_state or user_state.get("state") != "await_master_amount":
        return
    
    clear_user_state(message.chat.id)
    
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال المبلغ</b>", parse_mode='HTML')
            return
            
        amount = int(message.text.strip())
        if amount <= 0:
            bot.send_message(message.chat.id, "<b>✗ المبلغ يجب أن يكون أكبر من صفر</b>", parse_mode='HTML')
            return
        
        payment_settings = read_json(PAYMENT_SETTINGS_FILE)
        master_rate = payment_settings.get("master_card_rate", 1000)
        points_to_add = int((amount / master_rate) * 1.0)
        
        if points_to_add <= 0:
            points_to_add = 1
        
        request_id = save_request(
            "master_card",
            message.chat.id,
            {"amount": amount, "points": points_to_add},
            0
        )
        
        instructions = f"""<b>📤 أرسل صورة إيصال التحويل</b>

<blockquote><b>المبلغ:</b> {amount} دينار
<b>النقاط المستحقة:</b> {points_to_add} نقطة</blockquote>

<blockquote><i>سيتم مراجعة طلبك من قبل المسؤول</i></blockquote>"""
        
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("⤺ إلغاء", callback_data="charge_menu")
        markup.add(btn_back)
        
        bot.send_message(message.chat.id, instructions, parse_mode='HTML', reply_markup=markup)
        
        user_state = {
            "state": "await_master_receipt",
            "request_id": request_id,
            "amount": amount,
            "points": points_to_add,
            "timestamp": time.time()
        }
        save_user_state(message.chat.id, user_state)
        
    except ValueError:
        bot.send_message(message.chat.id, "<b>✗ الرجاء إدخال رقم صحيح</b>", parse_mode='HTML')

@bot.message_handler(content_types=['photo'])
def handle_photo_message(message):
    user_state = load_user_state(message.chat.id)
    
    if not user_state:
        return
    
    if user_state.get("state") == "await_master_receipt":
        request_id = user_state.get("request_id")
        amount = user_state.get("amount")
        points_to_add = user_state.get("points")
        
        clear_user_state(message.chat.id)
        
        photo_id = message.photo[-1].file_id
        
        bot.send_message(message.chat.id, "<b>√ تم استلام إيصال الدفع. سيتم مراجعة طلبك قريباً.</b>", parse_mode='HTML')
        
        settings = read_json(SETTINGS_FILE)
        admin_group = settings.get("admin_group", ADMIN_GROUP_ID)
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_approve = types.InlineKeyboardButton("√ موافقة", callback_data=f"master_approve_{request_id}")
        btn_reject = types.InlineKeyboardButton("✗ رفض", callback_data=f"master_reject_{request_id}")
        markup.add(btn_approve, btn_reject)
        
        request_text = f"""<b>💳 طلب شحن بـ ماستر كارد</b>

<blockquote>👤 المستخدم: {message.chat.id}
💰 المبلغ: {amount} دينار
💎 النقاط المستحقة: {points_to_add}
📋 طلب ID: {request_id}</blockquote>"""
        
        bot.send_photo(admin_group, photo_id, caption=request_text, parse_mode='HTML', reply_markup=markup)
    
    elif user_state.get("state") == "await_zain_receipt":
        request_id = user_state.get("request_id")
        amount = user_state.get("amount")
        points_to_add = user_state.get("points")
        
        clear_user_state(message.chat.id)
        
        photo_id = message.photo[-1].file_id
        
        bot.send_message(message.chat.id, "<b>√ تم استلام إيصال الدفع. سيتم مراجعة طلبك قريباً.</b>", parse_mode='HTML')
        
        settings = read_json(SETTINGS_FILE)
        admin_group = settings.get("admin_group", ADMIN_GROUP_ID)
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_approve = types.InlineKeyboardButton("√ موافقة", callback_data=f"zain_approve_{request_id}")
        btn_reject = types.InlineKeyboardButton("✗ رفض", callback_data=f"zain_reject_{request_id}")
        markup.add(btn_approve, btn_reject)
        
        request_text = f"""<b>📲 طلب شحن بـ زين كاش</b>

<blockquote>👤 المستخدم: {message.chat.id}
💰 المبلغ: {amount} دينار
💎 النقاط المستحقة: {points_to_add}
📋 طلب ID: {request_id}</blockquote>"""
        
        bot.send_photo(admin_group, photo_id, caption=request_text, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('master_approve_', 'master_reject_')))
def handle_master_approval(call):
    if call.data.startswith('master_approve_'):
        request_id = call.data.replace('master_approve_', '')
        action = 'approve'
    else:
        request_id = call.data.replace('master_reject_', '')
        action = 'reject'
    
    request_info = get_request_data(request_id)
    
    if not request_info:
        bot.answer_callback_query(call.id, "<b>✗ الطلب غير موجود</b>", show_alert=True)
        return
    
    user_id = int(request_info["user_id"])
    
    if action == 'approve':
        points_to_add = request_info["data"]["points"]
        new_balance = add_user_points(user_id, points_to_add)
        
        bot.send_message(user_id, 
                        f"""<b>√ تمت الموافقة على طلب الشحن!</b>

<blockquote><b>📊 التفاصيل:</b>
• المبلغ: {request_info['data']['amount']} دينار
• النقاط المضافة: {points_to_add} نقطة
• رصيدك الجديد: {new_balance} نقطة</blockquote>""",
                        parse_mode='HTML')
        
        update_request_status(request_id, "approved")
        bot.answer_callback_query(call.id, "<b>√ تمت الموافقة على الطلب</b>", show_alert=True)
        
        
        try:
            new_text = f"""<b>💳 طلب شحن بـ ماستر كارد - تمت الموافقة</b>

<blockquote>👤 المستخدم: {user_id}
💰 المبلغ: {request_info['data']['amount']} دينار
💎 النقاط المستحقة: {points_to_add}
📋 طلب ID: {request_id}</blockquote>

<blockquote><i>√ تمت الموافقة من قبل: {call.from_user.first_name}</i></blockquote>"""
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode='HTML'
            )
        except:
            pass
        
    else:
        bot.send_message(user_id, "<b>✗ تم رفض طلب الشحن. يرجى التواصل مع المسؤول.</b>", parse_mode='HTML')
        update_request_status(request_id, "rejected")
        bot.answer_callback_query(call.id, "<b>✗ تم رفض الطلب</b>", show_alert=True)
        
        
        try:
            new_text = f"""<b>💳 طلب شحن بـ ماستر كارد - تم الرفض</b>

<blockquote>👤 المستخدم: {user_id}
💰 المبلغ: {request_info['data']['amount']} دينار
💎 النقاط المستحقة: {request_info['data']['points']}
📋 طلب ID: {request_id}</blockquote>

<blockquote><i>✗ تم الرفض من قبل: {call.from_user.first_name}</i></blockquote>"""
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode='HTML'
            )
        except:
            pass

@bot.callback_query_handler(func=lambda call: call.data == 'charge_zain')
def charge_with_zain(call):
    settings = read_json(SETTINGS_FILE)
    zain_text = settings.get("zain_cash_text", "📲 الدفع بـ زين كاش\n\nالرجاء التحويل إلى الرقم التالي:\n0770XXXXXXX\n\nأرسل إيصال الدفع بعد التحويل")
    
    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("⤺ رجوع", callback_data="charge_menu")
    markup.add(btn_back)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"<b>{zain_text}</b>",
        parse_mode='HTML',
        reply_markup=markup
    )
    
    user_state = {"state": "await_zain_amount", "timestamp": time.time()}
    save_user_state(call.from_user.id, user_state)
    
    msg = bot.send_message(call.message.chat.id, 
                          "<b>💵 أرسل مبلغ التحويل (بالدينار):</b>",
                          parse_mode='HTML',
                          reply_markup=types.ReplyKeyboardRemove())
    
    bot.register_next_step_handler(msg, process_zain_amount)

def process_zain_amount(message):
    user_state = load_user_state(message.chat.id)
    
    if not user_state or user_state.get("state") != "await_zain_amount":
        return
    
    clear_user_state(message.chat.id)
    
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال المبلغ</b>", parse_mode='HTML')
            return
            
        amount = int(message.text.strip())
        if amount <= 0:
            bot.send_message(message.chat.id, "<b>✗ المبلغ يجب أن يكون أكبر من صفر</b>", parse_mode='HTML')
            return
        
        payment_settings = read_json(PAYMENT_SETTINGS_FILE)
        zain_rate = payment_settings.get("zain_cash_rate", 1000)
        points_to_add = int((amount / zain_rate) * 1.0)
        
        if points_to_add <= 0:
            points_to_add = 1
        
        request_id = save_request(
            "zain_cash",
            message.chat.id,
            {"amount": amount, "points": points_to_add},
            0
        )
        
        instructions = f"""<b>📤 أرسل صورة إيصال التحويل</b>

<blockquote><b>المبلغ:</b> {amount} دينار
<b>النقاط المستحقة:</b> {points_to_add} نقطة</blockquote>

<blockquote><i>سيتم مراجعة طلبك من قبل المسؤول</i></blockquote>"""
        
        markup = types.InlineKeyboardMarkup()
        btn_back = types.InlineKeyboardButton("⤺ إلغاء", callback_data="charge_menu")
        markup.add(btn_back)
        
        bot.send_message(message.chat.id, instructions, parse_mode='HTML', reply_markup=markup)
        
        user_state = {
            "state": "await_zain_receipt",
            "request_id": request_id,
            "amount": amount,
            "points": points_to_add,
            "timestamp": time.time()
        }
        save_user_state(message.chat.id, user_state)
        
    except ValueError:
        bot.send_message(message.chat.id, "<b>✗ الرجاء إدخال رقم صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data.startswith(('zain_approve_', 'zain_reject_')))
def handle_zain_approval(call):
    if call.data.startswith('zain_approve_'):
        request_id = call.data.replace('zain_approve_', '')
        action = 'approve'
    else:
        request_id = call.data.replace('zain_reject_', '')
        action = 'reject'
    
    request_info = get_request_data(request_id)
    
    if not request_info:
        bot.answer_callback_query(call.id, "<b>✗ الطلب غير موجود</b>", show_alert=True)
        return
    
    user_id = int(request_info["user_id"])
    
    if action == 'approve':
        points_to_add = request_info["data"]["points"]
        new_balance = add_user_points(user_id, points_to_add)
        
        bot.send_message(user_id, 
                        f"""<b>√ تمت الموافقة على طلب الشحن!</b>

<blockquote><b>📊 التفاصيل:</b>
• المبلغ: {request_info['data']['amount']} دينار
• النقاط المضافة: {points_to_add} نقطة
• رصيدك الجديد: {new_balance} نقطة</blockquote>""",
                        parse_mode='HTML')
        
        update_request_status(request_id, "approved")
        bot.answer_callback_query(call.id, "<b>√ تمت الموافقة على الطلب</b>", show_alert=True)
        
        
        try:
            new_text = f"""<b>📲 طلب شحن بـ زين كاش - تمت الموافقة</b>

<blockquote>👤 المستخدم: {user_id}
💰 المبلغ: {request_info['data']['amount']} دينار
💎 النقاط المستحقة: {points_to_add}
📋 طلب ID: {request_id}</blockquote>

<blockquote><i>√ تمت الموافقة من قبل: {call.from_user.first_name}</i></blockquote>"""
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode='HTML'
            )
        except:
            pass
        
    else:
        bot.send_message(user_id, "<b>✗ تم رفض طلب الشحن. يرجى التواصل مع المسؤول.</b>", parse_mode='HTML')
        update_request_status(request_id, "rejected")
        bot.answer_callback_query(call.id, "<b>✗ تم رفض الطلب</b>", show_alert=True)
        
        
        try:
            new_text = f"""<b>📲 طلب شحن بـ زين كاش - تم الرفض</b>

<blockquote>👤 المستخدم: {user_id}
💰 المبلغ: {request_info['data']['amount']} دينار
💎 النقاط المستحقة: {request_info['data']['points']}
📋 طلب ID: {request_id}</blockquote>

<blockquote><i>✗ تم الرفض من قبل: {call.from_user.first_name}</i></blockquote>"""
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode='HTML'
            )
        except:
            pass

@bot.callback_query_handler(func=lambda call: call.data == 'publish_gift_menu')
def publish_gift_menu(call):
    user = get_user_data(call.from_user.id)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('🎁 نشر عادي (2 نقطة)', callback_data='publish_gift_normal')
    btn2 = types.InlineKeyboardButton('⚡ نشر إجباري (5 نقاط)', callback_data='publish_gift_forced')
    btn3 = types.InlineKeyboardButton('⤺ رجوع', callback_data='main_menu')
    markup.add(btn1, btn2, btn3)
    
    text = f"""<b>🎁 اختر نوع نشر الهدية</b>

<blockquote>💎 نقاطك الحالية: {user['points']}</blockquote>

<blockquote><b>• عادي:</b> 2 نقطة
<b>• إجباري:</b> 5 نقاط (مدة 15 دقيقة)</blockquote>"""
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'publish_gift_normal')
def publish_gift_normal(call):
    user = get_user_data(call.from_user.id)
    
    if user["points"] < 2:
        bot.answer_callback_query(call.id, "<b>✗ نقاطك غير كافية. تحتاج إلى نقطتين على الأقل</b>", show_alert=True)
        return
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    msg = bot.send_message(call.message.chat.id,
                          """<b>🎁 نشر هدية جديدة 🎁</b>

<blockquote>• أرسل رابط الهدية بالصيغة الصحيحة
• الرابط يجب أن يكون بهذا الشكل:
t.me/nft/GiftName-1234</blockquote>""",
                          parse_mode='HTML')
    bot.register_next_step_handler(msg, process_gift_link, "normal", 2)

@bot.callback_query_handler(func=lambda call: call.data == 'publish_gift_forced')
def publish_gift_forced(call):
    user = get_user_data(call.from_user.id)
    
    if user["points"] < 5:
        bot.answer_callback_query(call.id, "<b>✗ نقاطك غير كافية. تحتاج إلى 5 نقاط</b>", show_alert=True)
        return
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    msg = bot.send_message(call.message.chat.id,
                          """<b>⚡ نشر هدية إجبارية ⚡</b>

<blockquote>• أرسل رابط الهدية بالصيغة الصحيحة
• الرابط يجب أن يكون بهذا الشكل:
t.me/nft/GiftName-1234</blockquote>""",
                          parse_mode='HTML')
    bot.register_next_step_handler(msg, process_gift_link, "forced", 5)

def process_gift_link(message, gift_type, points_needed):
    if message.text is None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ المحاولة مرة أخرى", callback_data="publish_gift_menu"))
        bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال الرابط</b>", parse_mode='HTML', reply_markup=markup)
        return
    
    gift_link = message.text.strip()
    
    if gift_link.startswith("https://"):
        gift_link = gift_link.replace("https://", "")
    
    if not gift_link.startswith("t.me/nft/"):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ المحاولة مرة أخرى", callback_data="publish_gift_menu"))
        bot.send_message(message.chat.id, 
                        "<b>✗ رابط غير صالح. يجب أن يبدأ بـ t.me/nft/</b>",
                        parse_mode='HTML',
                        reply_markup=markup)
        return
    
    request_id = save_request(
        f"gift_{gift_type}",
        message.chat.id,
        {"link": gift_link, "type": gift_type},
        points_needed
    )
    
    if gift_type == "forced":
        settings = read_json(SETTINGS_FILE)
        auction_admin = settings.get("auction_admin", AUCTION_ADMIN)
        
        transfer_msg = f"""<b>حسناً ⚡</b>

<blockquote>قم الآن بتحويل الهدية إلى المشرف الآتي:
{auction_admin}</blockquote>

<blockquote>ثم اضغط على زر 'لقد أرسلت'</blockquote>"""
        
        markup = types.InlineKeyboardMarkup()
        btn_sent = types.InlineKeyboardButton("√ لقد أرسلت", callback_data=f"gift_sent_{request_id}")
        markup.add(btn_sent)
        
        bot.send_message(message.chat.id, transfer_msg, parse_mode='HTML', reply_markup=markup)
    else:
        
        send_gift_for_review(request_id, gift_link, gift_type, message.chat.id)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ القائمة الرئيسية", callback_data="main_menu"))
        
        bot.send_message(message.chat.id,
                        "<b>√ تم إرسال طلبك للمراجعة!</b>",
                        parse_mode='HTML',
                        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('gift_sent_'))
def gift_sent_confirmation(call):
    request_id = call.data.replace('gift_sent_', '')
    requests_db = read_json(PENDING_REQUESTS_FILE)
    
    if "requests" not in requests_db:
        requests_db["requests"] = {}
    
    if request_id not in requests_db["requests"]:
        bot.answer_callback_query(call.id, "<b>✗ الطلب غير موجود</b>", show_alert=True)
        return
    
    request_data = requests_db["requests"][request_id]
    gift_link = request_data["data"]["link"]
    user_id = call.from_user.id
    
    send_gift_for_review(request_id, gift_link, "forced", user_id)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>√ تم إرسال طلبك للمراجعة! سيتم إعلامك بالقرار.</b>",
        parse_mode='HTML'
    )

def send_gift_for_review(request_id, gift_link, gift_type, user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_approve = types.InlineKeyboardButton("√ موافقة", callback_data=f"approve_{request_id}")
    btn_reject = types.InlineKeyboardButton("✗ رفض", callback_data=f"reject_{request_id}")
    markup.add(btn_approve, btn_reject)
    
    user_data = get_user_data(user_id)
    
    if gift_type == "forced":
        type_text = "إجباري ⚡ (15 دقيقة)"
        points_text = "5 نقاط"
    else:
        type_text = "عادي 🎁"
        points_text = "2 نقطة"
    
    request_text = f"""<b>📋 طلب نشر هدية جديد</b>

<blockquote><b>• المستخدم:</b> {user_id}
<b>• النقاط الحالية:</b> {user_data['points']}
<b>• النوع:</b> {type_text}
<b>• التكلفة:</b> {points_text}
<b>• الرابط:</b> {gift_link}
<b>• طلب ID:</b> {request_id}</blockquote>"""
    
    settings = read_json(SETTINGS_FILE)
    admin_group = settings.get("admin_group", ADMIN_GROUP_ID)
    
    bot.send_message(admin_group, request_text, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'publish_username_menu')
def publish_username_menu(call):
    user = get_user_data(call.from_user.id)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('📜 نشر معرف (5 نقاط)', callback_data='publish_username_normal')
    btn2 = types.InlineKeyboardButton('⤺ رجوع', callback_data='main_menu')
    markup.add(btn1, btn2)
    
    text = f"""<b>📜 نشر معرف جديد</b>

<blockquote>💎 نقاطك الحالية: {user['points']}</blockquote>

<blockquote><b>• النشر:</b> 5 نقاط</blockquote>"""
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'publish_username_normal')
def publish_username_normal(call):
    user = get_user_data(call.from_user.id)
    
    if user["points"] < 5:
        bot.answer_callback_query(call.id, "<b>✗ نقاطك غير كافية. تحتاج إلى 5 نقاط على الأقل</b>", show_alert=True)
        return
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    msg = bot.send_message(call.message.chat.id,
                          """<b>📜 نشر معرف جديد 📜</b>

<blockquote>• أرسل المعرف الذي تود نشره.
• يجب أن يبدأ بـ @ مثال: <code>@h3ry3</code></blockquote>""",
                          parse_mode='HTML')
    bot.register_next_step_handler(msg, process_username, "normal", 5)

def process_username(message, publish_type, points_needed):
    if message.text is None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ المحاولة مرة أخرى", callback_data="publish_username_menu"))
        bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال المعرف</b>", parse_mode='HTML', reply_markup=markup)
        return
    
    username = message.text.strip()
    
    if not username.startswith("@"):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ المحاولة مرة أخرى", callback_data="publish_username_menu"))
        bot.send_message(message.chat.id, 
                        "<b>✗ المعرف غير صالح. يجب أن يبدأ بـ @</b>",
                        parse_mode='HTML',
                        reply_markup=markup)
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('ملكية', callback_data=f'username_type_ownership_{publish_type}_{points_needed}_{username.replace("@", "")}')
    btn2 = types.InlineKeyboardButton('منصة (NFT)', callback_data=f'username_type_nft_{publish_type}_{points_needed}_{username.replace("@", "")}')
    markup.add(btn1, btn2)
    
    msg = bot.send_message(message.chat.id,
                          "<b>حسناً الان اختر نوع المعرف:</b>",
                          parse_mode='HTML',
                          reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('username_type_'))
def handle_username_type_selection(call):
    data_parts = call.data.split('_')
    username_type = data_parts[2]
    
    publish_type = data_parts[3]   
    points_needed = int(data_parts[4])
    username = data_parts[5]
    
    user_id = call.from_user.id
    
    request_id = save_request(
        f"username_{publish_type}",
        user_id,
        {"username": username, "type": username_type},
        points_needed
    )
    
    send_username_for_review(request_id, username, username_type, user_id)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>√ تم إرسال طلبك للمراجعة!</b>",
        parse_mode='HTML'
    )

def send_username_for_review(request_id, username, username_type, user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_approve = types.InlineKeyboardButton("√ موافقة", callback_data=f"approve_{request_id}")
    btn_reject = types.InlineKeyboardButton("✗ رفض", callback_data=f"reject_{request_id}")
    markup.add(btn_approve, btn_reject)
    
    user_data = get_user_data(user_id)
    
    type_text = "منصة (NFT)" if username_type == "nft" else "ملكية"
    
    request_text = f"""<b>📜 طلب نشر معرف جديد</b>

<blockquote><b>• المستخدم:</b> {user_id}
<b>• النقاط الحالية:</b> {user_data['points']}
<b>• التكلفة:</b> 5 نقاط
<b>• النوع:</b> {type_text}
<b>• المعرف:</b> @{username}
<b>• طلب ID:</b> {request_id}</blockquote>"""
    
    settings = read_json(SETTINGS_FILE)
    admin_group = settings.get("admin_group", ADMIN_GROUP_ID)
    
    bot.send_message(admin_group, request_text, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('approve_', 'reject_')))
def handle_approval(call):
    if call.data.startswith('approve_'):
        request_id = call.data.replace('approve_', '')
        action = 'approve'
    else:
        request_id = call.data.replace('reject_', '')
        action = 'reject'
    
    request_info = get_request_data(request_id)
    
    if not request_info:
        bot.answer_callback_query(call.id, "<b>✗ الطلب غير موجود</b>", show_alert=True)
        return
    
    user_id = int(request_info["user_id"])
    
    if action == 'approve':
        points_needed = request_info.get("points_required", 0)
        user_data = get_user_data(user_id)
        
        if user_data["points"] >= points_needed:
            subtract_user_points(user_id, points_needed)
        else:
            bot.answer_callback_query(call.id, "<b>✗ نقاط المستخدم غير كافية</b>", show_alert=True)
            return
        
        if "gift" in request_info["type"]:
            gift_type = request_info["data"].get("type", "normal")
            gift_link = request_info["data"].get("link", "")
            
            if gift_link:
                message_id = publish_gift_to_channel(gift_link, gift_type)
                if message_id and message_id != "cooldown":
                    bot.send_message(user_id, 
                                    f"""<b>√ تم نشر هديتك بنجاح!</b>

<blockquote><b>🔗 رابط هديتك:</b> https://t.me/c/{str(CHANNEL_ID).replace('-100', '')}/{message_id}</blockquote>""",
                                    parse_mode='HTML')
                elif message_id == "cooldown":
                    bot.send_message(user_id, "<b>⏳ سيتم نشر هديتك بعد 5 دقائق من آخر نشر</b>", parse_mode='HTML')
                    
                    request_info["status"] = "waiting"
                    update_request_status(request_id, "waiting")
                    
                    try:
                        new_text = f"""<b>📋 طلب نشر هدية جديد - في الانتظار</b>

<blockquote><b>• المستخدم:</b> {user_id}
<b>• النقاط الحالية:</b> {user_data['points']}
<b>• النوع:</b> {gift_type}
<b>• التكلفة:</b> {points_needed} نقاط
<b>• الرابط:</b> {gift_link}
<b>• طلب ID:</b> {request_id}</blockquote>

<blockquote><i>⏳ في انتظار الدور للنشر (فاصل 5 دقائق)</i></blockquote>"""
                        
                        bot.edit_message_text(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text=new_text,
                            parse_mode='HTML'
                        )
                    except:
                        pass
                    return
                else:
                    bot.send_message(user_id, "<b>✗ حدث خطأ في نشر الهدية. تم استرجاع نقاطك.</b>", parse_mode='HTML')
                    add_user_points(user_id, points_needed)
        
        elif "username" in request_info["type"]:
            username = request_info["data"].get("username", "")
            username_type = request_info["data"].get("type", "ownership")
            
            if username:
                message_id = publish_username_to_channel(username, username_type)
                if message_id and message_id != "cooldown":
                    bot.send_message(user_id, 
                                    f"""<b>√ تم نشر معرفك بنجاح!</b>

<blockquote><b>🔗 رابط معرفك:</b> https://t.me/c/{str(CHANNEL_ID).replace('-100', '')}/{message_id}</blockquote>""",
                                    parse_mode='HTML')
                elif message_id == "cooldown":
                    bot.send_message(user_id, "<b>⏳ سيتم نشر معرفك بعد 5 دقائق من آخر نشر</b>", parse_mode='HTML')
                    
                    request_info["status"] = "waiting"
                    update_request_status(request_id, "waiting")
                    
                    try:
                        type_text = "منصة (NFT)" if username_type == "nft" else "ملكية"
                        new_text = f"""<b>📜 طلب نشر معرف جديد - في الانتظار</b>

<blockquote><b>• المستخدم:</b> {user_id}
<b>• النقاط الحالية:</b> {user_data['points']}
<b>• التكلفة:</b> {points_needed} نقاط
<b>• النوع:</b> {type_text}
<b>• المعرف:</b> @{username}
<b>• طلب ID:</b> {request_id}</blockquote>

<blockquote><i>⏳ في انتظار الدور للنشر (فاصل 5 دقائق)</i></blockquote>"""
                        
                        bot.edit_message_text(
                            chat_id=call.message.chat.id,
                            message_id=call.message.message_id,
                            text=new_text,
                            parse_mode='HTML'
                        )
                    except:
                        pass
                    return
                else:
                    bot.send_message(user_id, "<b>✗ حدث خطأ في نشر المعرف. تم استرجاع نقاطك.</b>", parse_mode='HTML')
                    add_user_points(user_id, points_needed)
        
        update_request_status(request_id, "approved")
        bot.answer_callback_query(call.id, "<b>√ تمت الموافقة</b>", show_alert=True)
        
        
        try:
            if "gift" in request_info["type"]:
                gift_type = request_info["data"].get("type", "normal")
                gift_link = request_info["data"].get("link", "")
                type_text = "إجباري ⚡" if gift_type == "forced" else "عادي 🎁"
                
                new_text = f"""<b>📋 طلب نشر هدية جديد - تمت الموافقة</b>

<blockquote><b>• المستخدم:</b> {user_id}
<b>• النقاط الحالية:</b> {user_data['points']}
<b>• النوع:</b> {type_text}
<b>• التكلفة:</b> {points_needed} نقاط
<b>• الرابط:</b> {gift_link}
<b>• طلب ID:</b> {request_id}</blockquote>

<blockquote><i>√ تمت الموافقة من قبل: {call.from_user.first_name}</i></blockquote>"""
                
            elif "username" in request_info["type"]:
                username = request_info["data"].get("username", "")
                username_type = request_info["data"].get("type", "ownership")
                type_text = "منصة (NFT)" if username_type == "nft" else "ملكية"
                
                new_text = f"""<b>📜 طلب نشر معرف جديد - تمت الموافقة</b>

<blockquote><b>• المستخدم:</b> {user_id}
<b>• النقاط الحالية:</b> {user_data['points']}
<b>• التكلفة:</b> {points_needed} نقاط
<b>• النوع:</b> {type_text}
<b>• المعرف:</b> @{username}
<b>• طلب ID:</b> {request_id}</blockquote>

<blockquote><i>√ تمت الموافقة من قبل: {call.from_user.first_name}</i></blockquote>"""
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode='HTML'
            )
        except:
            pass
        
    else:
        bot.send_message(user_id, "<b>✗ تم رفض طلبك</b>", parse_mode='HTML')
        update_request_status(request_id, "rejected")
        bot.answer_callback_query(call.id, "<b>✗ تم الرفض</b>", show_alert=True)
        
        
        try:
            if "gift" in request_info["type"]:
                gift_type = request_info["data"].get("type", "normal")
                gift_link = request_info["data"].get("link", "")
                type_text = "إجباري ⚡" if gift_type == "forced" else "عادي 🎁"
                
                new_text = f"""<b>📋 طلب نشر هدية جديد - تم الرفض</b>

<blockquote><b>• المستخدم:</b> {user_id}
<b>• النقاط الحالية:</b> {user_data['points']}
<b>• النوع:</b> {type_text}
<b>• التكلفة:</b> {points_needed} نقاط
<b>• الرابط:</b> {gift_link}
<b>• طلب ID:</b> {request_id}</blockquote>

<blockquote><i>✗ تم الرفض من قبل: {call.from_user.first_name}</i></blockquote>"""
                
            elif "username" in request_info["type"]:
                username = request_info["data"].get("username", "")
                username_type = request_info["data"].get("type", "ownership")
                type_text = "منصة (NFT)" if username_type == "nft" else "ملكية"
                
                new_text = f"""<b>📜 طلب نشر معرف جديد - تم الرفض</b>

<blockquote><b>• المستخدم:</b> {user_id}
<b>• النقاط الحالية:</b> {user_data['points']}
<b>• التكلفة:</b> {points_needed} نقاط
<b>• النوع:</b> {type_text}
<b>• المعرف:</b> @{username}
<b>• طلب ID:</b> {request_id}</blockquote>

<blockquote><i>✗ تم الرفض من قبل: {call.from_user.first_name}</i></blockquote>"""
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode='HTML'
            )
        except:
            pass

def check_and_publish_waiting():
    while True:
        try:
            requests_db = read_json(PENDING_REQUESTS_FILE)
            waiting_requests = [req for req in requests_db.get("requests", {}).values() if req.get("status") == "waiting"]
            
            for request in waiting_requests:
                if can_publish():
                    user_id = int(request["user_id"])
                    
                    if "gift" in request["type"]:
                        gift_link = request["data"].get("link", "")
                        gift_type = request["data"].get("type", "normal")
                        
                        if gift_link:
                            message_id = publish_gift_to_channel(gift_link, gift_type)
                            if message_id:
                                bot.send_message(user_id, 
                                                f"""<b>√ تم نشر هديتك بعد الانتظار!</b>

<blockquote><b>🔗 رابط هديتك:</b> https://t.me/c/{str(CHANNEL_ID).replace('-100', '')}/{message_id}</blockquote>""",
                                                parse_mode='HTML')
                                update_request_status(request["id"], "approved")
                    
                    elif "username" in request["type"]:
                        username = request["data"].get("username", "")
                        username_type = request["data"].get("type", "ownership")
                        
                        if username:
                            message_id = publish_username_to_channel(username, username_type)
                            if message_id:
                                bot.send_message(user_id, 
                                                f"""<b>√ تم نشر معرفك بعد الانتظار!</b>

<blockquote><b>🔗 رابط معرفك:</b> https://t.me/c/{str(CHANNEL_ID).replace('-100', '')}/{message_id}</blockquote>""",
                                                parse_mode='HTML')
                                update_request_status(request["id"], "approved")
        
        except Exception as e:
            print(f"خطأ في فحص الطلبات المنتظرة: {e}")
        
        time.sleep(60)  

@bot.callback_query_handler(func=lambda call: call.data == 'charge_asia')
def charge_with_asia(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    instructions = """<b>📱 تحويل آسيا سيل التلقائي</b>

<blockquote><b>لشحن الرصيد عبر آسيا سيل:</b>
1. قم بأرسال رقم هاتفك بالشكل التالي:
077xxxxxxxx</blockquote>

<blockquote><i>ملاحظة: يجب أن يكون لديك حساب نشط في آسيا سيل</i></blockquote>"""
    
    msg = bot.send_message(call.message.chat.id, instructions, parse_mode='HTML')
    bot.register_next_step_handler(msg, start_asia_cell_transfer)

def start_asia_cell_transfer(message):
    try:
        if message.text is None:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ رجوع", callback_data="charge_menu"))
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال رقم الهاتف</b>", parse_mode='HTML', reply_markup=markup)
            return
            
        phone = message.text.strip()
        if not re.match(r'^07[0-9]{9}$', phone):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ رجوع", callback_data="charge_menu"))
            bot.send_message(message.chat.id, "<b>✗ رقم الهاتف غير صحيح. يجب أن يبدأ بـ 07 ويتكون من 11 رقماً</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        update_user_data(message.chat.id, phone=phone)
        
        dev = ''.join(random.choice("qazxcndoeprohfncowuntgoyhebkfoch") for i in range(9))
        deviceid = f'b6ae347764eabef98b17439{dev}'
        
        url = 'https://www.asiacell.com/api/v1/captcha?lang=en'
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://www.asiacell.com',
            'Referer': 'https://www.asiacell.com/en/personal/my-account/login?afterLogin=%252Fen%252Fpersonal%252Fmy-account',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
            'deviceid': deviceid,
        }
        
        session = requests.Session()
        session.verify = False
        
        response = session.post(url, headers=headers, json={}, timeout=30)
        
        if response.status_code != 200:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ فشل في الاتصال بخدمة آسيا سيل. حاول مرة أخرى</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        image_url = f"https://www.asiacell.com" + response.json()["captcha"]["resourceUrl"]
        
        photo_msg = bot.send_photo(message.chat.id, image_url, 
                            caption="<b>🔢 ارسل الكود الموجود في الصورة:</b>", 
                            parse_mode='HTML')
        
        msg = bot.send_message(message.chat.id, "<b>اكتب الكود هنا:</b>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_asia_captcha, phone, deviceid, session, photo_msg.message_id)
            
    except Exception as e:
        print(f"خطأ في start_asia_cell_transfer: {e}")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
        bot.send_message(message.chat.id, f"<b>✗ خطأ: {str(e)}</b>", 
                       parse_mode='HTML', reply_markup=markup)

def process_asia_captcha(message, phone, deviceid, session, photo_msg_id):
    try:
        try:
            bot.delete_message(message.chat.id, photo_msg_id)
        except:
            pass
        
        if message.text is None:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال الكود</b>", parse_mode='HTML', reply_markup=markup)
            return
            
        captcha_code = message.text.strip()
        
        url = 'https://www.asiacell.com/api/v1/login?lang=en'
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://www.asiacell.com',
            'Referer': 'https://www.asiacell.com/en/personal/my-account/login?afterLogin=%252Fen%252Fpersonal%252Fmy-account',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
            'deviceid': deviceid,
        }
        
        payload = {
            'username': phone,
            'captchaCode': captcha_code,
        }
        
        response = session.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ فشل تسجيل الدخول. تأكد من رقم الهاتف</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        data = response.json()
        next_url = data.get("nextUrl", "")
        
        if not next_url:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ فشل تسجيل الدخول. حاول مرة أخرى</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        pid_match = re.search(r'PID=([\w-]+)', next_url)
        if not pid_match:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ خطأ في استجابة الخادم</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        pid = pid_match.group(1)
        
        msg = bot.send_message(message.chat.id, "<b>📲 ارسل كود التحقق المرسل لهاتفك:</b>", parse_mode='HTML')
        bot.register_next_step_handler(msg, process_asia_sms, pid, deviceid, session, phone)
        
    except Exception as e:
        print(f"خطأ في process_asia_captcha: {e}")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
        bot.send_message(message.chat.id, f"<b>✗ خطأ: {str(e)}</b>", 
                       parse_mode='HTML', reply_markup=markup)

def process_asia_sms(message, pid, deviceid, session, phone):
    try:
        if message.text is None:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال كود التحقق</b>", parse_mode='HTML', reply_markup=markup)
            return
            
        sms_code = message.text.strip()
        
        url = "https://www.asiacell.com/api/v1/smsvalidation?lang=en"
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Origin': 'https://www.asiacell.com',
            'Referer': 'https://www.asiacell.com/en/personal/my-account/login?afterLogin=%252Fen%252Fpersonal%252Fmy-account',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
            'deviceid': deviceid,
        }
        
        payload = {
            "PID": pid,
            "passcode": sms_code
        }
        
        response = session.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ كود التحقق غير صحيح</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        if "access_token" not in response.json():
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ فشل الحصول على صلاحية الدخول</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        tokenacc = response.json()["access_token"]
        
        msg = bot.send_message(message.chat.id, 
                              """<b>💰 أرسل المبلغ المراد تحويله (بالدينار):</b>

<blockquote><b>مثال:</b> لتحويل 1000 دينار أرسل 1000</blockquote>

<blockquote><b>الحد الأدنى:</b> 1000 دينار
<b>الحد الأقصى:</b> 60000 دينار</blockquote>""", 
                              parse_mode='HTML')
        
        bot.register_next_step_handler(msg, process_asia_amount, tokenacc, deviceid, phone)
        
    except Exception as e:
        print(f"خطأ في process_asia_sms: {e}")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
        bot.send_message(message.chat.id, f"<b>✗ خطأ: {str(e)}</b>", 
                       parse_mode='HTML', reply_markup=markup)

def process_asia_amount(message, tokenacc, deviceid, phone):
    try:
        if message.text is None:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال المبلغ</b>", parse_mode='HTML', reply_markup=markup)
            return
            
        try:
            amount = int(message.text.strip())
        except ValueError:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ الرجاء إدخال رقم صحيح</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        if amount < 1000 or amount > 60000:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ المبلغ يجب أن يكون بين 1000 و 60000 دينار</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        payment_settings = read_json(PAYMENT_SETTINGS_FILE)
        points_per_1000 = payment_settings.get("asia_points_per_1000", 1.0)
        points_to_add = int((amount / 1000) * points_per_1000)
        
        settings = read_json(SETTINGS_FILE)
        asia_receiver = settings.get("asia_number", ASIA_CELL_RECEIVER)
        
        url = "https://www.asiacell.com/api/v1/credit-transfer/start?lang=en"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {tokenacc}",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "DeviceID": deviceid,
            "Origin": "https://www.asiacell.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        }
        
        payload = {
            "receiverMsisdn": asia_receiver,
            "amount": amount
        }
        
        session = requests.Session()
        session.verify = False
        
        response = session.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ فشل بدء عملية التحويل</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        if "PID" not in response.json():
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
            bot.send_message(message.chat.id, "<b>✗ خطأ في استجابة التحويل</b>", 
                           parse_mode='HTML', reply_markup=markup)
            return
        
        transfer_pid = response.json()["PID"]
        
        msg = bot.send_message(message.chat.id, 
                              f"""<b>📲 أرسل كود التأكيد المرسل لهاتفك لتحويل الرصيد:</b>

<blockquote><b>المبلغ:</b> {amount} دينار
<b>النقاط المستحقة:</b> {points_to_add} نقطة</blockquote>""", 
                              parse_mode='HTML')
        
        bot.register_next_step_handler(msg, complete_asia_transfer, transfer_pid, tokenacc, deviceid, amount, points_to_add, phone)
        
    except Exception as e:
        print(f"خطأ في process_asia_amount: {e}")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⤺ البداية", callback_data="start"))
        bot.send_message(message.chat.id, f"<b>✗ خطأ: {str(e)}</b>", 
                       parse_mode='HTML', reply_markup=markup)

def complete_asia_transfer(message, transfer_pid, tokenacc, deviceid, amount, points_to_add, phone):
    try:
        if message.text is None:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🏠 البداية", callback_data="home"))
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال كود التأكيد</b>", parse_mode='HTML', reply_markup=markup)
            return
            
        confirm_code = message.text.strip()
        
        url = "https://www.asiacell.com/api/v1/credit-transfer/do-transfer?lang=en"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": f"Bearer {tokenacc}",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "DeviceID": deviceid,
            "Origin": "https://www.asiacell.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        }
        
        payload = {
            "PID": transfer_pid,
            "passcode": confirm_code
        }
        
        session = requests.Session()
        session.verify = False
        
        response = session.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        response_text = response.text
        
        is_successful = False
        failure_message = ""
        
        try:
            response_json = json.loads(response_text)
            
            if response.status_code == 200:
                if response_json.get("status") == "success" or response_json.get("success") == True:
                    is_successful = True
                elif "transactionId" in response_json or "reference" in response_json:
                    is_successful = True
                elif response_json.get("message") and any(word in response_json["message"].lower() for word in ["success", "completed", "تمت", "نجح"]):
                    is_successful = True
                elif response_json.get("message") and any(word in response_json["message"].lower() for word in ["fail", "error", "insufficient", "not enough", "فشل", "خطأ", "غير كافي"]):
                    is_successful = False
                    failure_message = response_json.get("message", "فشل غير محدد")
                else:
                    is_successful = False
                    failure_message = "لا توجد مؤشرات نجاح واضحة في الاستجابة"
        
        except json.JSONDecodeError:
            if response.status_code == 200:
                lower_response = response_text.lower()
                failure_keywords = ["fail", "error", "insufficient", "not enough", "sorry", "فشل", "خطأ"]
                success_keywords = ["success", "completed", "transfer successful", "تمت بنجاح"]
                
                if any(keyword in lower_response for keyword in failure_keywords):
                    is_successful = False
                elif any(keyword in lower_response for keyword in success_keywords):
                    is_successful = True
                else:
                    is_successful = False
                    failure_message = "استجابة غير واضحة"
            else:
                is_successful = False
                failure_message = f"خطأ في الخادم: {response.status_code}"
        
        if is_successful:
            new_balance = add_user_points(message.chat.id, points_to_add)
            
            success_msg = f"""<b>√ تم التحويل وإضافة النقاط بنجاح!</b>

<blockquote><b>📊 تفاصيل العملية:</b>
• المبلغ المحول: {amount} دينار
• النقاط المضافة: {points_to_add} نقطة
• رصيدك الجديد: {new_balance} نقطة
• الوقت: {datetime.datetime.now().strftime("%H:%M:%S")}</blockquote>"""
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🏠 البداية", callback_data="home"))
            bot.send_message(message.chat.id, success_msg, 
                           parse_mode='HTML', reply_markup=markup)
            
            settings = read_json(SETTINGS_FILE)
            admin_group = settings.get("admin_group", ADMIN_GROUP_ID)
            
            admin_msg = f"""<b>🔔 إشعار تحويل آسيا سيل ناجح</b>

<blockquote>👤 المستخدم: {message.chat.id}
📞 الرقم: {phone}
💰 المبلغ: {amount} دينار
💎 النقاط: {points_to_add}
📊 الرصيد الجديد: {new_balance}
⏰ الوقت: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</blockquote>"""
            
            bot.send_message(admin_group, admin_msg, parse_mode='HTML')
            
        else:
            error_msg = f"""<b>✗ فشلت عملية التحويل</b>

<blockquote><b>📊 تفاصيل العملية:</b>
• المبلغ: {amount} دينار
• السبب: رصيدك لا يكفي للتحويل أو خطك معلق راجع رسائل الخط</blockquote>

<blockquote><i>ملاحظة: لم يتم خصم أي مبلغ من رصيدك ولم تتم إضافة نقاط</i></blockquote>"""
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⤺ المحاولة مجدداً", callback_data="retry"))
            bot.send_message(message.chat.id, error_msg, 
                           parse_mode='HTML', reply_markup=markup)
            
            admin_msg = f"""<b>⚠️ إشعار تحويل آسيا سيل فاشل</b>

<blockquote>👤 المستخدم: {message.chat.id}
📞 الرقم: {phone}
💰 المبلغ: {amount} دينار
✗ السبب: {failure_message or 'فشل غير محدد'}
⏰ الوقت: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</blockquote>"""
            
            bot.send_message(ADMIN_GROUP_ID, admin_msg, parse_mode='HTML')
        
    except Exception as e:
        print(f"خطأ في complete_asia_transfer: {e}")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🏠 البداية", callback_data="home"))
        bot.send_message(message.chat.id, f"<b>✗ خطأ نهائي: {str(e)}</b>", 
                       parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["menu", "start", "home", "retry"])
def handle_menu_buttons(call):
    if call.data == "menu" or call.data == "home" or call.data == "start":
        start_command(call.message)
    elif call.data == "retry":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        instructions = """<b>📱 تحويل آسيا سيل التلقائي</b>

<blockquote><b>لشحن الرصيد عبر آسيا سيل:</b>
1. قم بأرسال رقم هاتفك بالشكل التالي:
077xxxxxxxx</blockquote>

<blockquote><i>ملاحظة: يجب أن يكون لديك حساب نشط في آسيا سيل</i></blockquote>"""
        
        msg = bot.send_message(call.message.chat.id, instructions, parse_mode='HTML')
        bot.register_next_step_handler(msg, start_asia_cell_transfer)

@bot.message_handler(commands=['admin'])
def admin_command(message):
    if message.chat.id not in ID_AD:
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('🎟️ إنشاء كود', callback_data='admin_generate')
    btn2 = types.InlineKeyboardButton('📊 الإحصائيات', callback_data='admin_stats')
    btn3 = types.InlineKeyboardButton('👥 المستخدمين', callback_data='admin_users')
    btn4 = types.InlineKeyboardButton('➕ إضافة نقاط', callback_data='admin_add_points')
    btn5 = types.InlineKeyboardButton('➖ خصم نقاط', callback_data='admin_subtract_points')
    btn6 = types.InlineKeyboardButton('⚙️ الإعدادات', callback_data='admin_settings')
    btn7 = types.InlineKeyboardButton('📋 الطلبات', callback_data='admin_requests')
    btn8 = types.InlineKeyboardButton('💰 أسعار الدفع', callback_data='admin_payment_rates')
    btn9 = types.InlineKeyboardButton('🔧 طرق الدفع', callback_data='admin_payment_methods')
    btn10 = types.InlineKeyboardButton('📢 قنوات الاشتراك', callback_data='admin_subscription')
    btn11 = types.InlineKeyboardButton('ℹ️ آلية الموافقة/الرفض', callback_data='admin_approval_info')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
    
    bot.send_message(message.chat.id, "<b>👑 لوحة تحكم المسؤول</b>", parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'admin_approval_info')
def admin_approval_info(call):
    info_text = """<b>ℹ️ آلية الموافقة والرفض في البوت</b>

<blockquote><b>• الهدايا الإجبارية:</b>
يجب على المستخدم تحويل الهداية إلى المسؤول أولاً
ثم يتم الموافقة/الرفض من الكروب

<b>• الهدايا العادية:</b>
يتم إرسال الطلب مباشرة إلى الكروب
يتم الموافقة/الرفض من الكروب

<b>• المعرفات (يوزرنيمات):</b>
يتم إرسال الطلب مباشرة إلى الكروب
يتم الموافقة/الرفض من الكروب

<b>• طلبات الشحن:</b>
(نجوم، ماستر كارد، زين كاش)
يتم مراجعتها من الكروب</blockquote>

<blockquote><b>📢 ملاحظة:</b>
جميع الطلبات تُرسل مباشرة إلى كروب المراجعة
لا يوجد تأكيد من المستخدم بعد الإرسال</blockquote>"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⤺ رجوع", callback_data="admin_back"))
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=info_text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'admin_generate')
def admin_generate(call):
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn5 = types.InlineKeyboardButton('5 نقاط', callback_data='gen_5')
    btn10 = types.InlineKeyboardButton('10 نقاط', callback_data='gen_10')
    btn20 = types.InlineKeyboardButton('20 نقاط', callback_data='gen_20')
    btn30 = types.InlineKeyboardButton('30 نقاط', callback_data='gen_30')
    btn50 = types.InlineKeyboardButton('50 نقاط', callback_data='gen_50')
    btn100 = types.InlineKeyboardButton('100 نقطة', callback_data='gen_100')
    btn_custom = types.InlineKeyboardButton('قيمة مخصصة', callback_data='gen_custom')
    btn_back = types.InlineKeyboardButton('⤺ رجوع', callback_data='admin_back')
    markup.add(btn5, btn10, btn20, btn30, btn50, btn100, btn_custom, btn_back)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>🎟️ اختر قيمة الكود:</b>",
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('gen_'))
def generate_specific_code(call):
    if call.data == 'gen_custom':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, "<b>🎟️ أدخل قيمة الكود (عدد النقاط):</b>", parse_mode='HTML')
        bot.register_next_step_handler(msg, generate_custom_code)
        return
    
    amount = int(call.data.replace('gen_', ''))
    code = generate_code(amount)
    
    bot.send_message(call.message.chat.id,
                    f"""<b>🎟️ تم إنشاء كود شحن جديد</b>

<blockquote><b>• الكود:</b> {code}
<b>• القيمة:</b> {amount} نقطة</blockquote>""",
                    parse_mode='HTML')

def generate_custom_code(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال القيمة</b>", parse_mode='HTML')
            return
            
        amount = int(message.text.strip())
        if amount <= 0:
            bot.send_message(message.chat.id, "<b>✗ القيمة يجب أن تكون أكبر من صفر</b>", parse_mode='HTML')
            return
        
        code = generate_code(amount)
        
        bot.send_message(message.chat.id,
                        f"""<b>🎟️ تم إنشاء كود شحن جديد</b>

<blockquote><b>• الكود:</b> {code}
<b>• القيمة:</b> {amount} نقطة</blockquote>""",
                        parse_mode='HTML')
    except ValueError:
        bot.send_message(message.chat.id, "<b>✗ الرجاء إدخال رقم صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'admin_stats')
def admin_stats(call):
    users = read_json(USERS_FILE)
    requests_db = read_json(PENDING_REQUESTS_FILE)
    codes = read_json(CODES_FILE)
    
    if "requests" not in requests_db:
        requests_db["requests"] = {}
    
    total_users = len(users)
    total_points = sum(user.get("points", 0) for user in users.values())
    pending_requests = sum(1 for req in requests_db["requests"].values() if req.get("status") == "pending")
    used_codes = sum(1 for code in codes.values() if code.get("used", False))
    total_codes = len(codes)
    
    
    referrals = read_json(REFERRAL_FILE)
    total_referrals = len(referrals)
    
    stats_text = f"""<b>📊 إحصائيات البوت</b>

<blockquote><b>👥 إجمالي المستخدمين:</b> {total_users}
<b>💎 إجمالي النقاط:</b> {total_points}
<b>📋 الطلبات المعلقة:</b> {pending_requests}
<b>🎟️ الأكواد المستخدمة:</b> {used_codes}/{total_codes}
<b>👥 إجمالي الدعوات:</b> {total_referrals}
<b>⏰ آخر تحديث:</b> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</blockquote>"""
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=stats_text,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data == 'admin_users')
def admin_users(call):
    users = read_json(USERS_FILE)
    
    if not users:
        bot.answer_callback_query(call.id, "لا يوجد مستخدمين بعد", show_alert=True)
        return
    
    users_list = []
    for user_id, user_data in list(users.items())[:10]:
        users_list.append(f"👤 {user_id}: {user_data.get('points', 0)} نقطة (دعوات: {user_data.get('referrals', 0)})")
    
    users_text = "<b>👥 قائمة المستخدمين (أول 10):</b>\n\n" + "\n".join(users_list)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⤺ رجوع", callback_data="admin_back"))
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=users_text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'admin_add_points')
def admin_add_points(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>👤 أرسل آيدي المستخدم:</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, admin_add_points_step2)

def admin_add_points_step2(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال آيدي</b>", parse_mode='HTML')
            return
            
        user_id = int(message.text.strip())
        msg = bot.send_message(message.chat.id, "<b>💎 أرسل عدد النقاط:</b>", parse_mode='HTML')
        bot.register_next_step_handler(msg, admin_add_points_step3, user_id)
    except:
        bot.send_message(message.chat.id, "<b>✗ آيدي غير صحيح</b>", parse_mode='HTML')

def admin_add_points_step3(message, user_id):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال عدد النقاط</b>", parse_mode='HTML')
            return
            
        points = int(message.text.strip())
        new_balance = add_user_points(user_id, points)
        bot.send_message(message.chat.id, f"<b>√ تمت إضافة {points} نقطة للمستخدم {user_id}</b>\n<blockquote>رصيده الجديد: {new_balance}</blockquote>", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "<b>✗ عدد النقاط غير صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'admin_subtract_points')
def admin_subtract_points(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>👤 أرسل آيدي المستخدم:</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, admin_subtract_points_step2)

def admin_subtract_points_step2(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال آيدي</b>", parse_mode='HTML')
            return
            
        user_id = int(message.text.strip())
        msg = bot.send_message(message.chat.id, "<b>💎 أرسل عدد النقاط لخصمها:</b>", parse_mode='HTML')
        bot.register_next_step_handler(msg, admin_subtract_points_step3, user_id)
    except:
        bot.send_message(message.chat.id, "<b>✗ آيدي غير صحيح</b>", parse_mode='HTML')

def admin_subtract_points_step3(message, user_id):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال عدد النقاط</b>", parse_mode='HTML')
            return
            
        points = int(message.text.strip())
        if subtract_user_points(user_id, points):
            user_data = get_user_data(user_id)
            bot.send_message(message.chat.id, f"<b>√ تم خصم {points} نقطة من المستخدم {user_id}</b>\n<blockquote>رصيده الجديد: {user_data.get('points', 0)}</blockquote>", parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, f"<b>✗ نقاط المستخدم غير كافية</b>", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "<b>✗ عدد النقاط غير صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'admin_settings')
def admin_settings(call):
    settings = read_json(SETTINGS_FILE)
    
    settings_text = f"""<b>⚙️ إعدادات البوت</b>

<blockquote><b>📢 قناة المزاد:</b> {settings.get('channel_id', CHANNEL_ID)}
<b>👥 مجموعة المراجعة:</b> {settings.get('admin_group', ADMIN_GROUP_ID)}
<b>👤 مسؤول المزاد:</b> {settings.get('auction_admin', AUCTION_ADMIN)}
<b>📱 رقم آسيا سيل:</b> {settings.get('asia_number', ASIA_CELL_RECEIVER)}
<b>🎯 نقاط الدعوة:</b> {settings.get('referral_points', 1)} نقطة</blockquote>"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('✏️ تعديل القناة', callback_data='edit_channel')
    btn2 = types.InlineKeyboardButton('✏️ تعديل المجموعة', callback_data='edit_group')
    btn3 = types.InlineKeyboardButton('✏️ تعديل المسؤول', callback_data='edit_admin')
    btn4 = types.InlineKeyboardButton('✏️ تعديل الرقم', callback_data='edit_number')
    btn5 = types.InlineKeyboardButton('✏️ نص ماستر كارد', callback_data='edit_master_text')
    btn6 = types.InlineKeyboardButton('✏️ نص زين كاش', callback_data='edit_zain_text')
    btn7 = types.InlineKeyboardButton('✏️ تعديل الشروط', callback_data='edit_terms')
    btn8 = types.InlineKeyboardButton('✏️ نقاط الدعوة', callback_data='edit_referral_points')
    btn9 = types.InlineKeyboardButton('⤺ رجوع', callback_data='admin_back')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=settings_text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'edit_channel')
def edit_channel(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>📢 أرسل آيدي قناة المزاد الجديد:</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_channel_id)

def save_channel_id(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال آيدي</b>", parse_mode='HTML')
            return
            
        new_id = int(message.text.strip())
        settings = read_json(SETTINGS_FILE)
        settings['channel_id'] = new_id
        write_json(SETTINGS_FILE, settings)
        bot.send_message(message.chat.id, f"<b>√ تم تحديث قناة المزاد إلى:</b> {new_id}", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "<b>✗ آيدي غير صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_group')
def edit_group(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>👥 أرسل آيدي مجموعة المراجعة الجديد:</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_group_id)

def save_group_id(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال آيدي</b>", parse_mode='HTML')
            return
            
        new_id = int(message.text.strip())
        settings = read_json(SETTINGS_FILE)
        settings['admin_group'] = new_id
        write_json(SETTINGS_FILE, settings)
        bot.send_message(message.chat.id, f"<b>√ تم تحديث مجموعة المراجعة إلى:</b> {new_id}", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "<b>✗ آيدي غير صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_admin')
def edit_admin(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>👤 أرسل يوزر مسؤول المزاد الجديد (مثال: @K01q1):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_admin)

def save_admin(message):
    if message.text is None:
        bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال النص</b>", parse_mode='HTML')
        return
        
    new_admin = message.text.strip()
    settings = read_json(SETTINGS_FILE)
    settings['auction_admin'] = new_admin
    write_json(SETTINGS_FILE, settings)
    bot.send_message(message.chat.id, f"<b>√ تم تحديث مسؤول المزاد إلى:</b> {new_admin}", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_number')
def edit_number(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>📱 أرسل رقم آسيا سيل الجديد (مثال: 07725257200):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_number)

def save_number(message):
    if message.text is None:
        bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال الرقم</b>", parse_mode='HTML')
        return
        
    new_number = message.text.strip()
    settings = read_json(SETTINGS_FILE)
    settings['asia_number'] = new_number
    write_json(SETTINGS_FILE, settings)
    bot.send_message(message.chat.id, f"<b>√ تم تحديث رقم آسيا سيل إلى:</b> {new_number}", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_master_text')
def edit_master_text(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>💳 أرسل نص ماستر كارد الجديد (استخدم \\n للسطر الجديد):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_master_text)

def save_master_text(message):
    if message.text is None:
        bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال النص</b>", parse_mode='HTML')
        return
        
    new_text = message.text.strip()
    settings = read_json(SETTINGS_FILE)
    settings['master_card_text'] = new_text.replace('\\n', '\n')
    write_json(SETTINGS_FILE, settings)
    bot.send_message(message.chat.id, f"<b>√ تم تحديث نص ماستر كارد</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_zain_text')
def edit_zain_text(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>📲 أرسل نص زين كاش الجديد (استخدم \\n للسطر الجديد):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_zain_text)

def save_zain_text(message):
    if message.text is None:
        bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال النص</b>", parse_mode='HTML')
        return
        
    new_text = message.text.strip()
    settings = read_json(SETTINGS_FILE)
    settings['zain_cash_text'] = new_text.replace('\\n', '\n')
    write_json(SETTINGS_FILE, settings)
    bot.send_message(message.chat.id, f"<b>√ تم تحديث نص زين كاش</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_terms')
def edit_terms(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>📜 أرسل نص الشروط الجديد (استخدم \\n للسطر الجديد):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_terms)

def save_terms(message):
    if message.text is None:
        bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال النص</b>", parse_mode='HTML')
        return
        
    new_text = message.text.strip()
    settings = read_json(SETTINGS_FILE)
    settings['terms_text'] = new_text.replace('\\n', '\n')
    write_json(SETTINGS_FILE, settings)
    bot.send_message(message.chat.id, f"<b>√ تم تحديث نص الشروط</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_referral_points')
def edit_referral_points(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>🎯 أدخل عدد النقاط التي يحصل عليها المستخدم عند دعوة شخص:</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_referral_points)

def save_referral_points(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال العدد</b>", parse_mode='HTML')
            return
            
        points = int(message.text.strip())
        settings = read_json(SETTINGS_FILE)
        settings['referral_points'] = points
        write_json(SETTINGS_FILE, settings)
        bot.send_message(message.chat.id, f"<b>√ تم تحديث نقاط الدعوة إلى:</b> {points} نقطة", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "<b>✗ الرقم غير صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'admin_payment_rates')
def admin_payment_rates(call):
    payment_settings = read_json(PAYMENT_SETTINGS_FILE)
    
    rates_text = f"""<b>💰 أسعار طرق الدفع</b>

<blockquote><b>📱 آسيا سيل:</b> {payment_settings.get('asia_points_per_1000', 1.0)} نقطة لكل 1000 دينار
<b>⭐ النجوم:</b> {payment_settings.get('stars_points_per_star', 1)} نقطة لكل نجمة
<b>💲 سعر النجوم:</b> {payment_settings.get('stars_price_per_100', 1.0)}$ لكل 100 نجمة
<b>💳 ماستر كارد:</b> نقطة لكل {payment_settings.get('master_card_rate', 1000)} دينار
<b>📲 زين كاش:</b> نقطة لكل {payment_settings.get('zain_cash_rate', 1000)} دينار</blockquote>"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('✏️ آسيا سيل', callback_data='edit_asia_rate')
    btn2 = types.InlineKeyboardButton('✏️ النجوم', callback_data='edit_stars_rate')
    btn3 = types.InlineKeyboardButton('✏️ سعر النجوم', callback_data='edit_stars_price')
    btn4 = types.InlineKeyboardButton('✏️ ماستر كارد', callback_data='edit_master_rate')
    btn5 = types.InlineKeyboardButton('✏️ زين كاش', callback_data='edit_zain_rate')
    btn6 = types.InlineKeyboardButton('⤺ رجوع', callback_data='admin_back')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=rates_text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'edit_asia_rate')
def edit_asia_rate(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>📱 أدخل عدد النقاط لكل 1000 دينار آسيا سيل (مثال: 1.0):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_asia_rate)

def save_asia_rate(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال السعر</b>", parse_mode='HTML')
            return
            
        rate = float(message.text.strip())
        payment_settings = read_json(PAYMENT_SETTINGS_FILE)
        payment_settings['asia_points_per_1000'] = rate
        write_json(PAYMENT_SETTINGS_FILE, payment_settings)
        bot.send_message(message.chat.id, f"<b>√ تم تحديث سعر آسيا سيل إلى:</b> {rate} نقطة/1000 دينار", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "<b>✗ الرقم غير صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_stars_rate')
def edit_stars_rate(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>⭐ أدخل عدد النقاط لكل نجمة (مثال: 1):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_stars_rate)

def save_stars_rate(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال السعر</b>", parse_mode='HTML')
            return
            
        rate = int(message.text.strip())
        payment_settings = read_json(PAYMENT_SETTINGS_FILE)
        payment_settings['stars_points_per_star'] = rate
        write_json(PAYMENT_SETTINGS_FILE, payment_settings)
        bot.send_message(message.chat.id, f"<b>√ تم تحديث سعر النجوم إلى:</b> {rate} نقطة/نجمة", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "<b>✗ الرقم غير صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_stars_price')
def edit_stars_price(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>💲 أدخل سعر 100 نجمة بالدولار (مثال: 1.0):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_stars_price)

def save_stars_price(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال السعر</b>", parse_mode='HTML')
            return
            
        price = float(message.text.strip())
        payment_settings = read_json(PAYMENT_SETTINGS_FILE)
        payment_settings['stars_price_per_100'] = price
        write_json(PAYMENT_SETTINGS_FILE, payment_settings)
        bot.send_message(message.chat.id, f"<b>√ تم تحديث سعر النجوم إلى:</b> {price}$ لكل 100 نجمة", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "<b>✗ الرقم غير صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_master_rate')
def edit_master_rate(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>💳 أدخل عدد الدينارات لكل نقطة (مثال: 1000 يعني نقطة لكل 1000 دينار):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_master_rate)

def save_master_rate(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال السعر</b>", parse_mode='HTML')
            return
            
        rate = int(message.text.strip())
        payment_settings = read_json(PAYMENT_SETTINGS_FILE)
        payment_settings['master_card_rate'] = rate
        write_json(PAYMENT_SETTINGS_FILE, payment_settings)
        bot.send_message(message.chat.id, f"<b>√ تم تحديث سعر ماستر كارد إلى:</b> نقطة لكل {rate} دينار", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "<b>✗ الرقم غير صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'edit_zain_rate')
def edit_zain_rate(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>📲 أدخل عدد الدينارات لكل نقطة (مثال: 1000 يعني نقطة لكل 1000 دينار):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_zain_rate)

def save_zain_rate(message):
    try:
        if message.text is None:
            bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال السعر</b>", parse_mode='HTML')
            return
            
        rate = int(message.text.strip())
        payment_settings = read_json(PAYMENT_SETTINGS_FILE)
        payment_settings['zain_cash_rate'] = rate
        write_json(PAYMENT_SETTINGS_FILE, payment_settings)
        bot.send_message(message.chat.id, f"<b>√ تم تحديث سعر زين كاش إلى:</b> نقطة لكل {rate} دينار", parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, "<b>✗ الرقم غير صحيح</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'admin_payment_methods')
def admin_payment_methods(call):
    payment_methods = read_json(PAYMENT_METHODS_FILE)
    
    methods_text = """<b>🔧 إدارة طرق الدفع</b>

<blockquote><b>الطرق المتاحة:</b></blockquote>
"""
    
    for method_id, method_data in payment_methods["methods"].items():
        status = "√ مفعل" if method_data["enabled"] else "✗ معطل"
        methods_text += f"\n{method_data['name']}: {status}"
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    for method_id, method_data in payment_methods["methods"].items():
        if method_data["enabled"]:
            btn = types.InlineKeyboardButton(f"✗ تعطيل {method_data['name']}", callback_data=f"disable_method_{method_id}")
        else:
            btn = types.InlineKeyboardButton(f"√ تفعيل {method_data['name']}", callback_data=f"enable_method_{method_id}")
        markup.add(btn)
    
    btn_back = types.InlineKeyboardButton('⤺ رجوع', callback_data='admin_back')
    markup.add(btn_back)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=methods_text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith(('enable_method_', 'disable_method_')))
def handle_payment_method_toggle(call):
    if call.data.startswith('enable_method_'):
        method_id = call.data.replace('enable_method_', '')
        action = 'enable'
    else:
        method_id = call.data.replace('disable_method_', '')
        action = 'disable'
    
    payment_methods = read_json(PAYMENT_METHODS_FILE)
    
    if method_id in payment_methods["methods"]:
        if action == 'enable':
            payment_methods["methods"][method_id]["enabled"] = True
            bot.answer_callback_query(call.id, f"√ تم تفعيل {payment_methods['methods'][method_id]['name']}", show_alert=True)
        else:
            payment_methods["methods"][method_id]["enabled"] = False
            bot.answer_callback_query(call.id, f"✗ تم تعطيل {payment_methods['methods'][method_id]['name']}", show_alert=True)
        
        write_json(PAYMENT_METHODS_FILE, payment_methods)
        admin_payment_methods(call)

@bot.callback_query_handler(func=lambda call: call.data == 'admin_subscription')
def admin_subscription(call):
    subscription_data = read_json(SUBSCRIPTION_FILE)
    
    channels_text = ""
    if subscription_data.get("channels"):
        for i, channel in enumerate(subscription_data["channels"], 1):
            try:
                channel_info = bot.get_chat(channel)
                channels_text += f"{i}. {channel_info.title} (@{channel_info.username})\n"
            except:
                channels_text += f"{i}. {channel} (غير متاح)\n"
    else:
        channels_text = "لا توجد قنوات مضافة"
    
    status = "√ مفعل" if subscription_data.get("enabled", False) else "✗ معطل"
    
    subscription_text = f"""<b>📢 قنوات الاشتراك الإجباري</b>

<blockquote><b>الحالة:</b> {status}</blockquote>

<blockquote><b>القنوات المطلوبة:</b>
{channels_text}</blockquote>"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('➕ إضافة قناة', callback_data='add_subscription_channel')
    btn2 = types.InlineKeyboardButton('➖ حذف قناة', callback_data='remove_subscription_channel')
    
    if subscription_data.get("enabled", False):
        btn3 = types.InlineKeyboardButton('✗ تعطيل الاشتراك', callback_data='disable_subscription')
    else:
        btn3 = types.InlineKeyboardButton('√ تفعيل الاشتراك', callback_data='enable_subscription')
    
    btn4 = types.InlineKeyboardButton('⤺ رجوع', callback_data='admin_back')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=subscription_text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'add_subscription_channel')
def add_subscription_channel(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "<b>📢 أرسل آيدي القناة أو اليوزر (مثال: @channel_username أو -1001234567890):</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, save_subscription_channel)

def save_subscription_channel(message):
    if message.text is None:
        bot.send_message(message.chat.id, "<b>✗ لم تقم بإرسال آيدي القناة</b>", parse_mode='HTML')
        return
    
    channel_id = message.text.strip()
    
    subscription_data = read_json(SUBSCRIPTION_FILE)
    
    if channel_id not in subscription_data["channels"]:
        subscription_data["channels"].append(channel_id)
        write_json(SUBSCRIPTION_FILE, subscription_data)
        bot.send_message(message.chat.id, f"<b>√ تمت إضافة القناة:</b> {channel_id}", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, f"<b>✗ القناة مضافة مسبقاً</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'remove_subscription_channel')
def remove_subscription_channel(call):
    subscription_data = read_json(SUBSCRIPTION_FILE)
    
    if not subscription_data.get("channels"):
        bot.answer_callback_query(call.id, "لا توجد قنوات لحذفها", show_alert=True)
        return
    
    markup = types.InlineKeyboardMarkup()
    
    for i, channel in enumerate(subscription_data["channels"]):
        try:
            channel_info = bot.get_chat(channel)
            btn = types.InlineKeyboardButton(f"حذف {channel_info.title}", callback_data=f"delete_channel_{i}")
        except:
            btn = types.InlineKeyboardButton(f"حذف {channel}", callback_data=f"delete_channel_{i}")
        markup.add(btn)
    
    btn_back = types.InlineKeyboardButton('⤺ رجوع', callback_data='admin_subscription')
    markup.add(btn_back)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="<b>اختر القناة التي تريد حذفها:</b>",
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_channel_'))
def delete_channel(call):
    index = int(call.data.replace('delete_channel_', ''))
    subscription_data = read_json(SUBSCRIPTION_FILE)
    
    if 0 <= index < len(subscription_data["channels"]):
        deleted_channel = subscription_data["channels"].pop(index)
        write_json(SUBSCRIPTION_FILE, subscription_data)
        bot.answer_callback_query(call.id, f"تم حذف القناة: {deleted_channel}", show_alert=True)
        admin_subscription(call)

@bot.callback_query_handler(func=lambda call: call.data == 'enable_subscription')
def enable_subscription(call):
    subscription_data = read_json(SUBSCRIPTION_FILE)
    subscription_data["enabled"] = True
    write_json(SUBSCRIPTION_FILE, subscription_data)
    bot.answer_callback_query(call.id, "√ تم تفعيل الاشتراك الإجباري", show_alert=True)
    admin_subscription(call)

@bot.callback_query_handler(func=lambda call: call.data == 'disable_subscription')
def disable_subscription(call):
    subscription_data = read_json(SUBSCRIPTION_FILE)
    subscription_data["enabled"] = False
    write_json(SUBSCRIPTION_FILE, subscription_data)
    bot.answer_callback_query(call.id, "✗ تم تعطيل الاشتراك الإجباري", show_alert=True)
    admin_subscription(call)

@bot.callback_query_handler(func=lambda call: call.data == 'admin_requests')
def admin_requests(call):
    requests_db = read_json(PENDING_REQUESTS_FILE)
    
    if "requests" not in requests_db or not requests_db["requests"]:
        bot.answer_callback_query(call.id, "لا توجد طلبات معلقة", show_alert=True)
        return
    
    pending_count = sum(1 for req in requests_db["requests"].values() if req.get("status") == "pending")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(f'📋 الطلبات المعلقة ({pending_count})', callback_data='view_pending')
    btn2 = types.InlineKeyboardButton('⤺ رجوع', callback_data='admin_back')
    markup.add(btn1, btn2)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"<b>📋 إدارة الطلبات</b>\n\n<blockquote>إجمالي الطلبات المعلقة: {pending_count}</blockquote>",
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'view_pending')
def view_pending(call):
    requests_db = read_json(PENDING_REQUESTS_FILE)
    
    if "requests" not in requests_db:
        bot.answer_callback_query(call.id, "لا توجد طلبات", show_alert=True)
        return
    
    pending_requests = [req for req in requests_db["requests"].values() if req.get("status") == "pending"]
    
    if not pending_requests:
        bot.answer_callback_query(call.id, "لا توجد طلبات معلقة", show_alert=True)
        return
    
    request = pending_requests[0]
    request_id = request["id"]
    user_id = request["user_id"]
    req_type = request["type"]
    
    if "gift" in req_type:
        gift_type = request["data"].get("type", "normal")
        gift_link = request["data"].get("link", "")
        
        request_text = f"""<b>📋 طلب نشر هدية</b>

<blockquote><b>• طلب ID:</b> {request_id}
<b>• المستخدم:</b> {user_id}
<b>• النوع:</b> {gift_type}
<b>• الرابط:</b> {gift_link}
<b>• التكلفة:</b> {request.get('points_required', 0)} نقطة</blockquote>"""
    elif "username" in req_type:
        username = request["data"].get("username", "")
        username_type = request["data"].get("type", "ownership")
        
        type_text = "منصة (NFT)" if username_type == "nft" else "ملكية"
        
        request_text = f"""<b>📜 طلب نشر معرف</b>

<blockquote><b>• طلب ID:</b> {request_id}
<b>• المستخدم:</b> {user_id}
<b>• النوع:</b> {type_text}
<b>• المعرف:</b> @{username}
<b>• التكلفة:</b> {request.get('points_required', 0)} نقطة</blockquote>"""
    elif req_type == "master_card":
        amount = request["data"].get("amount", 0)
        points = request["data"].get("points", 0)
        
        request_text = f"""<b>💳 طلب شحن ماستر كارد</b>

<blockquote><b>• طلب ID:</b> {request_id}
<b>• المستخدم:</b> {user_id}
<b>• المبلغ:</b> {amount} دينار
<b>• النقاط:</b> {points} نقطة</blockquote>"""
    elif req_type == "zain_cash":
        amount = request["data"].get("amount", 0)
        points = request["data"].get("points", 0)
        
        request_text = f"""<b>📲 طلب شحن زين كاش</b>

<blockquote><b>• طلب ID:</b> {request_id}
<b>• المستخدم:</b> {user_id}
<b>• المبلغ:</b> {amount} دينار
<b>• النقاط:</b> {points} نقطة</blockquote>"""
    elif req_type == "stars":
        stars_amount = request["data"].get("stars_amount", 0)
        points = request["data"].get("points", 0)
        
        request_text = f"""<b>⭐ طلب شحن بالنجوم</b>

<blockquote><b>• طلب ID:</b> {request_id}
<b>• المستخدم:</b> {user_id}
<b>• النجوم:</b> {stars_amount}
<b>• النقاط:</b> {points} نقطة</blockquote>"""
    else:
        request_text = f"""<b>📋 طلب عام</b>

<blockquote><b>• طلب ID:</b> {request_id}
<b>• المستخدم:</b> {user_id}
<b>• النوع:</b> {req_type}</blockquote>"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('√ قبول', callback_data=f'admin_approve_{request_id}')
    btn2 = types.InlineKeyboardButton('✗ رفض', callback_data=f'admin_reject_{request_id}')
    btn3 = types.InlineKeyboardButton('⏭️ تخطي', callback_data='view_pending')
    btn4 = types.InlineKeyboardButton('⤺ رجوع', callback_data='admin_requests')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=request_text,
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_approve_'))
def admin_approve_request(call):
    request_id = call.data.replace('admin_approve_', '')
    request_info = get_request_data(request_id)
    
    if not request_info:
        bot.answer_callback_query(call.id, "<b>الطلب غير موجود</b>", show_alert=True)
        return
    
    user_id = int(request_info["user_id"])
    
    if "gift" in request_info["type"]:
        gift_type = request_info["data"].get("type", "normal")
        gift_link = request_info["data"].get("link", "")
        
        if gift_link:
            message_id = publish_gift_to_channel(gift_link, gift_type)
            if message_id and message_id != "cooldown":
                bot.send_message(user_id, 
                                f"""<b>√ تم نشر هديتك بنجاح!</b>

<blockquote><b>🔗 رابط هديتك:</b> https://t.me/c/{str(CHANNEL_ID).replace('-100', '')}/{message_id}</blockquote>""",
                                parse_mode='HTML')
                
                points_needed = request_info.get("points_required", 0)
                subtract_user_points(user_id, points_needed)
            elif message_id == "cooldown":
                bot.send_message(user_id, "<b>⏳ سيتم نشر هديتك قريباً</b>", parse_mode='HTML')
                
                request_info["status"] = "waiting"
                update_request_status(request_id, "waiting")
                bot.answer_callback_query(call.id, "<b>تم حفظ الطلب للنشر لاحقاً</b>", show_alert=True)
                view_pending(call)
                return
            else:
                bot.send_message(user_id, "<b>✗ حدث خطأ في نشر الهدية</b>", parse_mode='HTML')
                bot.answer_callback_query(call.id, "<b>حدث خطأ في النشر</b>", show_alert=True)
                view_pending(call)
                return
    
    elif "username" in request_info["type"]:
        username = request_info["data"].get("username", "")
        username_type = request_info["data"].get("type", "ownership")
        
        if username:
            message_id = publish_username_to_channel(username, username_type)
            if message_id and message_id != "cooldown":
                bot.send_message(user_id, 
                                f"""<b>√ تم نشر معرفك بنجاح!</b>

<blockquote><b>🔗 رابط معرفك:</b> https://t.me/c/{str(CHANNEL_ID).replace('-100', '')}/{message_id}</blockquote>""",
                                parse_mode='HTML')
                
                points_needed = request_info.get("points_required", 0)
                subtract_user_points(user_id, points_needed)
            elif message_id == "cooldown":
                bot.send_message(user_id, "<b>⏳ سيتم نشر معرفك قريباً</b>", parse_mode='HTML')
                
                request_info["status"] = "waiting"
                update_request_status(request_id, "waiting")
                bot.answer_callback_query(call.id, "<b>تم حفظ الطلب للنشر لاحقاً</b>", show_alert=True)
                view_pending(call)
                return
            else:
                bot.send_message(user_id, "<b>✗ حدث خطأ في نشر المعرف</b>", parse_mode='HTML')
                bot.answer_callback_query(call.id, "<b>حدث خطأ في النشر</b>", show_alert=True)
                view_pending(call)
                return
    
    elif request_info["type"] in ["master_card", "zain_cash", "stars"]:
        points_to_add = request_info["data"]["points"]
        new_balance = add_user_points(user_id, points_to_add)
        
        if request_info["type"] == "stars":
            amount_text = f"النجوم: {request_info['data']['stars_amount']} نجمة"
        else:
            amount_text = f"المبلغ: {request_info['data']['amount']} دينار"
        
        bot.send_message(user_id, 
                        f"""<b>√ تمت الموافقة على طلب الشحن!</b>

<blockquote><b>📊 التفاصيل:</b>
• {amount_text}
• النقاط المضافة: {points_to_add} نقطة
• رصيدك الجديد: {new_balance} نقطة</blockquote>""",
                        parse_mode='HTML')
    
    update_request_status(request_id, "approved")
    bot.answer_callback_query(call.id, "<b>تم قبول الطلب</b>", show_alert=True)
    view_pending(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_reject_'))
def admin_reject_request(call):
    request_id = call.data.replace('admin_reject_', '')
    request_info = get_request_data(request_id)
    
    if not request_info:
        bot.answer_callback_query(call.id, "<b>الطلب غير موجود</b>", show_alert=True)
        return
    
    user_id = int(request_info["user_id"])
    
    if request_info["type"] in ["master_card", "zain_cash", "stars"]:
        bot.send_message(user_id, "<b>✗ تم رفض طلب الشحن. يرجى التواصل مع المسؤول.</b>", parse_mode='HTML')
    else:
        bot.send_message(user_id, "<b>✗ تم رفض طلبك</b>", parse_mode='HTML')
    
    update_request_status(request_id, "rejected")
    bot.answer_callback_query(call.id, "<b>تم رفض الطلب</b>", show_alert=True)
    view_pending(call)

@bot.callback_query_handler(func=lambda call: call.data == 'admin_back')
def admin_back(call):
    admin_command(call.message)

if __name__ == '__main__':
    init_files()
    print("=" * 50)
    print("√ البوت يعمل بنجاح!")
    print("=" * 50)
    
    
    waiting_thread = Thread(target=check_and_publish_waiting)
    waiting_thread.daemon = True
    waiting_thread.start()
    
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f" خطأ: {e}")
        time.sleep(5)