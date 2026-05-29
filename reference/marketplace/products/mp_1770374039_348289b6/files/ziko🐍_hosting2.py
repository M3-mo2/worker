#الملف من كتابتى الخاصه  من الصفر  @Zeko12e
#جميع الحقوق محفوظه للقناه https://t.me/zeko_1123
#لاتخمط واذكر المصدر 🐍

import telebot
from telebot import types
import os
import subprocess
import sqlite3
import signal
import time
from datetime import datetime

# --- الإعدادات الأساسية ---
BOT_TOKEN = 'توكنك ي حب 🐍'
ADMIN_ID = #ايدى المطور 👁️‍🗨️
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "هنا ي حب حط الملف db 💬")
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")

# إنشاء المجلدات
#المطور @Zeko12e
os.makedirs(PROJECTS_DIR, exist_ok=True)

# --- إعداد وتحديث قاعدة البيانات ---
def setup_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = conn.cursor()
    # إنشاء الجداول الأساسية
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, approved INTEGER, banned INTEGER DEFAULT 0)")
    cur.execute("CREATE TABLE IF NOT EXISTS files (user_id INTEGER, filename TEXT, pid INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS pending_files (file_id TEXT PRIMARY KEY, user_id INTEGER, file_name TEXT, original_file_id TEXT, upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    
    # تحديث تلقائي
    try:
        cur.execute("ALTER TABLE users ADD COLUMN banned INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass
    
    conn.commit()
    return conn, cur

db, sql = setup_db()

bot = telebot.TeleBot(BOT_TOKEN)

# --- وظائف التحكم في العمليات ---
def start_process(file_path):
    try:
        proc = subprocess.Popen(['python', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc.pid
    except Exception as e:
        print(f"Error starting process: {e}")
        return None

def stop_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        time.sleep(0.5)  # إعطاء وقت للإيقاف
        return True
    except ProcessLookupError:
        return True  # العملية غير موجودة بالفعل
    except Exception as e:
        print(f"Error stopping process: {e}")
        return False

# --- فحص حالة المستخدم ---
def check_user(uid):
    sql.execute("SELECT approved, banned FROM users WHERE id=?", (uid,))
    res = sql.fetchone()
    if not res:
        return {"approved": 0, "banned": 0}
    return {"approved": res[0], "banned": res[1]}

# --- الأوامر الأساسية ---
@bot.message_handler(commands=['start'])
def welcome(message):
    uid = message.from_user.id
    status = check_user(uid)
    
    if status['banned'] == 1:
        return bot.send_message(uid, "🚫 **تم حظرك**\n\n❌ نعتذر، لقد تم حظرك من استخدام استضافة زيكو.\n\n📞 للاستفسار: @Zeko12e")
    
    if uid == ADMIN_ID:
        # لوحة تحكم المطور
        admin_menu(message)
    elif status['approved'] == 1:
        main_menu(message)
    else:
        sql.execute("INSERT OR IGNORE INTO users (id, approved) VALUES (?, 0)", (uid,))
        db.commit()
        
        welcome_text = """
🛡️ **أهلاً بك في استضافة زيكو**

🔒 **حسابك غير مفعل حالياً**
لتفعيل حسابك والاستفادة من جميع الميزات:

1️⃣ تواصل مع المطور @Zeko12e
2️⃣ أرسل له الأيدي: `{}`
3️⃣ انتظر رسالة التفعيل

⚡ **مميزات الاستضافة:**
• تشغيل 24/7
• دعم فني مباشر
• مراقبة الأداء
        """.format(uid)
        
        bot.send_message(uid, welcome_text, parse_mode="Markdown")
        
        # إرسال إشعار للمطور
        admin_notif = """
🔔 **طلب تفعيل جديد**

👤 **المستخدم:** {}
🆔 **الأيدي:** `{}`
📅 **الوقت:** {}
        """.format(
            message.from_user.first_name,
            uid,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ تفعيل المستخدم", callback_data=f"activate_{uid}"))
        
        bot.send_message(ADMIN_ID, admin_notif, reply_markup=markup, parse_mode="Markdown")

def main_menu(message):
    uid = message.from_user.id
    
    # حساب عدد الملفات
    user_dir = os.path.join(PROJECTS_DIR, str(uid))
    file_count = len(os.listdir(user_dir)) if os.path.exists(user_dir) else 0
    
    # حساب الملفات النشطة
    sql.execute("SELECT COUNT(*) FROM files WHERE user_id=?", (uid,))
    active_count = sql.fetchone()[0]
    
    menu_text = """
🚀 **لوحة تحكم زيكو**

📊 **إحصائيات حسابك:**
• 📁 الملفات المرفوعة: {}
• ⚡ الملفات النشطة: {}
• 📅 تاريخ الاشتراك: دائم

🔧 **اختر من القائمة:**
    """.format(file_count, active_count)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📤 رفع سكربت جديد", callback_data="upload"),
        types.InlineKeyboardButton("⚙️ إدارة الملفات", callback_data="manage_files"),
        types.InlineKeyboardButton("📊 إحصائيات", callback_data="stats"),
        types.InlineKeyboardButton("🆘 المساعدة", callback_data="help"),
        types.InlineKeyboardButton("👤 المطور", url="https://t.me/Zeko12e")
    )
    
    bot.send_message(message.chat.id, menu_text, reply_markup=markup, parse_mode="Markdown")

def admin_menu(message):
    menu_text = """
⚙️ **لوحة تحكم المطور**

👑 **مرحباً بك أيها المطور**
إليك قائمة التحكم الكاملة:
    """
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📋 طلبات الرفع", callback_data="admin_pending"),
        types.InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users"),
        types.InlineKeyboardButton("📢 إرسال إشعار", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("📊 إحصائيات", callback_data="admin_stats"),
        types.InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_main")
    )
    
    bot.send_message(message.chat.id, menu_text, reply_markup=markup, parse_mode="Markdown")

# --- نظام رفع الملفات ---
@bot.callback_query_handler(func=lambda call: call.data == "upload")
def upload_init(call):
    status = check_user(call.from_user.id)
    if status['banned']:
        return bot.answer_callback_query(call.id, "❌ حسابك محظور!", show_alert=True)
    
    # التحقق من وجود مساحة كافية
    user_dir = os.path.join(PROJECTS_DIR, str(call.from_user.id))
    if os.path.exists(user_dir):
        file_count = len(os.listdir(user_dir))
        if file_count >= 10:  # حد 10 ملفات لكل مستخدم
            return bot.answer_callback_query(call.id, "❌ وصلت للحد الأقصى (10 ملفات)!", show_alert=True)
    
    upload_guide = """
📤 **رفع سكربت جديد**

📝 **الشروط والمتطلبات:**
✓ الملف بصيغة .py فقط
✓ حجم أقل من 20 ميجابايت
✓ لا يحتوي على أكواد ضارة
✓ مراجعة المطور قبل التشغيل

⏱️ **مدة المراجعة:** 1-24 ساعة
🔔 **سيتم إعلامك فور الموافقة**

📄 **أرسل ملف السكربت الآن:**
    """
    
    bot.edit_message_text(
        upload_guide,
        call.message.chat.id,
        call.message.message_id,
        parse_mode="Markdown"
    )
    
    msg = bot.send_message(call.message.chat.id, "📎 **بانتظار ملفك...**")
    bot.register_next_step_handler(msg, process_upload_request)

def process_upload_request(message):
    uid = message.from_user.id
    
    # التحقق من وجود الملف
    if not message.document:
        bot.send_message(uid, "❌ **خطأ في الرفع**\n\n⚠️ يرجى إرسال ملف وليس نصاً.")
        return main_menu(message)
    
    # التحقق من صيغة الملف
    if not message.document.file_name.endswith('.py'):
        bot.send_message(uid, "❌ **خطأ في الصيغة**\n\n⚠️ يسمح فقط بملفات بايثون (.py)")
        return main_menu(message)
    
    # التحقق من الحجم
    if message.document.file_size > 20 * 1024 * 1024:  # 20MB
        bot.send_message(uid, "❌ **حجم الملف كبير**\n\n⚠️ الحد الأقصى 20 ميجابايت")
        return main_menu(message)
    
    fid = message.document.file_id
    fname = message.document.file_name
    
    # إنشاء معرف فريد للملف
    unique_id = f"{uid}_{int(time.time())}_{fname}"
    
    # حفظ في قاعدة البيانات
    sql.execute("""
        INSERT INTO pending_files (file_id, user_id, file_name, original_file_id) 
        VALUES (?, ?, ?, ?)
    """, (unique_id, uid, fname, fid))
    db.commit()
    
    # إرسال إشعار للمستخدم
    user_notif = """
✅ **تم استلام ملفك بنجاح!**

📄 **اسم الملف:** `{}`
📊 **الحجم:** {} كيلوبايت
🕐 **وقت الرفع:** {}
📋 **حالة المراجعة:** ⏳ قيد المراجعة

🔔 **سيتم إعلامك فور الانتهاء من المراجعة.**
    """.format(
        fname,
        message.document.file_size // 1024,
        datetime.now().strftime('%H:%M:%S')
    )
    
    bot.send_message(uid, user_notif, parse_mode="Markdown")
    
    # إرسال للمطور
    admin_notif = """
📬 **طلب رفع جديد**

👤 **المستخدم:** [{}](tg://user?id={})
🆔 **الأيدي:** `{}`
📄 **الملف:** `{}`
📊 **الحجم:** {} كيلوبايت
📅 **الوقت:** {}

📋 **اختر الإجراء:**
    """.format(
        message.from_user.first_name,
        uid,
        uid,
        fname,
        message.document.file_size // 1024,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📥 تحميل الملف", callback_data=f"view_file_{unique_id}"),
        types.InlineKeyboardButton("✅ قبول الملف", callback_data=f"accept_{unique_id}"),
        types.InlineKeyboardButton("❌ رفض الملف", callback_data=f"reject_{unique_id}"),
        types.InlineKeyboardButton("👤 معلومات", callback_data=f"user_info_{uid}")
    )
    
    bot.send_message(ADMIN_ID, admin_notif, reply_markup=markup, parse_mode="Markdown")

# --- معالجة الأزرار (محسنة) ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    try:
        data = call.data
        
        if data == "back_to_main":
            main_menu(call.message)
        
        elif data == "manage_files":
            list_user_files(call)
        
        elif data == "stats":
            show_stats(call)
        
        elif data == "help":
            show_help(call)
        
        elif data == "admin_pending":
            show_pending_files(call)
        
        elif data == "admin_users":
            show_all_users(call)
        
        elif data == "admin_broadcast":
            start_broadcast(call)
        
        elif data == "admin_stats":
            show_admin_stats(call)
        
        elif data.startswith("view_file_"):
            view_pending_file(call)
        
        elif data.startswith("accept_"):
            accept_file(call)
        
        elif data.startswith("reject_"):
            reject_file(call)
        
        elif data.startswith("user_info_"):
            show_user_info(call)
        
        elif data.startswith("activate_"):
            activate_user(call)
        
        elif data.startswith("managefile_"):
            file_actions(call)
        
        elif data.startswith("run_"):
            run_file(call)
        
        elif data.startswith("stop_"):
            stop_file(call)
        
        elif data.startswith("delete_"):
            delete_file(call)
        
        else:
            bot.answer_callback_query(call.id, "❌ هذا الزر غير متاح حالياً", show_alert=True)
            
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ حدث خطأ: {str(e)[:100]}", show_alert=True)

# --- وظائف إدارة الملفات ---
def list_user_files(call):
    uid = call.from_user.id
    user_dir = os.path.join(PROJECTS_DIR, str(uid))
    
    if not os.path.exists(user_dir) or not os.listdir(user_dir):
        bot.edit_message_text(
            "📂 **لا توجد ملفات**\n\n❌ لم تقم برفع أي ملفات بعد.\n\n📤 استخدم زر 'رفع سكربت جديد' لبدء الاستضافة.",
            call.message.chat.id,
            call.message.message_id
        )
        return
    
    files = os.listdir(user_dir)
    text = "📂 **ملفاتك المرفوعة**\n\n"
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    for filename in files:
        # التحقق من حالة التشغيل
        sql.execute("SELECT pid FROM files WHERE user_id=? AND filename=?", (uid, filename))
        is_running = sql.fetchone()
        
        status = "🟢 نشط" if is_running else "🔴 متوقف"
        size = os.path.getsize(os.path.join(user_dir, filename)) // 1024  # حجم بالكيلوبايت
        
        text += f"📄 `{filename}`\n"
        text += f"   📊 الحجم: {size} كيلوبايت\n"
        text += f"   ⚡ الحالة: {status}\n\n"
        
        # إضافة زر التحكم
        btn_text = "🛑 إيقاف" if is_running else "▶️ تشغيل"
        btn_data = f"stop_{filename}" if is_running else f"run_{filename}"
        
        markup.add(
            types.InlineKeyboardButton(btn_text, callback_data=btn_data),
            types.InlineKeyboardButton("🗑️ حذف", callback_data=f"delete_{filename}")
        )
    
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )

def file_actions(call):
    filename = call.data.split("_", 1)[1]
    uid = call.from_user.id
    filepath = os.path.join(PROJECTS_DIR, str(uid), filename)
    
    if not os.path.exists(filepath):
        return bot.answer_callback_query(call.id, "❌ الملف غير موجود!", show_alert=True)
    
    # التحقق من حالة التشغيل
    sql.execute("SELECT pid FROM files WHERE user_id=? AND filename=?", (uid, filename))
    is_running = sql.fetchone()
    
    text = f"""
🛠️ **تحكم في الملف**

📄 **الاسم:** `{filename}`
📊 **الحجم:** {os.path.getsize(filepath) // 1024} كيلوبايت
⚡ **الحالة:** {'🟢 نشط' if is_running else '🔴 متوقف'}
📅 **تاريخ الرفع:** {datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d')}
    """
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if is_running:
        markup.add(types.InlineKeyboardButton("🛑 إيقاف التشغيل", callback_data=f"stop_{filename}"))
    else:
        markup.add(types.InlineKeyboardButton("▶️ بدء التشغيل", callback_data=f"run_{filename}"))
    
    markup.add(
        types.InlineKeyboardButton("🗑️ حذف الملف", callback_data=f"delete_{filename}"),
        types.InlineKeyboardButton("🔙 رجوع", callback_data="manage_files")
    )
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )

def run_file(call):
    filename = call.data.split("_", 1)[1]
    uid = call.from_user.id
    filepath = os.path.join(PROJECTS_DIR, str(uid), filename)
    
    if not os.path.exists(filepath):
        return bot.answer_callback_query(call.id, "❌ الملف غير موجود!", show_alert=True)
    
    # التحقق مما إذا كان الملف قيد التشغيل بالفعل
    sql.execute("SELECT pid FROM files WHERE user_id=? AND filename=?", (uid, filename))
    if sql.fetchone():
        return bot.answer_callback_query(call.id, "⚠️ الملف قيد التشغيل بالفعل!", show_alert=True)
    
    # بدء التشغيل
    pid = start_process(filepath)
    
    if pid:
        sql.execute("INSERT INTO files (user_id, filename, pid) VALUES (?, ?, ?)", (uid, filename, pid))
        db.commit()
        bot.answer_callback_query(call.id, "✅ تم بدء تشغيل السكربت بنجاح!")
        list_user_files(call)
    else:
        bot.answer_callback_query(call.id, "❌ فشل في تشغيل الملف!", show_alert=True)

def stop_file(call):
    filename = call.data.split("_", 1)[1]
    uid = call.from_user.id
    
    # البحث عن PID
    sql.execute("SELECT pid FROM files WHERE user_id=? AND filename=?", (uid, filename))
    result = sql.fetchone()
    
    if not result:
        return bot.answer_callback_query(call.id, "❌ الملف غير قيد التشغيل!", show_alert=True)
    
    pid = result[0]
    
    # إيقاف العملية
    if stop_process(pid):
        sql.execute("DELETE FROM files WHERE user_id=? AND filename=?", (uid, filename))
        db.commit()
        bot.answer_callback_query(call.id, "✅ تم إيقاف السكربت بنجاح!")
        list_user_files(call)
    else:
        bot.answer_callback_query(call.id, "❌ فشل في إيقاف الملف!", show_alert=True)

def delete_file(call):
    filename = call.data.split("_", 1)[1]
    uid = call.from_user.id
    filepath = os.path.join(PROJECTS_DIR, str(uid), filename)
    
    # إيقاف الملف إذا كان قيد التشغيل
    sql.execute("SELECT pid FROM files WHERE user_id=? AND filename=?", (uid, filename))
    result = sql.fetchone()
    if result:
        stop_process(result[0])
        sql.execute("DELETE FROM files WHERE user_id=? AND filename=?", (uid, filename))
    
    # حذف الملف
    if os.path.exists(filepath):
        os.remove(filepath)
    
    bot.answer_callback_query(call.id, "✅ تم حذف الملف بنجاح!")
    list_user_files(call)

# --- وظائف المساعدة والإحصائيات ---
def show_stats(call):
    uid = call.from_user.id
    user_dir = os.path.join(PROJECTS_DIR, str(uid))
    
    # حساب الملفات
    total_files = len(os.listdir(user_dir)) if os.path.exists(user_dir) else 0
    
    # حساب الملفات النشطة
    sql.execute("SELECT COUNT(*) FROM files WHERE user_id=?", (uid,))
    active_files = sql.fetchone()[0]
    
    # حساب إجمالي الحجم
    total_size = 0
    if os.path.exists(user_dir):
        for filename in os.listdir(user_dir):
            filepath = os.path.join(user_dir, filename)
            total_size += os.path.getsize(filepath)
    
    stats_text = f"""
📊 **إحصائيات حسابك**

📁 **الملفات:** {total_files} ملف
⚡ **النشطة:** {active_files} ملف
💾 **المساحة:** {total_size // 1024} كيلوبايت
👤 **نوع الحساب:** {'🟢 مفعل' if check_user(uid)['approved'] else '🟡 قيد الانتظار'}
📅 **تاريخ التسجيل:** {datetime.now().strftime('%Y-%m-%d')}

🔧 **حدود الحساب:**
• 10 ملفات كحد أقصى
• 50 ميجابايت إجمالي
• تشغيل 24/7
    """
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main"))
    
    bot.edit_message_text(
        stats_text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )

def show_help(call):
    help_text = """
🆘 **مركز المساعدة**

📖 **كيفية الاستخدام:**
1️⃣ رفع السكربت (.py فقط)
2️⃣ انتظار موافقة المطور
3️⃣ تشغيل السكربت من 'إدارة الملفات'
4️⃣ متابعة الأداء

⚡ **مميزات الاستضافة:**
• تشغيل مستمر 24/7
• دعم فني مباشر
• مراقبة الأداء
• تحديثات تلقائية

⚠️ **ملاحظات هامة:**
• لا ترفع ملفات ضارة
• احترم سياسة الاستخدام
• تواصل مع المطور للمشاكل

📞 **الدعم الفني:** @Zeko12e
⏰ **الرد خلال:** 24 ساعة
    """
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📤 رفع سكربت", callback_data="upload"),
        types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")
    )
    
    bot.edit_message_text(
        help_text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )

# --- وظائف المطور (محسنة) ---
def show_pending_files(call):
    if call.from_user.id != ADMIN_ID:
        return bot.answer_callback_query(call.id, "❌ غير مسموح!", show_alert=True)
    
    sql.execute("SELECT COUNT(*) FROM pending_files")
    count = sql.fetchone()[0]
    
    if count == 0:
        bot.edit_message_text(
            "📭 **لا توجد طلبات في الانتظار**\n\n✨ كل شيء جاهز!",
            call.message.chat.id,
            call.message.message_id
        )
        return
    
    sql.execute("SELECT file_id, user_id, file_name, upload_time FROM pending_files ORDER BY upload_time")
    files = sql.fetchall()
    
    text = f"📋 **طلبات الرفع قيد الانتظار**\n\n📊 **العدد:** {count} طلب\n\n"
    
    for i, (file_id, user_id, file_name, upload_time) in enumerate(files, 1):
        text += f"{i}. 👤 `{user_id}` - 📄 `{file_name}`\n"
        text += f"   ⏰ {upload_time}\n\n"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 تحديث", callback_data="admin_pending"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )

def show_all_users(call):
    if call.from_user.id != ADMIN_ID:
        return bot.answer_callback_query(call.id, "❌ غير مسموح!", show_alert=True)
    
    sql.execute("SELECT id, approved, banned FROM users")
    users = sql.fetchall()
    
    text = "👥 **قائمة المستخدمين**\n\n"
    
    for user_id, approved, banned in users:
        status = "🟢 مفعل" if approved else "🟡 غير مفعل"
        if banned:
            status = "🔴 محظور"
        
        # حساب ملفات المستخدم
        user_dir = os.path.join(PROJECTS_DIR, str(user_id))
        file_count = len(os.listdir(user_dir)) if os.path.exists(user_dir) else 0
        
        text += f"👤 `{user_id}` - {status}\n"
        text += f"   📁 {file_count} ملف\n"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 تحديث", callback_data="admin_users"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )

def start_broadcast(call):
    if call.from_user.id != ADMIN_ID:
        return bot.answer_callback_query(call.id, "❌ غير مسموح!", show_alert=True)
    
    bot.edit_message_text(
        "📢 **نظام الإذاعة**\n\n✍️ أرسل الآن الرسالة التي تريد إذاعتها:",
        call.message.chat.id,
        call.message.message_id
    )
    
    msg = bot.send_message(call.message.chat.id, "📝 **اكتب الرسالة:**")
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    broadcast_text = message.text
    
    sql.execute("SELECT id FROM users WHERE banned=0")
    users = [u[0] for u in sql.fetchall()]
    
    bot.send_message(ADMIN_ID, f"📤 **جاري الإرسال لـ {len(users)} مستخدم...**")
    
    success = 0
    failed = 0
    
    for user_id in users:
        try:
            bot.send_message(user_id, f"📢 **إشعار من الإدارة:**\n\n{broadcast_text}")
            success += 1
            time.sleep(0.1)  # لتجنب حظر التليجرام
        except:
            failed += 1
    
    bot.send_message(
        ADMIN_ID,
        f"✅ **تمت الإذاعة**\n\n✅ الناجح: {success}\n❌ الفاشل: {failed}"
    )
    
    admin_menu(message)

def show_admin_stats(call):
    if call.from_user.id != ADMIN_ID:
        return bot.answer_callback_query(call.id, "❌ غير مسموح!", show_alert=True)
    
    # إحصائيات المستخدمين
    sql.execute("SELECT COUNT(*) FROM users")
    total_users = sql.fetchone()[0]
    
    sql.execute("SELECT COUNT(*) FROM users WHERE approved=1")
    active_users = sql.fetchone()[0]
    
    sql.execute("SELECT COUNT(*) FROM users WHERE banned=1")
    banned_users = sql.fetchone()[0]
    
    # إحصائيات الملفات
    total_files = 0
    active_files = 0
    
    for user_dir in os.listdir(PROJECTS_DIR):
        user_path = os.path.join(PROJECTS_DIR, user_dir)
        if os.path.isdir(user_path):
            total_files += len(os.listdir(user_path))
    
    sql.execute("SELECT COUNT(*) FROM files")
    active_files = sql.fetchone()[0]
    
    stats_text = f"""
📈 **إحصائيات النظام**

👥 **المستخدمين:**
• الإجمالي: {total_users}
• النشطين: {active_users}
• المحظورين: {banned_users}

📁 **الملفات:**
• المرفوعة: {total_files}
• النشطة: {active_files}
• في الانتظار: {len(os.listdir(PROJECTS_DIR))}

💾 **المساحة المستخدمة:** {sum(os.path.getsize(os.path.join(root, f)) for root, dirs, files in os.walk(PROJECTS_DIR) for f in files) // 1024} كيلوبايت

⏰ **وقت التشغيل:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 تحديث", callback_data="admin_stats"))
    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main"))
    
    bot.edit_message_text(
        stats_text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode="Markdown"
    )

# --- وظائف الموافقة والرفض ---
def view_pending_file(call):
    file_id = call.data.split("_", 2)[2]
    
    sql.execute("SELECT user_id, file_name, original_file_id FROM pending_files WHERE file_id=?", (file_id,))
    result = sql.fetchone()
    
    if not result:
        return bot.answer_callback_query(call.id, "❌ الملف غير موجود!", show_alert=True)
    
    user_id, file_name, original_file_id = result
    
    try:
        bot.send_document(
            ADMIN_ID,
            original_file_id,
            caption=f"📄 **معاينة الملف**\n\n👤 المستخدم: `{user_id}`\n📁 الاسم: `{file_name}`"
        )
        bot.answer_callback_query(call.id, "✅ تم إرسال الملف!")
    except:
        bot.answer_callback_query(call.id, "❌ فشل في إرسال الملف!", show_alert=True)

def accept_file(call):
    file_id = call.data.split("_", 1)[1]
    
    sql.execute("SELECT user_id, file_name, original_file_id FROM pending_files WHERE file_id=?", (file_id,))
    result = sql.fetchone()
    
    if not result:
        return bot.answer_callback_query(call.id, "❌ الملف غير موجود!", show_alert=True)
    
    user_id, file_name, original_file_id = result
    
    try:
        # تحميل الملف
        file_info = bot.get_file(original_file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        # حفظ الملف
        user_dir = os.path.join(PROJECTS_DIR, str(user_id))
        os.makedirs(user_dir, exist_ok=True)
        
        file_path = os.path.join(user_dir, file_name)
        with open(file_path, 'wb') as f:
            f.write(downloaded)
        
        # حذف من قائمة الانتظار
        sql.execute("DELETE FROM pending_files WHERE file_id=?", (file_id,))
        db.commit()
        
        # إرسال إشعار للمستخدم
        bot.send_message(
            user_id,
            f"🎉 **تم قبول ملفك!**\n\n📄 `{file_name}`\n✅ تمت الموافقة عليه.\n🚀 يمكنك الآن تشغيله من 'إدارة الملفات'."
        )
        
        # إرسال إشعار للمطور
        bot.answer_callback_query(call.id, "✅ تم قبول الملف!", show_alert=True)
        
        # تحديث الرسالة
        bot.edit_message_text(
            f"✅ **تمت الموافقة**\n\n👤 المستخدم: `{user_id}`\n📄 الملف: `{file_name}`\n🕐 الوقت: {datetime.now().strftime('%H:%M:%S')}",
            call.message.chat.id,
            call.message.message_id
        )
        
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ خطأ: {str(e)[:100]}", show_alert=True)

def reject_file(call):
    file_id = call.data.split("_", 1)[1]
    
    sql.execute("SELECT user_id, file_name FROM pending_files WHERE file_id=?", (file_id,))
    result = sql.fetchone()
    
    if not result:
        return bot.answer_callback_query(call.id, "❌ الملف غير موجود!", show_alert=True)
    
    user_id, file_name = result
    
    # حذف من قائمة الانتظار
    sql.execute("DELETE FROM pending_files WHERE file_id=?", (file_id,))
    db.commit()
    
    # إرسال إشعار للمستخدم
    bot.send_message(
        user_id,
        f"❌ **تم رفض ملفك**\n\n📄 `{file_name}`\n⚠️ لم يتم قبوله.\n📞 للاستفسار: @Zeko12e"
    )
    
    bot.answer_callback_query(call.id, "✅ تم رفض الملف!", show_alert=True)
    
    # تحديث الرسالة
    bot.edit_message_text(
        f"❌ **تم الرفض**\n\n👤 المستخدم: `{user_id}`\n📄 الملف: `{file_name}`\n🕐 الوقت: {datetime.now().strftime('%H:%M:%S')}",
        call.message.chat.id,
        call.message.message_id
    )

def show_user_info(call):
    user_id = call.data.split("_", 2)[2]
    
    sql.execute("SELECT approved, banned FROM users WHERE id=?", (user_id,))
    result = sql.fetchone()
    
    if not result:
        return bot.answer_callback_query(call.id, "❌ المستخدم غير موجود!", show_alert=True)
    
    approved, banned = result
    
    # حساب ملفات المستخدم
    user_dir = os.path.join(PROJECTS_DIR, str(user_id))
    file_count = len(os.listdir(user_dir)) if os.path.exists(user_dir) else 0
    
    # حساب الملفات النشطة
    sql.execute("SELECT COUNT(*) FROM files WHERE user_id=?", (user_id,))
    active_count = sql.fetchone()[0]
    
    info_text = f"""
👤 **معلومات المستخدم**

🆔 **الأيدي:** `{user_id}`
📅 **الحالة:** {'🟢 مفعل' if approved else '🟡 غير مفعل'}
🚫 **الحظر:** {'نعم' if banned else 'لا'}
📁 **الملفات:** {file_count}
⚡ **النشطة:** {active_count}
    """
    
    bot.answer_callback_query(call.id, info_text, show_alert=True)

def activate_user(call):
    user_id = call.data.split("_", 1)[1]
    
    sql.execute("UPDATE users SET approved=1, banned=0 WHERE id=?", (user_id,))
    db.commit()
    
    bot.send_message(
        user_id,
        "🎉 **مبروك!**\n\n✅ تم تفعيل حسابك بنجاح.\n🚀 يمكنك الآن استخدام جميع ميزات الاستضافة."
    )
    
    bot.answer_callback_query(call.id, f"✅ تم تفعيل المستخدم {user_id}!", show_alert=True)
    
    bot.edit_message_text(
        f"✅ **تم التفعيل**\n\n👤 المستخدم: `{user_id}`\n🕐 الوقت: {datetime.now().strftime('%H:%M:%S')}",
        call.message.chat.id,
        call.message.message_id
    )

# --- أوامر إضافية ---
@bot.message_handler(commands=['help'])
def help_command(message):
    show_help_message = """
🤖 **أوامر البوت:**

/start - بدء استخدام البوت
/help - عرض المساعدة
/stats - إحصائيات حسابك

🔧 **للمطور فقط:**
/send - إرسال إشعار للمستخدمين
/add - تفعيل مستخدم
/ban - حظر مستخدم

📞 **الدعم:** @Zeko12e
    """
    
    bot.send_message(message.chat.id, show_help_message)

@bot.message_handler(commands=['add'])
def add_user(message):
    if message.from_user.id != ADMIN_ID:
        return bot.send_message(message.chat.id, "❌ هذا الأمر للمطور فقط!")
    
    try:
        user_id = int(message.text.split()[1])
        sql.execute("UPDATE users SET approved=1, banned=0 WHERE id=?", (user_id,))
        db.commit()
        
        bot.send_message(message.chat.id, f"✅ تم تفعيل المستخدم `{user_id}`")
        bot.send_message(user_id, "🎉 **مبروك!**\n\nتم تفعيل حسابك بنجاح.")
    except:
        bot.send_message(message.chat.id, "⚠️ استخدم: `/add [ID]`", parse_mode="Markdown")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id != ADMIN_ID:
        return bot.send_message(message.chat.id, "❌ هذا الأمر للمطور فقط!")
    
    try:
        user_id = int(message.text.split()[1])
        sql.execute("UPDATE users SET banned=1 WHERE id=?", (user_id,))
        db.commit()
        
        bot.send_message(message.chat.id, f"🚫 تم حظر المستخدم `{user_id}`")
        bot.send_message(user_id, "❌ **تم حظر حسابك**\n\nللاستفسار: @Zeko12e")
    except:
        bot.send_message(message.chat.id, "⚠️ استخدم: `/ban [ID]`", parse_mode="Markdown")

@bot.message_handler(commands=['send'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return bot.send_message(message.chat.id, "❌ هذا الأمر للمطور فقط!")
    
    try:
        text = message.text.split(None, 1)[1]
        
        sql.execute("SELECT id FROM users WHERE banned=0")
        users = [u[0] for u in sql.fetchall()]
        
        success = 0
        for user_id in users:
            try:
                bot.send_message(user_id, f"📢 **إعلان:**\n\n{text}")
                success += 1
                time.sleep(0.1)
            except:
                continue
        
        bot.send_message(message.chat.id, f"✅ تم الإرسال لـ {success} مستخدم")
    except:
        bot.send_message(message.chat.id, "⚠️ استخدم: `/send [نص]`", parse_mode="Markdown")

# --- تشغيل البوت ---
if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Ziko Hosting Bot Started Successfully")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👑 Admin ID: {ADMIN_ID}")
    print("=" * 50)
    
    bot.infinity_polling()