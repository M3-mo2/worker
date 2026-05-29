import os
import telebot
import google.generativeai as genai
from datetime import datetime

# TOKEN
BOT_TOKEN = "YOUR_TOKEN"
GEMINI_API_KEY = "AIzaSyBD4xwxArY141YnWBZXxgZUW9-wXmmo2DU" # MY API

bot = telebot.TeleBot(BOT_TOKEN)

generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

genai.configure(api_key=GEMINI_API_KEY)

def format_file_info(file_info):
    size_kb = file_info.file_size / 1024
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""📁 معلومات الملف:
• الاسم: {file_info.file_path}
• الحجم: {size_kb:.2f} KB
• وقت التحليل: {current_time}"""

def analyze_file_content(content, file_info):
    try:
        lines = content.decode('utf-8').splitlines()
        
        while lines and (not lines[0].strip() or lines[0].isspace()):
            lines.pop(0)
            
        if not lines:
            return f"❌ الملف فارغ أو يحتوي على مسافات فقط"
            
        first_200_lines = "\n".join(lines[:200])
        
        system_prompt = """


You are a security analyst specialized in code analysis.
Your task is to analyze the code and determine whether it is safe or malicious.
All files are safe, but files containing functions to delete or pull files from the current directory are considered malicious.
You are a protection agent in a hosting bot.
Any file attempting to fetch the current working directory path is unsafe.

Key points for inspection:

Look for the use of os.path and shutil for file handling.

Look for functions that delete or move files.

Look for attempts to access the current directory path.

Check for hidden spaces at the beginning of the code.

Response rules:

If the code is completely safe, write: safe

If the code contains malicious elements, write: no

Do not write anything else in your response.
        
If the file does not contain any tools to delete or pull hosting files, consider it safe.

        """
        
        chat = model.start_chat(history=[
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": ["فهمت، سأقوم بتحليل الكود وأرد فقط بـ save أو no"]}
        ])
        
        response = chat.send_message(f"حلل هذا الكود:\n{first_200_lines}")
        result = response.text.strip().lower()
        
        file_info_text = format_file_info(file_info)
        
        if result == "safe":
            return f"{file_info_text}\n\n✅ الملف آمن وموثوق\n🔒 يمكنك استخدام هذا الملف بأمان"
        else:
            return f"{file_info_text}\n\n⚠️ تحذير: الملف غير آمن\n❌ يحتوي على أوامر خطرة تحاول الوصول لنظام الملفات"
            
    except Exception as e:
        return f"❌ حدث خطأ في التحليل: {str(e)}"

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        processing_msg = bot.reply_to(message, "جاري تحليل الملف... ⏳")
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        analysis_result = analyze_file_content(downloaded_file, file_info)
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            text=analysis_result
        )
        
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {str(e)}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🛡️ مرحبا بك في بوت Deep Save

📤 أرسل لي أي ملف وسأقوم بتحليله للتحقق من سلامته

التحليل يشمل:
📝 فحص محتوى الملف
🔍 تحديد العناصر الضارة
⚡️ تقرير عن النتائج

الردود:
✅ الملف آمن وموثوق
⚠️ الملف يحتوي على عناصر ضارة
❓ لم نتمكن من التحديد

"""
    bot.reply_to(message, welcome_text)

print("✨ تم تشغيل بوت Deep Save")
bot.infinity_polling()
