import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = 'توكنك ي حب ⚔️'
ADMIN_ID = 8285783377  # الـ ID الخاص بك

# قاعدة بيانات بأسماء السور وأرقام صفحاتها
SURAH_PAGES = {
    "الفاتحة": 1, "البقرة": 2, "آل عمران": 50, "النساء": 77, "المائدة": 106,
    "الأنعام": 128, "الأعراف": 151, "الأنفال": 177, "التوبة": 187, "يونس": 208,
    "هود": 221, "يوسف": 235, "الرعد": 249, "إبراهيم": 255, "الحجر": 262,
    "النحل": 267, "الإسراء": 282, "الكهف": 293, "مريم": 305, "طه": 312,
    "الأنبياء": 322, "الحج": 332, "المؤمنون": 342, "النور": 350, "الفرقان": 359,
    "يس": 440, "الواقعة": 534, "الملك": 562, "النبأ": 582, "الإخلاص": 604, "الناس": 604
}

# --- وظائف قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

# --- لوحات التحكم ---
def get_nav_keyboard(page):
    buttons = []
    if page < 604: buttons.append(InlineKeyboardButton("التالي ⬅️", callback_data=f"p_{page+1}"))
    if page > 1: buttons.append(InlineKeyboardButton("➡️ السابق", callback_data=f"p_{page-1}"))
    return InlineKeyboardMarkup([buttons])

# لوحة أزرار المطور والقناة
def developer_buttons():
    keyboard = [
        [
            InlineKeyboardButton("👨‍💻 المطور", url="https://t.me/Zeko12e"),
            InlineKeyboardButton("📢 قناة المطور", url="https://t.me/zeko_1123")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(update.effective_user.id)
    await update.message.reply_text(
        "مرحباً بك يا زيكو 📖\n\n"
        "• ابحث برقم الصفحة (1-604)\n"
        "• أو اكتب اسم السورة (مثال: الكهف)\n"
        "• للمشرف: /stats لمعرفة الإحصائيات",
        reply_markup=developer_buttons()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text.isdigit():
        page = int(text)
        if 1 <= page <= 604:
            url = f"https://quran.ksu.edu.sa/png_big/{page}.png"
            await update.message.reply_photo(photo=url, caption=f"صفحة: {page}", reply_markup=get_nav_keyboard(page))
        else:
            await update.message.reply_text("يرجى إرسال رقم بين 1 و 604.")
        return

    if text in SURAH_PAGES:
        page = SURAH_PAGES[text]
        url = f"https://quran.ksu.edu.sa/png_big/{page}.png"
        await update.message.reply_photo(photo=url, caption=f"بداية سورة {text} - صفحة {page}", reply_markup=get_nav_keyboard(page))
    else:
        await update.message.reply_text("عذراً، لم أتعرف على اسم السورة.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    page = int(query.data.split("_")[1])
    
    url = f"https://quran.ksu.edu.sa/png_big/{page}.png"
    await query.edit_message_media(
        media=InputMediaPhoto(media=url, caption=f"صفحة: {page}"),
        reply_markup=get_nav_keyboard(page)
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    conn = sqlite3.connect('users.db')
    count = conn.cursor().execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    await update.message.reply_text(f"📊 إجمالي عدد مستخدمي البوت: {count}")

def main():
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("البوت شغال ي حب 💤")
    app.run_polling()

if __name__ == '__main__': main()
