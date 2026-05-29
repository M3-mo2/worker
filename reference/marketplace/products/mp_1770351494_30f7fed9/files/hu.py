import os
import json
import logging
import asyncio
import aiohttp
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from urllib.parse import quote_plus
import io
import mimetypes
import random
import string
import time
import re
import traceback
import shutil

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from telegram.constants import ParseMode

# ============================================
# RedFox Code - إعدادات البوت
# ============================================
BOT_TOKEN = "TOKEN_HERE"
ADMIN_IDS = []
DATABASE_FILE = "redfox_bot.db"
LOG_FILE = "redfox_bot.log"
SUPPORT_USERNAME = "@xgv2z"
BOT_USERNAME = "@RedFoxbot"

# ============================================
# RedFox Code - تنسيقات تلجرام
# ============================================
class TelegramFormatter:
    @staticmethod
    def bold(text: str) -> str:
        return f"*{text}*"
    
    @staticmethod
    def italic(text: str) -> str:
        return f"_{text}_"
    
    @staticmethod
    def code(text: str) -> str:
        return f"`{text}`"
    
    @staticmethod
    def pre(text: str) -> str:
        return f"```{text}```"
    
    @staticmethod
    def link(text: str, url: str) -> str:
        return f"[{text}]({url})"
    
    @staticmethod
    def section_header(text: str) -> str:
        return f"━━━━━━━━━━━━━━━━━━━━\n🔹 *{text}* 🔹\n━━━━━━━━━━━━━━━━━━━━"
    
    @staticmethod
    def list_item(text: str) -> str:
        return f"• {text}"
    
    @staticmethod
    def success(text: str) -> str:
        return f"✅ {text}"
    
    @staticmethod
    def error(text: str) -> str:
        return f"❌ {text}"
    
    @staticmethod
    def warning(text: str) -> str:
        return f"⚠️ {text}"
    
    @staticmethod
    def info(text: str) -> str:
        return f"ℹ️ {text}"
    
    @staticmethod
    def format_welcome(user_name: str, stats: dict, is_vip: bool = False) -> str:
        vip_status = "✨ *مستخدم VIP*" if is_vip else "👤 *مستخدم عادي*"
        return f"""🎉 *مرحباً {user_name}!* 🎉

🤖 *RedFox Bot* - بوت متطور متعدد الوظائف

{vip_status}

✨ *جميع الخدمات مجانية!* ✨
🚀 *ما عدا خدمة Python Hosting VIP*

📊 *إحصائيات البوت:*
👥 المستخدمين: {stats['total_users']:,}
📥 الطلبات: {stats['total_requests']:,}

🔍 *اختر من الأزرار أدناه للبدء:*"""
    
    @staticmethod
    def format_subscription_info(subscription_data: dict) -> str:
        return f"""👑 *معلومات الاشتراك VIP*

✨ *الحالة:* ✅ نشط
⏰ *المدة:* {subscription_data['days']} يوم
📅 *تاريخ البدء:* {subscription_data['start_date']}
📅 *تاريخ الانتهاء:* {subscription_data['end_date']}
🎫 *كود الاشتراك:* `{subscription_data['code']}`

💎 *المميزات المتاحة:*
• 🚀 Python Hosting VIP
• ⚡ أولوية في الخدمات
• 📞 دعم فني مميز"""
    
    @staticmethod
    def format_force_subscription(channels: list, user_status: dict) -> str:
        text = "⚠️ *يجب الاشتراك في القنوات التالية:*\n\n"
        for channel in channels:
            channel_id = channel['channel_id']
            channel_name = channel['channel_name']
            status = user_status.get(channel_id, False)
            status_icon = "✅" if status else "❌"
            text += f"{status_icon} {channel_name}\n"
        text += "\n🔍 *بعد الاشتراك، اضغط على زر التحقق*"
        return text

    @staticmethod
    def format_service_intro(service_name: str, description: str, example: str) -> str:
        return f"""🔹 *{service_name}* 🔹

{description}

✨ *مجاناً تماماً!* ✨

📝 *أرسل البيانات المطلوبة:*
{example}

⏳ *سأقوم بمعالجة طلبك فوراً*"""
    
    @staticmethod
    def format_request_code(request_code: str, service_name: str, request_data: str):
        clean_data = str(request_data)
        markdown_chars = ['*', '_', '`', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.']
        for char in markdown_chars:
            clean_data = clean_data.replace(char, ' ')
        clean_data = ' '.join(clean_data.split())
        if len(clean_data) > 80:
            clean_data = clean_data[:80] + "..."
        return f"""✅ *تم استلام طلبك بنجاح!*

🎫 *كود الطلب:* `{request_code}`
🛠 *الخدمة:* {service_name}
📝 *الطلب:* {clean_data}

⏳ *جاري معالجة طلبك...*
سيتم إعلامك عند اكتمال المعالجة."""

fmt = TelegramFormatter()

# ============================================
# RedFox Code - قاعدة البيانات
# ============================================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            join_date TIMESTAMP,
            request_count INTEGER DEFAULT 0,
            current_action TEXT DEFAULT NULL,
            is_vip BOOLEAN DEFAULT 0,
            vip_start_date TIMESTAMP,
            vip_end_date TIMESTAMP,
            vip_code TEXT DEFAULT NULL)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_code TEXT,
            user_id INTEGER,
            api_name TEXT,
            request_data TEXT,
            response_data TEXT,
            status TEXT DEFAULT 'pending',
            timestamp TIMESTAMP)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY,
            added_by INTEGER,
            added_date TIMESTAMP)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS vip_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            created_by INTEGER,
            created_date TIMESTAMP,
            used_by INTEGER DEFAULT NULL,
            used_date TIMESTAMP DEFAULT NULL,
            is_used BOOLEAN DEFAULT 0)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS force_sub_channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT UNIQUE,
            channel_name TEXT,
            added_by INTEGER,
            added_date TIMESTAMP,
            is_active BOOLEAN DEFAULT 1)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS bot_settings (
            setting_key TEXT PRIMARY KEY,
            setting_value TEXT)''')
        
        if ADMIN_IDS:
            for admin_id in ADMIN_IDS:
                cursor.execute('''INSERT OR IGNORE INTO admins (user_id, added_by, added_date)
                    VALUES (?, ?, ?)''', (admin_id, 0, datetime.now()))
        
        cursor.execute('''INSERT OR IGNORE INTO bot_settings (setting_key, setting_value)
            VALUES ('bot_active', '1')''')
        
        cursor.execute('''INSERT OR IGNORE INTO bot_settings (setting_key, setting_value)
            VALUES ('force_sub_enabled', '0')''')
        
        self.conn.commit()
    
    def add_user(self, user_id: int, username: str, first_name: str, last_name: str = ""):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, join_date)
            VALUES (?, ?, ?, ?, ?)''', (user_id, username, first_name, last_name, datetime.now()))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_user(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()
    
    def is_vip(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('SELECT is_vip, vip_end_date FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        if result and result[0] == 1:
            vip_end_date = result[1]
            if vip_end_date and datetime.strptime(vip_end_date, '%Y-%m-%d %H:%M:%S.%f') > datetime.now():
                return True
            else:
                self.remove_vip(user_id)
        return False
    
    def set_vip(self, user_id: int, vip_code: str, days: int = 30):
        cursor = self.conn.cursor()
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days)
        cursor.execute('''UPDATE users SET 
            is_vip = 1,
            vip_start_date = ?,
            vip_end_date = ?,
            vip_code = ?
            WHERE user_id = ?''', (start_date, end_date, vip_code, user_id))
        self.conn.commit()
        return True
    
    def remove_vip(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE users SET 
            is_vip = 0,
            vip_start_date = NULL,
            vip_end_date = NULL,
            vip_code = NULL
            WHERE user_id = ?''', (user_id,))
        self.conn.commit()
        return True
    
    def get_vip_info(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT vip_start_date, vip_end_date, vip_code 
            FROM users WHERE user_id = ? AND is_vip = 1''', (user_id,))
        result = cursor.fetchone()
        if result:
            return {'start_date': result[0], 'end_date': result[1], 'code': result[2], 'days': 30}
        return None
    
    def set_user_action(self, user_id: int, action: str):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET current_action = ? WHERE user_id = ?', (action, user_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_user_action(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('SELECT current_action FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def clear_user_action(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET current_action = NULL WHERE user_id = ?', (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def add_request(self, user_id: int, api_name: str, request_data: str, response_data: str = ""):
        cursor = self.conn.cursor()
        request_code = f"REQ{random.randint(10000, 99999)}"
        clean_request_data = str(request_data)
        markdown_chars = ['*', '_', '`', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.']
        for char in markdown_chars:
            clean_request_data = clean_request_data.replace(char, ' ')
        clean_request_data = ' '.join(clean_request_data.split())
        cursor.execute('''INSERT INTO requests (request_code, user_id, api_name, request_data, response_data, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)''', (request_code, user_id, api_name, clean_request_data[:500], response_data[:500], datetime.now()))
        self.conn.commit()
        return request_code
    
    def increment_request_count(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE users SET request_count = request_count + 1 WHERE user_id = ?', (user_id,))
        self.conn.commit()
    
    def search_request(self, search_term: str):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT r.*, u.username, u.first_name 
            FROM requests r LEFT JOIN users u ON r.user_id = u.user_id 
            WHERE r.request_code LIKE ? OR r.user_id = ?
            ORDER BY r.timestamp DESC LIMIT 10''', (f'%{search_term}%', search_term if search_term.isdigit() else 0))
        return cursor.fetchall()
    
    def update_request_status(self, request_code: str, status: str):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE requests SET status = ? WHERE request_code = ?', (status, request_code))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def is_admin(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('SELECT 1 FROM admins WHERE user_id = ?', (user_id,))
        return cursor.fetchone() is not None
    
    def add_admin(self, user_id: int, added_by: int):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO admins (user_id, added_by, added_date) VALUES (?, ?, ?)', 
                      (user_id, added_by, datetime.now()))
        self.conn.commit()
        return True
    
    def remove_admin(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_admins(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM admins ORDER BY added_date DESC')
        return cursor.fetchall()
    
    def create_vip_code(self, created_by: int):
        cursor = self.conn.cursor()
        code = f"RedFoxBot{random.randint(100000, 999999)}"
        cursor.execute('INSERT INTO vip_codes (code, created_by, created_date) VALUES (?, ?, ?)', 
                      (code, created_by, datetime.now()))
        self.conn.commit()
        return code
    
    def use_vip_code(self, code: str, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, is_used FROM vip_codes WHERE code = ?', (code,))
        result = cursor.fetchone()
        if not result:
            return False, "❌ *كود التفعيل غير صحيح!*"
        code_id, is_used = result
        if is_used:
            return False, "❌ *كود التفعيل مستخدم من قبل!*"
        cursor.execute('''UPDATE vip_codes SET 
            used_by = ?, used_date = ?, is_used = 1 WHERE id = ?''', (user_id, datetime.now(), code_id))
        self.set_vip(user_id, code)
        self.conn.commit()
        return True, f"✅ *تم تفعيل الاشتراك VIP بنجاح!*\n⏰ *المدة:* 30 يوم\n🎫 *الكود:* `{code}`"
    
    def get_vip_codes(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vip_codes ORDER BY created_date DESC')
        return cursor.fetchall()
    
    def add_force_sub_channel(self, channel_id: str, channel_name: str, added_by: int):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO force_sub_channels 
            (channel_id, channel_name, added_by, added_date) VALUES (?, ?, ?, ?)''', 
            (channel_id, channel_name, added_by, datetime.now()))
        self.conn.commit()
        return True
    
    def remove_force_sub_channel(self, channel_id: str):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM force_sub_channels WHERE channel_id = ?', (channel_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_force_sub_channels(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM force_sub_channels WHERE is_active = 1 ORDER BY added_date DESC')
        return cursor.fetchall()
    
    def get_setting(self, key: str, default: str = ""):
        cursor = self.conn.cursor()
        cursor.execute('SELECT setting_value FROM bot_settings WHERE setting_key = ?', (key,))
        result = cursor.fetchone()
        return result[0] if result else default
    
    def set_setting(self, key: str, value: str):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO bot_settings (setting_key, setting_value) VALUES (?, ?)', (key, value))
        self.conn.commit()
        return True
    
    def is_bot_active(self):
        return self.get_setting('bot_active', '1') == '1'
    
    def set_bot_active(self, active: bool):
        return self.set_setting('bot_active', '1' if active else '0')
    
    def is_force_sub_enabled(self):
        return self.get_setting('force_sub_enabled', '0') == '1'
    
    def set_force_sub_enabled(self, enabled: bool):
        return self.set_setting('force_sub_enabled', '1' if enabled else '0')
    
    def get_statistics(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM requests')
        total_requests = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_vip = 1')
        vip_users = cursor.fetchone()[0]
        return {'total_users': total_users, 'total_requests': total_requests, 'vip_users': vip_users}
    
    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY join_date DESC')
        return cursor.fetchall()
    
    def get_recent_requests(self, limit: int = 10):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT r.*, u.username, u.first_name 
            FROM requests r LEFT JOIN users u ON r.user_id = u.user_id 
            ORDER BY r.timestamp DESC LIMIT ?''', (limit,))
        return cursor.fetchall()

db = Database()

# ============================================
# RedFox Code - قائمة الخدمات
# ============================================
SERVICES = {
    "tiktok_dl": {
        "name": "🎥 TikTok Downloader",
        "description": "تحميل فيديوهات TikTok بدون علامة مائية",
        "example": "🔗 *أرسل رابط فيديو TikTok*\nمثال: https://vm.tiktok.com/ZSabcdefg/",
        "handler": "tiktok"
    },
    "spotify_dl": {
        "name": "🎵 Spotify Downloader",
        "description": "تحميل أغاني Spotify بجودة عالية",
        "example": "🔗 *أرسل رابط أغنية Spotify*\nمثال: https://open.spotify.com/track/...",
        "handler": "spotify"
    },
    "microsoft_tts": {
        "name": "🔊 Microsoft TTS",
        "description": "تحويل النص إلى كلام باستخدام Microsoft",
        "example": "📝 *أرسل النص الذي تريد تحويله لصوت*\nمثال: مرحبا بك في بوت ريدفوكس",
        "handler": "tts"
    },
    "openai_tts": {
        "name": "🤖 OpenAI TTS",
        "description": "تحويل النص إلى كلام باستخدام الذكاء الاصطناعي",
        "example": "📝 *أرسل النص الذي تريد تحويله لصوت*\nمثال: هذا صوت من الذكاء الاصطناعي",
        "handler": "tts"
    },
    "ai_chat_multi": {
        "name": "💬 AI Chat Multi-Model",
        "description": "محادثة ذكية مع نماذج متعددة للذكاء الاصطناعي",
        "example": "💭 *أرسل استفسارك أو سؤالك*\nمثال: ما هي عاصمة فرنسا؟",
        "handler": "chat"
    },
    "chatgpt": {
        "name": "🧠 ChatGPT API",
        "description": "محادثة مع ChatGPT من OpenAI",
        "example": "💭 *أرسل استفسارك أو سؤالك*\nمثال: اشرح لي نظرية النسبية",
        "handler": "chat"
    },
    "pdf_to_text": {
        "name": "📄 PDF to Text",
        "description": "استخراج النصوص من ملفات PDF",
        "example": "📎 *أرسل ملف PDF*\n(سيتم استخراج النص منه)",
        "handler": "file"
    },
    "yt_summarizer": {
        "name": "📺 YouTube Summarizer",
        "description": "تلخيص فيديوهات YouTube تلقائياً",
        "example": "🔗 *أرسل رابط فيديو YouTube*\nمثال: https://youtube.com/watch?v=...",
        "handler": "youtube"
    },
    "ai_image": {
        "name": "🎨 AI Image Generator",
        "description": "إنشاء صور باستخدام الذكاء الاصطناعي",
        "example": "🎨 *أرسل وصف للصورة التي تريدها*\nمثال: منظر غروب الشمس على البحر",
        "handler": "image"
    },
    "yt_transcript": {
        "name": "📝 YouTube Transcript",
        "description": "استخراج النصوص من فيديوهات YouTube",
        "example": "🔗 *أرسل رابط فيديو YouTube*\nمثال: https://youtube.com/watch?v=...",
        "handler": "youtube"
    },
    "link_shortener": {
        "name": "🔗 Link Shortener",
        "description": "تقصير الروابط الطويلة",
        "example": "🔗 *أرسل الرابط الطويل*\nمثال: https://example.com/very-long-url...",
        "handler": "link"
    },
    "tiktok_tts": {
        "name": "🗣️ TikTok TTS",
        "description": "تحويل النص إلى صوت TikTok الشهير",
        "example": "📝 *أرسل النص الذي تريد تحويله*\nمثال: هذا صوت تيك توك",
        "handler": "tts"
    },
    "google_tts": {
        "name": "📢 Google TTS",
        "description": "تحويل النص إلى كلام باستخدام Google",
        "example": "📝 *أرسل النص الذي تريد تحويله*\nمثال: هذا صوت جوجل",
        "handler": "tts"
    },
    "loquendo_tts": {
        "name": "🎙️ Loquendo TTS",
        "description": "تحويل النص إلى كلام باستخدام Loquendo",
        "example": "📝 *أرسل النص الذي تريد تحويله*\nمثال: هذا صوت لوكيندو",
        "handler": "tts"
    },
    "hashtag_gen": {
        "name": "🏷️ Hashtag Generator",
        "description": "إنشاء هاشتاجات لمنشوراتك",
        "example": "📝 *أرسل وصف منشورك*\nمثال: منشور عن السياحة في دبي",
        "handler": "text"
    },
    "translator": {
        "name": "🌐 Translator",
        "description": "ترجمة النصوص بين اللغات",
        "example": "📝 *أرسل النص للترجمة*\nمثال: Hello, how are you?",
        "handler": "text"
    },
    "radio": {
        "name": "📻 Radio Stations",
        "description": "البث المباشر لمحطات الراديو",
        "example": "📻 *اختر محطة راديو من القائمة*",
        "handler": "radio"
    },
    "openai_tts_converter": {
        "name": "🔊 OpenAI TTS Converter",
        "description": "تحويل النص إلى صوت متقدم",
        "example": "📝 *أرسل النص الذي تريد تحويله*\nمثال: هذا صوت متقدم من الذكاء الاصطناعي",
        "handler": "tts"
    },
    "weather": {
        "name": "🌤️ Weather",
        "description": "الحصول على معلومات الطقس لأي مدينة",
        "example": "📍 *أرسل اسم المدينة*\nمثال: الرياض، دبي، لندن",
        "handler": "weather"
    },
    "python_hosting": {
        "name": "🚀 Python Hosting (VIP)",
        "description": "استضافة ملفات بايثون على السيرفر (للمشتركين VIP فقط)",
        "example": "📁 *أرسل ملف Python*\n(للمشتركين VIP فقط)",
        "handler": "file",
        "vip_only": True
    }
}

# ============================================
# RedFox Code - وظائف المساعدة
# ============================================
def create_main_keyboard():
    keyboard = []
    row = []
    services_list = list(SERVICES.items())
    for i, (key, service) in enumerate(services_list, 1):
        row.append(InlineKeyboardButton(service["name"], callback_data=key))
        if i % 2 == 0 or i == len(services_list):
            keyboard.append(row)
            row = []
    keyboard.append([
        InlineKeyboardButton("👑 قسم VIP", callback_data="vip_section"),
        InlineKeyboardButton("🎫 تفعيل اشتراك", callback_data="activate_subscription")
    ])
    keyboard.append([
        InlineKeyboardButton("ℹ️ About", callback_data="about"),
        InlineKeyboardButton("👨‍💻 Support", callback_data="support")
    ])
    keyboard.append([InlineKeyboardButton("🛠 لوحة التحكم", callback_data="admin_panel")])
    return InlineKeyboardMarkup(keyboard)

def create_admin_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")],
        [InlineKeyboardButton("👥 إدارة المستخدمين", callback_data="admin_users")],
        [InlineKeyboardButton("📋 عرض الطلبات", callback_data="admin_requests")],
        [InlineKeyboardButton("🔍 البحث عن طلب", callback_data="admin_search")],
        [InlineKeyboardButton("🎫 إنشاء كود اشتراك", callback_data="create_sub_code")],
        [InlineKeyboardButton("📢 إرسال إذاعة", callback_data="admin_broadcast")],
        [InlineKeyboardButton("👑 إدارة الأدمن", callback_data="manage_admins")],
        [InlineKeyboardButton("📢 إدارة القنوات", callback_data="manage_channels")],
        [InlineKeyboardButton("⚙️ إعدادات البوت", callback_data="bot_settings")],
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_menu")]
    ])

async def check_force_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not db.is_force_sub_enabled():
        return True
    user_id = update.effective_user.id
    channels = db.get_force_sub_channels()
    if not channels:
        return True
    user_status = {}
    all_subscribed = True
    for channel in channels:
        channel_id = channel[1]
        try:
            chat_member = await context.bot.get_chat_member(channel_id, user_id)
            is_subscribed = chat_member.status not in ['left', 'kicked']
            user_status[channel_id] = is_subscribed
            if not is_subscribed:
                all_subscribed = False
        except Exception as e:
            logging.error(f"خطأ في التحقق من الاشتراك: {e}")
            user_status[channel_id] = False
            all_subscribed = False
    if not all_subscribed:
        keyboard = []
        for channel in channels:
            channel_id = channel[1]
            channel_name = channel[2]
            is_subscribed = user_status.get(channel_id, False)
            if not is_subscribed:
                keyboard.append([
                    InlineKeyboardButton(f"📢 اشترك في {channel_name}",
                        url=f"https://t.me/{channel_id[1:] if channel_id.startswith('@') else channel_id}")
                ])
        keyboard.append([InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription")])
        await update.message.reply_text(
            fmt.format_force_subscription(
                [{'channel_id': c[1], 'channel_name': c[2]} for c in channels],
                user_status),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN)
        return False
    return True

# ============================================
# RedFox Code - دوال المعالجة الفعلية
# ============================================
async def download_tiktok_video(url: str):
    try:
        clean_url = url.strip()
        api_url = f"https://tikwm.com/api/?url={clean_url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == 0:
                        video_url = data["data"]["play"]
                        title = data["data"].get("title", "TikTok Video")
                        return {"success": True, "video_url": video_url, "title": title, "message": "✅ تم تحميل الفيديو بنجاح"}
        return {"success": False, "message": "❌ لم يتم العثور على الفيديو، تأكد من الرابط"}
    except Exception as e:
        return {"success": False, "message": f"❌ خطأ في التحميل: {str(e)[:100]}"}

async def process_tiktok_download(url: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        processing_msg = await update.message.reply_text("⏳ جاري تحميل الفيديو من TikTok...")
        result = await download_tiktok_video(url)
        if result["success"]:
            await processing_msg.edit_text(f"✅ {result['message']}\n\n🎬 {result.get('title', '')}")
            try:
                await update.message.reply_video(
                    video=result["video_url"],
                    caption=f"🎬 {result.get('title', 'TikTok Video')}\n\n📥 بواسطة @RedFoxVIPBot",
                    parse_mode=None)
                await processing_msg.delete()
            except:
                await update.message.reply_text(
                    f"✅ {result['message']}\n\n🔗 رابط الفيديو: {result['video_url']}\n\n🎬 {result.get('title', '')}")
        else:
            await processing_msg.edit_text(result["message"])
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ في المعالجة: {str(e)[:100]}")

async def process_spotify_download(url: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        processing_msg = await update.message.reply_text("⏳ جاري تحميل الأغنية من Spotify...")
        await processing_msg.edit_text(
            "✅ تم تحليل رابط Spotify بنجاح!\n\n"
            f"🔗 الرابط: {url}\n\n"
            "⚠️ هذه نسخة تجريبية\n"
            "📞 للخدمة الفعلية تواصل مع الدعم الفني")
    except Exception as e:
        await update.message.reply_text(f"❌ فشل التحميل: {str(e)[:100]}")

async def process_weather(city: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        processing_msg = await update.message.reply_text(f"⏳ جاري البحث عن حالة الطقس في {city}...")
        await processing_msg.edit_text(
            f"🌤️ *حالة الطقس في {city}*\n\n"
            f"🌡️ درجة الحرارة: 25°C\n"
            f"🌈 الحالة: مشمس\n"
            f"💨 سرعة الرياح: 10 كم/ساعة\n"
            f"💧 الرطوبة: 60%\n\n"
            f"📅 التوقعات للأيام القادمة:\n"
            f"• الغد: 26°C ☀️\n"
            f"• بعد الغد: 24°C ⛅\n"
            f"• اليوم الثالث: 23°C 🌧️\n\n"
            "⚠️ هذه معلومات تجريبية",
            parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ فشل الحصول على حالة الطقس: {str(e)[:100]}")

async def process_chatgpt_request(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        processing_msg = await update.message.reply_text("⏳ جاري معالجة طلبك بواسطة ChatGPT...")
        response = f"🤖 *ChatGPT يجيب:*\n\n"
        response += "مرحباً! أنا مساعد الذكاء الاصطناعي. في النسخة الكاملة، سأقوم بمعالجة طلبك وإعطائك إجابة مفصلة.\n\n"
        response += f"📝 *طلبك كان:* {text[:100]}{'...' if len(text) > 100 else ''}\n\n"
        response += "💡 *نصيحة:* للخدمة الكاملة مع الذكاء الاصطناعي الحقيقي، تواصل مع الدعم الفني.\n\n"
        response += "📞 الدعم: @Dev2z"
        await processing_msg.edit_text(response, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ فشل المعالجة: {str(e)[:100]}")

async def process_text_to_speech(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE, service_name: str):
    try:
        processing_msg = await update.message.reply_text("⏳ جاري تحويل النص إلى صوت...")
        await processing_msg.edit_text(
            f"🔊 *{service_name}*\n\n"
            f"📝 *النص:* {text[:100]}{'...' if len(text) > 100 else ''}\n\n"
            f"✅ *تم التحويل بنجاح!*\n\n"
            f"⚠️ هذه نسخة تجريبية\n"
            f"📞 للخدمة الفعلية تواصل مع الدعم الفني",
            parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ فشل التحويل: {str(e)[:100]}")

# ============================================
# RedFox Code - الدوال الرئيسية
# ============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not db.is_bot_active():
        await update.message.reply_text(
            "⏸️ *البوت متوقف مؤقتاً*\n\n"
            "يرجى الانتظار حتى يتم تفعيل البوت من قبل الإدارة.",
            parse_mode=ParseMode.MARKDOWN)
        return
    if not await check_force_subscription(update, context):
        return
    user = update.effective_user
    is_new_user = db.add_user(user.id, user.username or "", user.first_name or "", user.last_name or "")
    is_vip = db.is_vip(user.id)
    stats = db.get_statistics()
    welcome_message = fmt.format_welcome(user.first_name or "صديقي", stats, is_vip)
    await update.message.reply_text(welcome_message, reply_markup=create_main_keyboard(), parse_mode=ParseMode.MARKDOWN)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    button_data = query.data
    
    admin_buttons = ["admin_stats", "admin_users", "admin_requests", "admin_search", 
                    "create_sub_code", "admin_broadcast", "manage_admins", "manage_channels",
                    "bot_settings", "back_to_admin"]
    
    if button_data in admin_buttons:
        if not db.is_admin(user_id):
            await query.edit_message_text("❌ *أنت لست أدمن!*", parse_mode=ParseMode.MARKDOWN)
            return
        if button_data == "admin_stats":
            await show_admin_stats(query, context)
        elif button_data == "admin_users":
            await show_admin_users(query, context)
        elif button_data == "admin_requests":
            await show_admin_requests(query, context)
        elif button_data == "admin_search":
            await show_admin_search(query, context)
        elif button_data == "create_sub_code":
            await create_subscription_code(query, context)
        elif button_data == "admin_broadcast":
            await show_admin_broadcast(query, context)
        elif button_data == "manage_admins":
            await show_manage_admins(query, context)
        elif button_data == "manage_channels":
            await show_manage_channels(query, context)
        elif button_data == "bot_settings":
            await show_bot_settings(query, context)
        elif button_data == "back_to_admin":
            await show_admin_panel(query, context)
        return
    
    if button_data == "admin_panel":
        await show_admin_panel(query, context)
        return
    elif button_data == "back_to_menu":
        await back_to_menu(query, context)
        return
    elif button_data == "vip_section":
        await handle_vip_section(query, context)
        return
    elif button_data == "activate_subscription":
        await handle_activate_subscription(query, context)
        return
    elif button_data == "check_subscription":
        user_id = query.from_user.id
        channels = db.get_force_sub_channels()
        if not channels:
            await query.edit_message_text("✅ *لا توجد قنوات اشتراك إجباري*", parse_mode=ParseMode.MARKDOWN)
            return
        all_subscribed = True
        user_status = {}
        for channel in channels:
            channel_id = channel[1]
            try:
                chat_member = await context.bot.get_chat_member(channel_id, user_id)
                is_subscribed = chat_member.status not in ['left', 'kicked']
                user_status[channel_id] = is_subscribed
                if not is_subscribed:
                    all_subscribed = False
            except Exception as e:
                user_status[channel_id] = False
                all_subscribed = False
        if all_subscribed:
            await query.edit_message_text(
                "✅ *تم التحقق من الاشتراك في جميع القنوات!*\n\n"
                "يمكنك الآن استخدام البوت.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_to_menu")]
                ]),
                parse_mode=ParseMode.MARKDOWN)
        else:
            keyboard = []
            for channel in channels:
                channel_id = channel[1]
                channel_name = channel[2]
                is_subscribed = user_status.get(channel_id, False)
                if not is_subscribed:
                    keyboard.append([
                        InlineKeyboardButton(f"📢 اشترك في {channel_name}",
                            url=f"https://t.me/{channel_id[1:] if channel_id.startswith('@') else channel_id}")
                    ])
            keyboard.append([InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription")])
            await query.edit_message_text(
                fmt.format_force_subscription(
                    [{'channel_id': c[1], 'channel_name': c[2]} for c in channels],
                    user_status),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=ParseMode.MARKDOWN)
        return
    elif button_data == "about":
        stats = db.get_statistics()
        await query.edit_message_text(
            f"🤖 *RedFox Bot*\n\n"
            f"📊 *إحصائيات البوت:*\n"
            f"• 👥 المستخدمين: {stats['total_users']:,}\n"
            f"• 👑 مستخدمين VIP: {stats['vip_users']}\n"
            f"• 📥 إجمالي الطلبات: {stats['total_requests']:,}\n\n"
            f"✨ *جميع الخدمات مجانية!* ✨\n"
            f"🚀 *ما عدا Python Hosting VIP*\n\n"
            f"🛠 *المطور:* {SUPPORT_USERNAME}\n"
            f"📢 *القناة:* @RedFoxCyber\n\n"
            f"🚀 *إصدار 7.0 - النسخة الكاملة المحسنة*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 قناة البوت", url="https://t.me/RedFoxCyber")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")]
            ]),
            parse_mode=ParseMode.MARKDOWN)
        return
    elif button_data == "support":
        await query.edit_message_text(
            "👨‍💻 *الدعم الفني*\n\n"
            f"📞 *للتواصل والدعم:*\n"
            f"• {SUPPORT_USERNAME}\n\n"
            "📢 *قناة البوت:*\n"
            "• @RedFoxCyber\n\n"
            "💰 *للدفع بالنجوم للخدمات المدفوعة:*\n"
            f"• {SUPPORT_USERNAME}\n\n"
            "⏰ *ساعات العمل:* 24/7",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"📞 تواصل مع الدعم", url=f"https://t.me/{SUPPORT_USERNAME[1:]}")],
                [InlineKeyboardButton("📢 قناة البوت", url="https://t.me/RedFoxCyber")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")]
            ]),
            parse_mode=ParseMode.MARKDOWN)
        return
    elif button_data == "python_hosting":
        user_id = query.from_user.id
        is_vip = db.is_vip(user_id)
        if is_vip:
            service = SERVICES.get(button_data, {})
            message = fmt.format_service_intro(
                service.get("name", "🚀 Python Hosting (VIP)"),
                service.get("description", ""),
                service.get("example", ""))
        else:
            message = f"""🚀 *Python Hosting VIP*

💰 *خدمة مدفوعة - سعر خاص:*

⭐ *أسعار الاشتراك:*
• 30 يوم: 200 نجمة ⭐

📞 *للدفع بالنجوم والحصول على الخدمة:*
{SUPPORT_USERNAME}

🎫 *للحصول على كود تفعيل، استخدم زر "🎫 تفعيل اشتراك"*"""
        keyboard = [
            [InlineKeyboardButton("🎫 تفعيل اشتراك", callback_data="activate_subscription")],
            [InlineKeyboardButton(f"💬 تواصل للشراء", url=f"https://t.me/{SUPPORT_USERNAME[1:]}")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")]
        ]
        await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)
        return
    elif button_data in SERVICES:
        service = SERVICES[button_data]
        if service.get("vip_only", False):
            user_id = query.from_user.id
            if not db.is_vip(user_id):
                await query.edit_message_text(
                    "👑 *خدمة VIP فقط!*\n\n"
                    "❌ هذه الخدمة متاحة للمشتركين VIP فقط.\n\n"
                    "🎫 للحصول على الاشتراك، استخدم زر '🎫 تفعيل اشتراك'",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🎫 تفعيل اشتراك", callback_data="activate_subscription")],
                        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")]
                    ]),
                    parse_mode=ParseMode.MARKDOWN)
                return
        db.set_user_action(user_id, button_data)
        await query.edit_message_text(
            fmt.format_service_intro(service["name"], service["description"], service["example"]),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")]
            ]),
            parse_mode=ParseMode.MARKDOWN)

async def handle_vip_section(query, context):
    user_id = query.from_user.id
    is_vip = db.is_vip(user_id)
    if is_vip:
        vip_info = db.get_vip_info(user_id)
        if vip_info:
            message = fmt.format_subscription_info(vip_info)
        else:
            message = "✨ *أنت مشترك VIP*"
    else:
        message = f"""👑 *قسم VIP*

🚀 *Python Hosting VIP فقط*

⭐ *أسعار الاشتراك:*
• 30 يوم: 200 نجمة ⭐

📞 *للدفع بالنجوم:*
{SUPPORT_USERNAME}"""
    keyboard = [
        [InlineKeyboardButton("🎫 تفعيل اشterاك", callback_data="activate_subscription")],
        [InlineKeyboardButton(f"💬 تواصل للشراء", url=f"https://t.me/{SUPPORT_USERNAME[1:]}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")]
    ]
    await query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def handle_activate_subscription(query, context):
    await query.edit_message_text(
        "🎫 *تفعيل اشتراك VIP*\n\n"
        "أرسل كود الاشتراك الذي حصلت عليه.\n\n"
        "📝 *مثال:*\n"
        "`RedFoxBot687687`\n\n"
        "⏰ *المدة:* 30 يوم\n"
        "💎 *المميزات:* Python Hosting VIP",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_menu")]
        ]))

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not db.is_bot_active():
        await update.message.reply_text(
            "⏸️ البوت متوقف مؤقتاً\n\nيرجى الانتظار حتى يتم تفعيل البوت من قبل الإدارة.",
            parse_mode=None)
        return
    user_id = update.effective_user.id
    message_text = update.message.text.strip()
    if message_text.startswith("RedFoxBot") and len(message_text) == len("RedFoxBot") + 6:
        success, result_message = db.use_vip_code(message_text, user_id)
        if success:
            vip_info = db.get_vip_info(user_id)
            if vip_info:
                subscription_info = fmt.format_subscription_info(vip_info)
                await update.message.reply_text(subscription_info, parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text(result_message, parse_mode=None)
        else:
            await update.message.reply_text(result_message, parse_mode=None)
        return
    if db.is_admin(user_id):
        if message_text.startswith("REQ") or message_text.isdigit():
            results = db.search_request(message_text)
            if results:
                search_text = "🔍 نتائج البحث:\n\n"
                for result in results[:5]:
                    req_id, request_code, req_user_id, api_name, request_data, response_data, status, timestamp, username, first_name = result
                    search_text += f"🎫 الكود: {request_code}\n"
                    search_text += f"👤 المستخدم: {first_name} (@{username or 'بدون'})\n"
                    search_text += f"🛠 الخدمة: {api_name}\n"
                    search_text += f"📝 الطلب: {request_data[:50]}...\n"
                    search_text += f"📅 التاريخ: {timestamp}\n\n"
                await update.message.reply_text(search_text, parse_mode=None)
                return
            else:
                await update.message.reply_text(f"❌ لم يتم العثور على نتائج لـ: {message_text}", parse_mode=None)
                return
    user_action = db.get_user_action(user_id)
    if user_action and user_action in SERVICES:
        current_action = user_action
        service_info = SERVICES[current_action]
        request_code = db.add_request(user_id, current_action, message_text, "في انتظار المعالجة")
        await update.message.reply_text(
            fmt.format_request_code(request_code, service_info["name"], message_text),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_to_menu")]
            ]),
            parse_mode=ParseMode.MARKDOWN)
        try:
            if current_action == "tiktok_dl":
                await process_tiktok_download(message_text, update, context)
            elif current_action == "spotify_dl":
                await process_spotify_download(message_text, update, context)
            elif current_action == "weather":
                await process_weather(message_text, update, context)
            elif current_action == "chatgpt":
                await process_chatgpt_request(message_text, update, context)
            elif current_action in ["microsoft_tts", "openai_tts", "tiktok_tts", "google_tts", 
                                   "loquendo_tts", "openai_tts_converter"]:
                await process_text_to_speech(message_text, update, context, service_info["name"])
            elif current_action in ["ai_chat_multi", "hashtag_gen", "translator"]:
                await update.message.reply_text(
                    f"🤖 *{service_info['name']}*\n\n"
                    f"📝 *الطلب:* {message_text[:200]}{'...' if len(message_text) > 200 else ''}\n\n"
                    f"✅ *تمت المعالجة بنجاح!*\n\n"
                    f"⚠️ هذه نسخة تجريبية\n"
                    f"📞 للخدمة الفعلية تواصل مع الدعم الفني",
                    parse_mode=ParseMode.MARKDOWN)
            elif current_action in ["yt_summarizer", "yt_transcript", "link_shortener"]:
                await update.message.reply_text(
                    f"🔗 *{service_info['name']}*\n\n"
                    f"📝 *الرابط:* {message_text}\n\n"
                    f"✅ *تمت المعالجة بنجاح!*\n\n"
                    f"⚠️ هذه نسخة تجريبية\n"
                    f"📞 للخدمة الفعلية تواصل مع الدعم الفني",
                    parse_mode=ParseMode.MARKDOWN)
            elif current_action == "ai_image":
                await update.message.reply_text(
                    f"🎨 *{service_info['name']}*\n\n"
                    f"📝 *الوصف:* {message_text[:200]}{'...' if len(message_text) > 200 else ''}\n\n"
                    f"✅ *تم إنشاء الصورة!*\n\n"
                    f"⚠️ هذه نسخة تجريبية\n"
                    f"📞 للخدمة الفعلية تواصل مع الدعم الفني",
                    parse_mode=ParseMode.MARKDOWN)
            elif current_action == "python_hosting":
                if db.is_vip(user_id):
                    await update.message.reply_text(
                        f"🚀 *{service_info['name']}*\n\n"
                        f"📁 *تم استلام ملف Python*\n\n"
                        f"✅ *سيتم استضافة الملف على السيرفر*\n\n"
                        f"⚠️ هذه نسخة تجريبية\n"
                        f"📞 للخدمة الفعلية تواصل مع الدعم الفني",
                        parse_mode=ParseMode.MARKDOWN)
                else:
                    await update.message.reply_text(
                        "❌ *خدمة VIP فقط!*\n\n"
                        "هذه الخدمة متاحة للمشتركين VIP فقط.",
                        parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text(
                    f"🛠️ *{service_info['name']}*\n\n"
                    f"📝 *البيانات:* {message_text[:200]}{'...' if len(message_text) > 200 else ''}\n\n"
                    f"✅ *تمت المعالجة بنجاح!*\n\n"
                    f"⚠️ هذه نسخة تجريبية\n"
                    f"📞 للخدمة الفعلية تواصل مع الدعم الفني",
                    parse_mode=ParseMode.MARKDOWN)
            db.update_request_status(request_code, "completed")
        except Exception as e:
            await update.message.reply_text(f"❌ *فشل المعالجة:*\n\n{str(e)[:200]}", parse_mode=None)
            db.update_request_status(request_code, f"failed: {str(e)[:100]}")
        db.clear_user_action(user_id)
    else:
        await update.message.reply_text(
            "❌ *لم تختر أي خدمة بعد!*\n\n"
            "استخدم الأزرار لاختيار الخدمة المطلوبة.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_to_menu")]
            ]),
            parse_mode=ParseMode.MARKDOWN)

# ============================================
# RedFox Code - لوحة تحكم الأدمن
# ============================================
async def show_admin_panel(query, context):
    user_id = query.from_user.id
    if not db.is_admin(user_id):
        await query.edit_message_text("❌ *أنت لست أدمن!*", parse_mode=ParseMode.MARKDOWN)
        return
    stats = db.get_statistics()
    admin_text = f"""🛠 *لوحة تحكم الأدمن*

📊 *الإحصائيات الحالية:*
• 👥 إجمالي المستخدمين: {stats['total_users']:,}
• 👑 مستخدمين VIP: {stats['vip_users']}
• 📥 إجمالي الطلبات: {stats['total_requests']:,}

🔧 *الأدوات المتاحة:*"""
    await query.edit_message_text(admin_text, reply_markup=create_admin_keyboard(), parse_mode=ParseMode.MARKDOWN)

async def show_admin_stats(query, context):
    stats = db.get_statistics()
    all_users = db.get_all_users()
    active_users = len([u for u in all_users if u[6] > 0])
    stats_text = f"""📊 *إحصائيات مفصلة*

👥 *المستخدمين:*
• الإجمالي: {stats['total_users']:,}
• النشطين: {active_users:,}
• VIP: {stats['vip_users']}

📥 *الطلبات:*
• الإجمالي: {stats['total_requests']:,}

🔄 *آخر تحديث:*
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث", callback_data="admin_stats")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]
    ]
    await query.edit_message_text(stats_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def show_admin_users(query, context):
    users = db.get_all_users()[:15]
    users_text = "👥 *آخر 15 مستخدم:*\n\n"
    for i, user in enumerate(users, 1):
        user_id, username, first_name, last_name, join_date, request_count, current_action, is_vip, vip_start, vip_end, vip_code = user
        username_display = f"@{username}" if username else "بدون"
        vip_status = "👑" if is_vip == 1 else "👤"
        users_text += f"{i}. {vip_status} *{first_name}* {username_display}\n"
        users_text += f"   🆔 `{user_id}` | 📊 {request_count} طلب\n"
        users_text += f"   📅 {join_date}\n\n"
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث", callback_data="admin_users")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]
    ]
    await query.edit_message_text(users_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def show_admin_requests(query, context):
    requests = db.get_recent_requests(10)
    requests_text = "📋 *آخر 10 طلبات:*\n\n"
    for i, req in enumerate(requests, 1):
        req_id, request_code, user_id, api_name, request_data, response_data, status, timestamp, username, first_name = req
        requests_text += f"{i}. *{first_name}* (@{username or 'بدون'})\n"
        requests_text += f"   🎫 *الكود:* `{request_code}`\n"
        requests_text += f"   🛠 *الخدمة:* {api_name}\n"
        requests_text += f"   📅 *التاريخ:* {timestamp}\n\n"
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث", callback_data="admin_requests")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]
    ]
    await query.edit_message_text(requests_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def create_subscription_code(query, context):
    user_id = query.from_user.id
    if not db.is_admin(user_id):
        await query.edit_message_text("❌ *أنت لست أدمن!*", parse_mode=ParseMode.MARKDOWN)
        return
    code = db.create_vip_code(user_id)
    await query.edit_message_text(
        f"✅ *تم إنشاء كود اشتراك جديد!*\n\n"
        f"🎫 *الكود:* `{code}`\n"
        f"⏰ *المدة:* 30 يوم\n"
        f"👤 *المنشئ:* {query.from_user.first_name}\n"
        f"📅 *التاريخ:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"🔑 *لتفعيل الكود:*\n"
        f"استخدم زر *🎫 تفعيل اشتراك* في القائمة الرئيسية",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎫 إنشاء كود آخر", callback_data="create_sub_code")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]
        ]))

async def show_admin_search(query, context):
    await query.edit_message_text(
        "🔍 *البحث عن طلب*\n\n"
        "أرسل كود الطلب للبحث عنه.\n\n"
        "📝 *مثال:*\n"
        "`REQ12345`\n"
        "`123456789` (معرف المستخدم)",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]
        ]))

async def show_manage_admins(query, context):
    admins = db.get_admins()
    admins_text = "👑 *قائمة الأدمن:*\n\n"
    for admin in admins:
        user_id, added_by, added_date = admin
        admins_text += f"🆔 *{user_id}*\n"
        admins_text += f"📅 *تاريخ الإضافة:* {added_date}\n\n"
    admins_text += "📝 *الأوامر:*\n"
    admins_text += "`/addadmin [المعرف]` - إضافة أدمن\n"
    admins_text += "`/removeadmin [المعرف]` - إزالة أدمن"
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث", callback_data="manage_admins")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]
    ]
    await query.edit_message_text(admins_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def show_manage_channels(query, context):
    channels = db.get_force_sub_channels()
    channels_text = "📢 *قنوات الاشتراك الإجباري:*\n\n"
    if channels:
        for channel in channels:
            channel_id, channel_name = channel[1], channel[2]
            channels_text += f"• *{channel_name}*\n"
            channels_text += f"  🆔 `{channel_id}`\n\n"
    else:
        channels_text += "❌ *لا توجد قنوات مضافة*\n\n"
    channels_text += "📝 *الأوامر:*\n"
    channels_text += "`/addchannel [معرف القناة] [اسم القناة]` - إضافة قناة\n"
    channels_text += "`/removechannel [معرف القناة]` - إزالة قناة\n"
    channels_text += "`/enableforce` - تفعيل الاشتراك الإجباري\n"
    channels_text += "`/disableforce` - تعطيل الاشتراك الإجباري"
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث", callback_data="manage_channels")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]
    ]
    await query.edit_message_text(channels_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def show_bot_settings(query, context):
    bot_active = db.is_bot_active()
    force_sub_enabled = db.is_force_sub_enabled()
    settings_text = f"""⚙️ *إعدادات البوت*

🟢 *حالة البوت:* {"✅ نشط" if bot_active else "⏸️ متوقف"}
📢 *الاشتراك الإجباري:* {"✅ مفعل" if force_sub_enabled else "❌ معطل"}

🛠 *الأوامر:*
`/startbot` - تشغيل البوت
`/stopbot` - إيقاف البوت
`/enableforce` - تفعيل الاشتراك الإجباري
`/disableforce` - تعطيل الاشتراك الإجباري"""
    keyboard = [
        [InlineKeyboardButton("🔄 تحديث", callback_data="bot_settings")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]
    ]
    await query.edit_message_text(settings_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def show_admin_broadcast(query, context):
    users = db.get_all_users()
    await query.edit_message_text(
        f"📢 *إرسال إذاعة*\n\n"
        f"👥 *عدد المستخدمين:* {len(users):,}\n\n"
        f"📝 *لإرسال إذاعة:*\n"
        f"استخدم الأمر:\n"
        f"`/broadcast [الرسالة]`\n\n"
        f"📝 *مثال:*\n"
        f"`/broadcast مرحبًا بالجميع!`",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_admin")]
        ]))

async def back_to_menu(query, context):
    user_id = query.from_user.id
    user_info = db.get_user(user_id)
    is_vip = user_info[7] == 1 if user_info else False
    stats = db.get_statistics()
    welcome_message = fmt.format_welcome(query.from_user.first_name or "صديقي", stats, is_vip)
    await query.edit_message_text(welcome_message, reply_markup=create_main_keyboard(), parse_mode=ParseMode.MARKDOWN)

# ============================================
# RedFox Code - الأوامر الإدارية
# ============================================
async def add_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text("❌ *هذا الأمر للمسؤولين فقط!*", parse_mode=ParseMode.MARKDOWN)
        return
    if len(context.args) < 1:
        await update.message.reply_text(
            "❌ *استخدام خاطئ!*\n\n"
            "📝 *الصيغة الصحيحة:*\n"
            "`/addadmin [معرف المستخدم]`\n\n"
            "📝 *مثال:*\n"
            "`/addadmin 123456789`",
            parse_mode=ParseMode.MARKDOWN)
        return
    try:
        new_admin_id = int(context.args[0])
        db.add_admin(new_admin_id, user_id)
        await update.message.reply_text(
            f"✅ *تمت إضافة الأدمن بنجاح!*\n\n"
            f"👤 *المعرف:* `{new_admin_id}`\n"
            f"📅 *التاريخ:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode=ParseMode.MARKDOWN)
    except ValueError:
        await update.message.reply_text("❌ *المعرف يجب أن يكون رقماً صحيحاً!*", parse_mode=ParseMode.MARKDOWN)

async def remove_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text("❌ *هذا الأمر للمسؤولين فقط!*", parse_mode=ParseMode.MARKDOWN)
        return
    if len(context.args) < 1:
        await update.message.reply_text(
            "❌ *استخدام خاطئ!*\n\n"
            "📝 *الصيغة الصحيحة:*\n"
            "`/removeadmin [معرف المستخدم]`\n\n"
            "📝 *مثال:*\n"
            "`/removeadmin 123456789`",
            parse_mode=ParseMode.MARKDOWN)
        return
    try:
        admin_id = int(context.args[0])
        if admin_id in ADMIN_IDS:
            await update.message.reply_text("❌ *لا يمكن إزالة الأدمن الأساسي!*", parse_mode=ParseMode.MARKDOWN)
            return
        db.remove_admin(admin_id)
        await update.message.reply_text(
            f"✅ *تمت إزالة الأدمن بنجاح!*\n\n"
            f"👤 *المعرف:* `{admin_id}`",
            parse_mode=ParseMode.MARKDOWN)
    except ValueError:
        await update.message.reply_text("❌ *المعرف يجب أن يكون رقماً صحيحاً!*", parse_mode=ParseMode.MARKDOWN)

async def add_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text("❌ *هذا الأمر للمسؤولين فقط!*", parse_mode=ParseMode.MARKDOWN)
        return
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ *استخدام خاطئ!*\n\n"
            "📝 *الصيغة الصحيحة:*\n"
            "`/addchannel [معرف القناة] [اسم القناة]`\n\n"
            "📝 *مثال:*\n"
            "`/addchannel @RedFoxCyber قناة ريدفوكس`",
            parse_mode=ParseMode.MARKDOWN)
        return
    channel_id = context.args[0]
    channel_name = ' '.join(context.args[1:])
    db.add_force_sub_channel(channel_id, channel_name, user_id)
    await update.message.reply_text(
        f"✅ *تمت إضافة القناة بنجاح!*\n\n"
        f"📢 *اسم القناة:* {channel_name}\n"
        f"🆔 *معرف القناة:* `{channel_id}`\n"
        f"📅 *التاريخ:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        parse_mode=ParseMode.MARKDOWN)

async def remove_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text("❌ *هذا الأمر للمسؤولين فقط!*", parse_mode=ParseMode.MARKDOWN)
        return
    if len(context.args) < 1:
        await update.message.reply_text(
            "❌ *استخدام خاطئ!*\n\n"
            "📝 *الصيغة الصحيحة:*\n"
            "`/removechannel [معرف القناة]`\n\n"
            "📝 *مثال:*\n"
            "`/removechannel @RedFoxCyber`",
            parse_mode=ParseMode.MARKDOWN)
        return
    channel_id = context.args[0]
    db.remove_force_sub_channel(channel_id)
    await update.message.reply_text(
        f"✅ *تمت إزالة القناة بنجاح!*\n\n"
        f"🆔 *معرف القناة:* `{channel_id}`",
        parse_mode=ParseMode.MARKDOWN)

async def enable_force_sub_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text("❌ *هذا الأمر للمسؤولين فقط!*", parse_mode=ParseMode.MARKDOWN)
        return
    db.set_force_sub_enabled(True)
    await update.message.reply_text(
        "✅ *تم تفعيل الاشتراك الإجباري بنجاح!*\n\n"
        "سيتم طلب الاشتراك في القنوات المحددة من جميع المستخدمين الجدد.",
        parse_mode=ParseMode.MARKDOWN)

async def disable_force_sub_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text("❌ *هذا الأمر للمسؤولين فقط!*", parse_mode=ParseMode.MARKDOWN)
        return
    db.set_force_sub_enabled(False)
    await update.message.reply_text("✅ *تم تعطيل الاشتراك الإجباري بنجاح!*", parse_mode=ParseMode.MARKDOWN)

async def start_bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text("❌ *هذا الأمر للمسؤولين فقط!*", parse_mode=ParseMode.MARKDOWN)
        return
    db.set_bot_active(True)
    await update.message.reply_text(
        "✅ *تم تشغيل البوت بنجاح!*\n\n"
        "البوت الآن نشط وجاهز للاستخدام.",
        parse_mode=ParseMode.MARKDOWN)

async def stop_bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text("❌ *هذا الأمر للمسؤولين فقط!*", parse_mode=ParseMode.MARKDOWN)
        return
    db.set_bot_active(False)
    await update.message.reply_text(
        "⏸️ *تم إيقاف البوت مؤقتاً!*\n\n"
        "البوت الآن غير متاح للمستخدمين.",
        parse_mode=ParseMode.MARKDOWN)

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text("❌ *هذا الأمر للمسؤولين فقط!*", parse_mode=ParseMode.MARKDOWN)
        return
    if not context.args:
        await update.message.reply_text(
            "❌ *استخدام خاطئ!*\n\n"
            "📝 *الصيغة الصحيحة:*\n"
            "`/broadcast [الرسالة]`\n\n"
            "📝 *مثال:*\n"
            "`/broadcast مرحبًا بالجميع!`",
            parse_mode=ParseMode.MARKDOWN)
        return
    message = ' '.join(context.args)
    users = db.get_all_users()
    if not users:
        await update.message.reply_text("❌ *لا يوجد مستخدمين لإرسال الرسالة!*", parse_mode=ParseMode.MARKDOWN)
        return
    sent_count = 0
    failed_count = 0
    progress_msg = await update.message.reply_text(
        f"📢 *جاري إرسال الإذاعة...*\n"
        f"👥 *إجمالي المستخدمين:* {len(users):,}\n"
        f"✅ *تم إرسالها:* 0\n"
        f"❌ *فشل:* 0",
        parse_mode=ParseMode.MARKDOWN)
    for i, user in enumerate(users, 1):
        try:
            await context.bot.send_message(chat_id=user[0], text=message, parse_mode=ParseMode.MARKDOWN)
            sent_count += 1
            if i % 10 == 0:
                await progress_msg.edit_text(
                    f"📢 *جاري إرسال الإذاعة...*\n"
                    f"👥 *إجمالي المستخدمين:* {len(users):,}\n"
                    f"✅ *تم إرسالها:* {sent_count:,}\n"
                    f"❌ *فشل:* {failed_count:,}",
                    parse_mode=ParseMode.MARKDOWN)
            await asyncio.sleep(0.1)
        except Exception as e:
            failed_count += 1
            logging.error(f"فشل إرسال إذاعة لـ {user[0]}: {e}")
    await progress_msg.edit_text(
        f"✅ *تم إكمال الإذاعة!*\n\n"
        f"👥 *إجمالي المستخدمين:* {len(users):,}\n"
        f"✅ *تم إرسالها بنجاح:* {sent_count:,}\n"
        f"❌ *فشل في الإرسال:* {failed_count:,}",
        parse_mode=ParseMode.MARKDOWN)

# ============================================
# RedFox Code - دوال الإصلاح
# ============================================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error_msg = str(context.error) if context.error else "خطأ غير معروف"
    print(f"❌ خطأ: {error_msg}")
    if context.error:
        traceback.print_exc()
    try:
        if update and update.effective_chat:
            clean_error_msg = error_msg
            chars_to_clean = ['*', '_', '`', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.']
            for char in chars_to_clean:
                clean_error_msg = clean_error_msg.replace(char, ' ')
            clean_error_msg = ' '.join(clean_error_msg.split())
            if len(clean_error_msg) > 80:
                clean_error_msg = clean_error_msg[:80] + "..."
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ حدث خطأ في المعالجة.\n\n📋 الخطأ: {clean_error_msg}\n\n🔧 يرجى المحاولة مرة أخرى أو استخدام /start",
                parse_mode=None)
    except Exception as e:
        print(f"❌ فشل إرسال رسالة الخطأ: {e}")

def fix_database_structure():
    print("🔧 جاري إصلاح هيكل قاعدة البيانات...")
    try:
        if os.path.exists(DATABASE_FILE):
            backup_file = DATABASE_FILE + ".backup"
            if not os.path.exists(backup_file):
                shutil.copy2(DATABASE_FILE, backup_file)
                print(f"📁 تم إنشاء نسخة احتياطية: {backup_file}")
        conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS requests")
        cursor.execute('''CREATE TABLE requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_code TEXT,
            user_id INTEGER,
            api_name TEXT,
            request_data TEXT,
            response_data TEXT,
            status TEXT DEFAULT 'pending',
            timestamp TIMESTAMP)''')
        print("✅ تم إنشاء جدول requests بنجاح!")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone():
            try:
                cursor.execute('ALTER TABLE users ADD COLUMN current_action TEXT DEFAULT NULL')
                print("✅ تم إضافة العمود current_action")
            except sqlite3.OperationalError:
                print("✅ العمود current_action موجود بالفعل")
        conn.commit()
        conn.close()
        print("✅ تم إكمال إصلاح قاعدة البيانات بنجاح!")
    except Exception as e:
        print(f"❌ خطأ في إصلاح قاعدة البيانات: {e}")
        traceback.print_exc()

# ============================================
# RedFox Code - الدالة الرئيسية
# ============================================
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    fix_database_structure()
    application.add_error_handler(error_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addadmin", add_admin_command))
    application.add_handler(CommandHandler("removeadmin", remove_admin_command))
    application.add_handler(CommandHandler("addchannel", add_channel_command))
    application.add_handler(CommandHandler("removechannel", remove_channel_command))
    application.add_handler(CommandHandler("enableforce", enable_force_sub_command))
    application.add_handler(CommandHandler("disableforce", disable_force_sub_command))
    application.add_handler(CommandHandler("startbot", start_bot_command))
    application.add_handler(CommandHandler("stopbot", stop_bot_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CallbackQueryHandler(handle_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    
    print("🤖 RedFox Bot يعمل الآن...")
    print(f"📊 قاعدة البيانات: {DATABASE_FILE}")
    print(f"📝 ملف السجلات: {LOG_FILE}")
    print(f"👨‍💻 الدعم الفني: {SUPPORT_USERNAME}")
    print(f"🤖 يوزر البوت: {BOT_USERNAME}")
    print("📢 القناة: @RedFoxCyber")
    print("✨ جميع الخدمات مجانية!")
    print("🚀 Python Hosting فقط مدفوع")
    print("✅ النسخة 7.0 - النسخة الكاملة مع جميع الميزات")
    print("🎫 نظام VIP مع أكواد تفعيل")
    print("📢 نظام الاشتراك الإجباري")
    print("🛠 لوحة تحكم كاملة")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()