import telebot
import requests
import time
import sqlite3
from datetime import datetime
from user_agent import generate_user_agent
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# استبدل 'YOUR_BOT_TOKEN' بالتوكين الخاص ببوتك
BOT_TOKEN = 'توكنك' #روح سطر (339) خلي ايديك مطوؤ
bot = telebot.TeleBot(BOT_TOKEN)

# قناة المطور (إلزامي)
CHANNEL_USERNAME = '@قناتك _اجباري'

# إنشاء قاعدة بيانات لحفظ بيانات المستخدمين
def init_db():
    conn = sqlite3.connect('instagram_bot.db')
    cursor = conn.cursor()
    
    # جدول المستخدمين
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        session_id TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # جدول التعليقات
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        post_id TEXT,
        comment_text TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# التحقق من اشتراك المستخدم في القناة
def check_subscription(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except:
        return False

# زر للاشتراك في القناة
def subscription_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("📢 قناة البوت", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
    )
    keyboard.row(
        InlineKeyboardButton("✅ تأكيد الاشتراك", callback_data="check_subscription")
    )
    return keyboard

# لوحة الأزرار الرئيسية
def main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔐 تسجيل الدخول", callback_data="login"),
        InlineKeyboardButton("🗑️ حذف الحساب", callback_data="delete_account"),
        InlineKeyboardButton("💬 نشر تعليقات", callback_data="start_comments"),
        InlineKeyboardButton("📊 حالة الحساب", callback_data="account_status"),
        InlineKeyboardButton("🆘 المساعدة", callback_data="help"),
        InlineKeyboardButton("👤 المطور", url="https://t.me/S7ASA7")
    )
    return keyboard

# لوحة تعليقات
def comments_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("✏️ تعليق واحد", callback_data="single_comment"),
        InlineKeyboardButton("🔄 تعليقات متعددة", callback_data="multi_comments"),
        InlineKeyboardButton("📝 تعديل النص", callback_data="edit_comment"),
        InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    )
    return keyboard

# تسجيل دخول إنستجرام
def instagram_login(username, password):
    try:
        cookies = {
            'csrftoken': 'VV76QOVaOeJRtIkOqyWJmu',
            'datr': 'wkBuaSyzwJm5epmg1_scY2gW',
            'ig_did': 'B6DEA0BD-C2A7-4983-B756-742D9E1F5E69',
            'ps_l': '1',
            'ps_n': '1',
            'dpr': '3.0234789848327637',
            'wd': '891x1671',
        }

        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-full-version-list': '"Chromium";v="137.0.7337.0", "Not/A)Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Linux"',
            'sec-ch-ua-platform-version': '""',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': str(generate_user_agent()),
            'x-asbd-id': '359341',
            'x-csrftoken': 'VV76QOVaOeJRtIkOqyWJmu',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': '0',
            'x-instagram-ajax': '1032159121',
            'x-requested-with': 'XMLHttpRequest',
            'x-web-session-id': 'onyrw7:w1hc2o:kgnxsu',
        }

        t = str(time.time()).split(".")[0]
        data = {
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{t}:{password}',
            'caaF2DebugGroup': '0',
            'isPrivacyPortalReq': 'false',
            'loginAttemptSubmissionCount': '0',
            'optIntoOneTap': 'false',
            'queryParams': '{}',
            'trustedDeviceRecords': '{}',
            'username': username,
            'jazoest': '21956',
        }

        response = requests.post(
            'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
            cookies=cookies, headers=headers, data=data, timeout=30
        )

        if "userId" in response.text:
            se = response.cookies.get_dict()
            session_id = se.get('sessionid', '')
            return {'success': True, 'session_id': session_id, 'message': 'تم تسجيل الدخول بنجاح'}
        else:
            return {'success': False, 'message': 'فشل تسجيل الدخول - تأكد من البيانات'}
            
    except requests.exceptions.Timeout:
        return {'success': False, 'message': 'انتهت المهلة - حاول مرة أخرى'}
    except Exception as e:
        return {'success': False, 'message': f'خطأ: {str(e)}'}

