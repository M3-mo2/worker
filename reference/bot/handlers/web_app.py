import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telethon import events
import traceback
import json
import hmac
import hashlib
import time
import urllib.parse

# استدعاءاتك الأساسية
from bot.core.client import client
from bot.core.config import settings

# استخدام التوكن من الإعدادات المركزية
BOT_TOKEN = settings.telegram.BOT_TOKEN
tb = telebot.TeleBot(BOT_TOKEN)

def generate_auth_url(user_id, first_name, username=None):
    """
    إنشاء رابط ويب أب مع بيانات مصادقة صحيحة (tgWebAppData) 
    ليعمل في التليجرام أو في المتصفح الخارجي
    """
    # استخدام الرابط من الإعدادات
    base_url = settings.web.WEBAPP_URL
    
    # 1. تجهيز بيانات المستخدم
    user_data = {
        "id": user_id,
        "first_name": first_name,
        "username": username or "",
        "language_code": "ar"
    }
    
    auth_date = int(time.time())
    
    # 2. تجهيز الـ Data Check String (يجب أن يكون مرتباً أبجدياً في تليجرام)
    data = {
        "auth_date": str(auth_date),
        "user": json.dumps(user_data, separators=(',', ':'))
    }
    
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items())])
    
    # 3. حساب الهاش بنفس طريقة تليجرام باستخدام التوكن
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    hash_value = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    # 4. بناء الـ Query Params
    params = {
        "auth_date": data["auth_date"],
        "user": data["user"],
        "hash": hash_value
    }
    
    query_string = urllib.parse.urlencode(params)
    return f"{base_url}?user_id={user_id}&tgWebAppData={urllib.parse.quote(query_string)}"

async def send_webapp_link(event):
    """
    معالج أمر /web - يرسل رابط لوحة التحكم للمستخدم
    """
    chat_id = event.chat_id
    
    try:
        # الحصول على بيانات المستخدم من الحدث
        user = await event.get_sender()
        
        # إنشاء الرابط ديناميكياً
        webapp_url = generate_auth_url(user.id, user.first_name, getattr(user, 'username', None))
        
        message_text = (
            "🔐 *لوحة التحكم (Mini App)*\n\n"
            "اضغط على الزر أدناه لفتح لوحة التحكم.\n"
            "يعمل هذا الرابط داخل تليجرام أو في المتصفح الخارجي.\n"
        )
        
        # تجهيز الكيبورد
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                text="🌐 لوحة الويب", 
                web_app=WebAppInfo(url=webapp_url)
            )
        )
        
        # إرسال الرسالة
        tb.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=markup,
            parse_mode="Markdown"
        )
        
    except Exception as e:
        print(f"Error in web_app handler: {e}")
        traceback.print_exc()
        await event.respond(f"❌ حدث خطأ أثناء إنشاء الرابط. يرجى المحاولة لاحقاً.")


def setup(client_instance):
    """Register /web command handler."""
    client_instance.on(events.NewMessage(pattern=r"^/web$"))(send_webapp_link)
    print("✅ WebApp /web handler registered.")