# نشر تعليق
def post_comment(session_id, post_id, comment_text):
    try:
        cookies = {
            'ig_did': 'C6C74DA4-B893-4F20-823D-D7EB2F30D35B',
            'csrftoken': 'MKGunz5BCC6QccQKBiW1-l',
            'datr': 'lhtuaUqx-dhAmDI6PMpoEP8e',
            'ps_l': '1',
            'ps_n': '1',
            'mid': 'aW4cYgABAAEJXUBvld-hTUPP742l',
            'ds_user_id': '76303971746',
            'dpr': '3.0234789848327637',
            'sessionid': session_id,
            'rur': '"RVA\\05476303971746\\0541800366491:01fe82669faf769995d8e7a182c7e0c30b54ce242432673733bc87491122081efc1814df"',
            'wd': '891x946',
        }
        
        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/p/DTpr8OkEXYq/',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-full-version-list': '"Chromium";v="137.0.7337.0", "Not/A)Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Linux"',
            'sec-ch-ua-platform-version': '""',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': str(generate_user_agent()),
            'x-asbd-id': '359341',
            'x-csrftoken': 'MKGunz5BCC6QccQKBiW1-l',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': 'hmac.AR2ZebPnMV8oF_FGwsM0MVblQPCh470v2aqmAowZOV6WCuTT',
            'x-instagram-ajax': '1032157550',
            'x-requested-with': 'XMLHttpRequest',
            'x-web-session-id': 'e1az7q:wbo8ag:a69ymb',
        }
        
        data = {
            'comment_text': comment_text,
            'jazoest': '21774',
        }
        
        response = requests.post(
            f'https://www.instagram.com/api/v1/web/comments/{post_id}/add/',
            cookies=cookies,
            headers=headers,
            data=data,
            timeout=30
        )
        
        if '"status":"ok"' in response.text:
            return {'success': True, 'message': 'تم نشر التعليق بنجاح'}
        else:
            return {'success': False, 'message': 'فشل نشر التعليق'}
            
    except requests.exceptions.Timeout:
        return {'success': False, 'message': 'انتهت المهلة - حاول مرة أخرى'}
    except Exception as e:
        return {'success': False, 'message': f'خطأ: {str(e)}'}

# حفظ بيانات المستخدم
def save_user(user_id, username, password, session_id):
    conn = sqlite3.connect('instagram_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR REPLACE INTO users (user_id, username, password, session_id, is_active)
    VALUES (?, ?, ?, ?, 1)
    ''', (user_id, username, password, session_id))
    
    conn.commit()
    conn.close()

# جلب بيانات المستخدم
def get_user(user_id):
    conn = sqlite3.connect('instagram_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    conn.close()
    return user

# حذف حساب المستخدم
def delete_user(user_id):
    conn = sqlite3.connect('instagram_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    
    conn.commit()
    conn.close()

# حفظ التعليق
def save_comment(user_id, post_id, comment_text, status):
    conn = sqlite3.connect('instagram_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO comments (user_id, post_id, comment_text, status)
    VALUES (?, ?, ?, ?)
    ''', (user_id, post_id, comment_text, status))
    
    conn.commit()
    conn.close()

# ============ تعريف الأوامر ============
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    if not check_subscription(user_id):
        bot.send_message(
            user_id,
            "🔒 **مرحباً بك في بوت إنستجرام**\n\n"
            "يجب الاشتراك في قناة البوت أولاً لاستخدام الخدمة:\n",
            reply_markup=subscription_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    welcome_text = """
🎉 **أهلاً بك في بوت إنستجرام المتكامل**

🧾 **الخدمات المتاحة:**
🔐 تسجيل دخول إنستجرام
💬 نشر تعليقات تلقائي
📊 متابعة حالة الحساب
🔄 إدارة متعددة للحسابات

👨‍💻 **المطور:** @S7ASA7

📌 **اختر من الأزرار أدناه:**
    """
    
    bot.send_message(user_id, welcome_text, 
                     reply_markup=main_keyboard(), parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
🆘 **دليل استخدام البوت:**

1️⃣ **تسجيل الدخول:**
   - انقر على زر "تسجيل الدخول"
   - أدخل اسم المستخدم
   - أدخل كلمة المرور

2️⃣ **نشر التعليقات:**
   - اختر "نشر تعليقات"
   - اختر نوع النشر
   - أدخل ID المنشور
   - أدخل نص التعليق

3️⃣ **إدارة الحساب:**
   - يمكنك حذف حسابك
   - معرفة حالة حسابك

⚠️ **ملاحظات:**
- البيانات محفوظة بشكل آمن
- البوت لأغراض تعليمية فقط
- يمنع استخدامه في الإساءة

📞 **الدعم:** @S7ASA7
    """
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id not in [YOUR_USER_ID]:  # استبدل برقمك
        return
    
    conn = sqlite3.connect('instagram_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM comments')
    total_comments = cursor.fetchone()[0]
    
    conn.close()
    
    stats_text = f"""
📊 **إحصائيات البوت:**

👥 المستخدمون: {total_users}
💬 التعليقات: {total_comments}
🕒 الوقت: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')

# ============ معالجة Callback ============
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    
    if call.data == "check_subscription":
        if check_subscription(user_id):
            start_command(call.message)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في القناة بعد!")
    
    elif call.data == "login":
        msg = bot.send_message(user_id, "👤 **أدخل اسم المستخدم:**", parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_username)
    
    elif call.data == "delete_account":
        user_data = get_user(user_id)
        if user_data:
            keyboard = InlineKeyboardMarkup()
            keyboard.row(
                InlineKeyboardButton("✅ نعم", callback_data="confirm_delete"),
                InlineKeyboardButton("❌ لا", callback_data="cancel_delete")
            )
            bot.send_message(user_id, "⚠️ **هل أنت متأكد من حذف حسابك؟**\nسيتم حذف جميع بياناتك.", 
                           reply_markup=keyboard, parse_mode='Markdown')
        else:
            bot.send_message(user_id, "❌ ليس لديك حساب مسجل!", parse_mode='Markdown')
    
    elif call.data == "confirm_delete":
        delete_user(user_id)
        bot.send_message(user_id, "✅ **تم حذف حسابك بنجاح**", parse_mode='Markdown')
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
    
    elif call.data == "cancel_delete":
        bot.send_message(user_id, "❌ **تم إلغاء الحذف**", parse_mode='Markdown')
        bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
    
    elif call.data == "start_comments":
        user_data = get_user(user_id)
        if user_data and user_data[4] == 1:  # is_active
            bot.send_message(user_id, "💬 **اختر نوع النشر:**", 
                           reply_markup=comments_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(user_id, "❌ **يجب تسجيل الدخول أولاً!**", parse_mode='Markdown')
    
    elif call.data == "single_comment":
        msg = bot.send_message(user_id, "🔢 **أدخل ID المنشور:**\n\nمثال: DTpr8OkEXYq", parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_post_id)
    
    elif call.data == "multi_comments":
        bot.send_message(user_id, "⏳ **قريباً...**", parse_mode='Markdown')
    
    elif call.data == "account_status":
        user_data = get_user(user_id)
        if user_data:
            conn = sqlite3.connect('instagram_bot.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM comments WHERE user_id = ?', (user_id,))
            comments_count = cursor.fetchone()[0]
            conn.close()
            
            status_text = f"""
📊 **حالة حسابك:**

👤 المستخدم: `{user_data[1]}`
🔄 الحالة: {'✅ نشط' if user_data[4] == 1 else '❌ غير نشط'}
💬 التعليقات: {comments_count}
📅 تاريخ التسجيل: {user_data[5]}
            """
            bot.send_message(user_id, status_text, parse_mode='Markdown')
        else:
            bot.send_message(user_id, "❌ **ليس لديك حساب مسجل!**", parse_mode='Markdown')
    
    elif call.data == "help":
        help_command(call.message)
    
    elif call.data == "back_to_main":
        start_command(call.message)
    
    bot.answer_callback_query(call.id)

# ============ معالجة الخطوات ============
def process_username(message):
    username = message.text.strip()
    msg = bot.send_message(message.chat.id, "🔒 **أدخل كلمة المرور:**", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_password, username)

def process_password(message, username):
    password = message.text.strip()
    
    # إظهار رسالة انتظار
    wait_msg = bot.send_message(message.chat.id, "⏳ **جاري تسجيل الدخول...**", parse_mode='Markdown')
    
    # تشغيل في thread منفصل
    def login_thread():
        result = instagram_login(username, password)
        
        if result['success']:
            save_user(message.from_user.id, username, password, result['session_id'])
            bot.edit_message_text(
                "✅ **تم تسجيل الدخول بنجاح!**\n\n"
                f"👤 المستخدم: `{username}`\n"
                "🔄 تم حفظ بيانات الجلسة",
                message.chat.id,
                wait_msg.message_id,
                parse_mode='Markdown'
            )
        else:
            bot.edit_message_text(
                f"❌ **فشل تسجيل الدخول**\n\n"
                f"الخطأ: {result['message']}\n\n"
                "⚠️ تأكد من:\n"
                "1- صحة البيانات\n"
                "2- اتصال الإنترنت\n"
                "3- عدم تفعيل التحقق بخطوتين",
                message.chat.id,
                wait_msg.message_id,
                parse_mode='Markdown'
            )
    
    threading.Thread(target=login_thread).start()

def process_post_id(message):
    post_id = message.text.strip()
    msg = bot.send_message(message.chat.id, "📝 **أدخل نص التعليق:**", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_comment_text, post_id)

def process_comment_text(message, post_id):
    comment_text = message.text.strip()
    user_id = message.from_user.id
    
    user_data = get_user(user_id)
    if not user_data:
        bot.send_message(user_id, "❌ **يجب تسجيل الدخول أولاً!**", parse_mode='Markdown')
        return
    
    # إظهار رسالة انتظار
    wait_msg = bot.send_message(user_id, "⏳ **جاري نشر التعليق...**", parse_mode='Markdown')
    
    # تشغيل في thread منفصل
    def comment_thread():
        session_id = user_data[3]  # session_id
        result = post_comment(session_id, post_id, comment_text)
        
        if result['success']:
            save_comment(user_id, post_id, comment_text, 'success')
            bot.edit_message_text(
                "✅ **تم نشر التعليق بنجاح!**\n\n"
                f"🔢 المنشور: `{post_id}`\n"
                f"💬 النص: {comment_text}\n\n"
                "📊 تم حفظ العملية في السجلات",
                message.chat.id,
                wait_msg.message_id,
                parse_mode='Markdown'
            )
        else:
            save_comment(user_id, post_id, comment_text, 'failed')
            bot.edit_message_text(
                f"❌ **فشل نشر التعليق**\n\n"
                f"الخطأ: {result['message']}\n\n"
                f"🔢 المنشور: `{post_id}`\n"
                f"💬 النص: {comment_text}",
                message.chat.id,
                wait_msg.message_id,
                parse_mode='Markdown'
            )
    
    threading.Thread(target=comment_thread).start()

# ============ تشغيل البوت ============
if __name__ == "__main__":
    print("🚀 جاري تشغيل بوت إنستجرام...")
    print(f"📢 قناة البوت: {CHANNEL_USERNAME}")
    print("⚡ البوت يعمل الآن!\n")
    
    # تهيئة قاعدة البيانات
    init_db()
    
    try:
        bot.polling(none_stop=True, interval=1, timeout=60)
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")