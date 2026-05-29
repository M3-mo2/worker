import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, BotCommand
import uuid
import random
import time
import os
from datetime import datetime

# --- الإعدادات الأساسية ---
API_TOKEN = '8320021946:AAGYl4q_kl7MTfzxnQiVlt39tGynbpW7bQ0'
ADMIN_IDS = [6502266915]
DEVELOPER_ID = 6502266915

bot = telebot.TeleBot(API_TOKEN)

# --- نظام التخزين في الذاكرة فقط ---
class MemoryStorage:
    def __init__(self):
        self.data = {
            'global_settings': {'bot_is_active': True},
            'user_channels': {},
            'active_roulettes': {},
            'banned_users': {},
            'user_data': {},
            'mandatory_channels': {},
            'roulette_channels': {},
            'user_subscriptions': {},
            'notified_users': {},
            'admins': {}  # إضافة تخزين المشرفين
        }
    
    def save(self):
        pass
    
    def load(self):
        pass

# إنشاء التخزين في الذاكرة
storage = MemoryStorage()
data = storage.data

# --- دوال سريعة ---
def get_global_setting(key):
    return data.get('global_settings', {}).get(key, True)

def set_global_setting(key, value):
    if 'global_settings' not in data:
        data['global_settings'] = {}
    data['global_settings'][key] = value

def get_user_channels(user_id):
    return data.get('user_channels', {}).get(str(user_id), [])

def add_user_channel(user_id, channel_id, channel_username):
    if 'user_channels' not in data:
        data['user_channels'] = {}
    if str(user_id) not in data['user_channels']:
        data['user_channels'][str(user_id)] = []
    
    # التحقق من عدم تكرار القناة
    for channel in data['user_channels'][str(user_id)]:
        if channel['channel_id'] == channel_id:
            return False
    
    data['user_channels'][str(user_id)].append({
        'channel_id': channel_id,
        'channel_username': channel_username,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return True

def remove_user_channel(user_id, channel_id):
    if str(user_id) in data.get('user_channels', {}):
        data['user_channels'][str(user_id)] = [
            channel for channel in data['user_channels'][str(user_id)] 
            if channel['channel_id'] != channel_id
        ]
        if not data['user_channels'][str(user_id)]:
            del data['user_channels'][str(user_id)]

def get_active_roulettes():
    return data.get('active_roulettes', {})

def save_roulette(roulette_id, roulette_data):
    if 'active_roulettes' not in data:
        data['active_roulettes'] = {}
    data['active_roulettes'][roulette_id] = roulette_data

def get_banned_users():
    return data.get('banned_users', {})

def ban_user(user_id):
    if 'banned_users' not in data:
        data['banned_users'] = {}
    data['banned_users'][str(user_id)] = {
        'banned_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def unban_user(user_id):
    if str(user_id) in data.get('banned_users', {}):
        del data['banned_users'][str(user_id)]

def is_user_banned(user_id):
    return str(user_id) in data.get('banned_users', {})

def save_user_data(user_id, username, first_name, last_name=None):
    if 'user_data' not in data:
        data['user_data'] = {}
    data['user_data'][str(user_id)] = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'joined_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_users_count():
    return len(data.get('user_data', {}))

def get_mandatory_channels():
    return data.get('mandatory_channels', {})

def add_mandatory_channel(channel_id, channel_username):
    if 'mandatory_channels' not in data:
        data['mandatory_channels'] = {}
    data['mandatory_channels'][str(channel_id)] = {
        'username': channel_username,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def remove_mandatory_channel(channel_id):
    if str(channel_id) in data.get('mandatory_channels', {}):
        del data['mandatory_channels'][str(channel_id)]

def get_mandatory_channels_count():
    return len(data.get('mandatory_channels', {}))

def get_roulette_channels():
    return data.get('roulette_channels', {})

def add_roulette_channel(channel_id, channel_username):
    if 'roulette_channels' not in data:
        data['roulette_channels'] = {}
    data['roulette_channels'][str(channel_id)] = {
        'username': channel_username,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def remove_roulette_channel(channel_id):
    if str(channel_id) in data.get('roulette_channels', {}):
        del data['roulette_channels'][str(channel_id)]

def get_roulette_channels_count():
    return len(data.get('roulette_channels', {}))

def mark_user_subscribed(user_id):
    if 'user_subscriptions' not in data:
        data['user_subscriptions'] = {}
    data['user_subscriptions'][str(user_id)] = True

def is_user_subscribed(user_id):
    return str(user_id) in data.get('user_subscriptions', {})

# --- دوال إدارة المشرفين ---
def add_admin(user_id, added_by, username=None, first_name=None):
    if 'admins' not in data:
        data['admins'] = {}
    data['admins'][str(user_id)] = {
        'username': username,
        'first_name': first_name,
        'added_by': added_by,
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def remove_admin(user_id):
    if str(user_id) in data.get('admins', {}):
        del data['admins'][str(user_id)]

def is_admin(user_id):
    return user_id in ADMIN_IDS or str(user_id) in data.get('admins', {})

def get_admins():
    return data.get('admins', {})

def get_admins_count():
    return len(data.get('admins', {}))

# --- التحقق من الاشتراك الإجباري ---
def check_mandatory_join(user_id):
    mandatory_channels = get_mandatory_channels()
    if not mandatory_channels:
        return True, []
    
    not_joined_channels = []
    for channel_id, channel_data in mandatory_channels.items():
        if not is_channel_member(int(channel_id), user_id):
            not_joined_channels.append(channel_data['username'])
    
    return len(not_joined_channels) == 0, not_joined_channels

# --- التحقق من صلاحيات البوت في القناة ---
def is_bot_admin_in_channel(channel_id):
    try:
        bot_member = bot.get_chat_member(channel_id, bot.get_me().id)
        return bot_member.status in ['administrator', 'creator']
    except Exception as e:
        print(f"خطأ في التحقق من صلاحيات البوت: {e}")
        return False

# --- التحقق من صلاحيات المستخدم في القناة ---
def is_user_admin_in_channel(channel_id, user_id):
    try:
        user_member = bot.get_chat_member(channel_id, user_id)
        return user_member.status in ['administrator', 'creator']
    except Exception as e:
        print(f"خطأ في التحقق من صلاحيات المستخدم: {e}")
        return False

# --- إعداد سريع ---
def set_bot_commands():
    commands = [
        BotCommand("start", "بدء استخدام البوت 🚀"),
    ]
    try:
        bot.set_my_commands(commands)
    except:
        pass

# --- النصوص ---
def get_welcome_text(first_name):
    return f"""أهلاً بك يا {first_name} 🎉

في روليت السر هنا ستجد روليت سهل ومجاني لاجلك"""

# --- المتغيرات السريعة ---
user_states = {}
user_temp_data = {}

# --- إشعار للمطور ---
def notify_admin_new_user(user_id, username, first_name):
    if 'notified_users' not in data:
        data['notified_users'] = {}
    if str(user_id) in data['notified_users']:
        return
    
    total_users = get_users_count()
    
    for admin_id in ADMIN_IDS:
        try:
            bot.send_message(
                admin_id,
                f"🆔 **تم تسجيل دخول شخص جديد إلى البوت**\n\n"
                f"👤 **الاسم:** {first_name}\n"
                f"📱 **اليوزر:** @{username if username else 'لا يوجد'}\n"
                f"🆔 **الأيدي:** `{user_id}`\n"
                f"⏰ **الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"👥 **العدد الكلي للمستخدمين:** {total_users}",
                parse_mode="Markdown"
            )
            data['notified_users'][str(user_id)] = True
        except:
            pass

# --- إشعار إنشاء روليت جديد ---
def notify_new_roulette(user_id, username, first_name, channel_username, channel_id):
    for admin_id in ADMIN_IDS:
        try:
            bot.send_message(
                admin_id,
                f"🎯 روليت جديد!\n\n"
                f"👤 المستخدم: {first_name} (@{username if username else 'لا يوجد'})\n"
                f"🆔 أيدي المستخدم: {user_id}\n"
                f"📢 القناة: @{channel_username}\n"
                f"🔗 رابط القناة: https://t.me/{channel_username}\n"
                f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
        except:
            pass

# --- إشعار حظر البوت ---
def notify_user_blocked_bot(user_id, username, first_name):
    total_users = get_users_count()
    
    for admin_id in ADMIN_IDS:
        try:
            bot.send_message(
                admin_id,
                f"🚫 **قام مستخدم بحظر البوت**\n\n"
                f"👤 **الاسم:** {first_name}\n"
                f"📱 **اليوزر:** @{username if username else 'لا يوجد'}\n"
                f"🆔 **الأيدي:** `{user_id}`\n"
                f"⏰ **الوقت:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"👥 **العدد الكلي للمستخدمين:** {total_users}",
                parse_mode="Markdown"
            )
        except:
            pass

# --- لوحات المفاتيح ---
def main_menu_kb(user_id):
    kb = InlineKeyboardMarkup(row_width=2)
    
    kb.row(
        InlineKeyboardButton("🎰 ابدأ روليت", callback_data="create_roulette"),
        InlineKeyboardButton("📺 قنواتي", callback_data="my_channels")
    )
    
    kb.row(
        InlineKeyboardButton("❓ مساعدة", callback_data="help"),
        InlineKeyboardButton("📜 سياسة الاستخدام", callback_data="usage_policy")
    )
    
    if is_admin(user_id):
        kb.row(InlineKeyboardButton("⚙️ لوحة الإدارة", callback_data="admin_panel"))
    
    return kb

def admin_panel_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("📊 إحصائيات سريعة", callback_data="admin_stats"))
    kb.add(InlineKeyboardButton("👥 قائمة المستخدمين", callback_data="admin_users"))
    kb.add(InlineKeyboardButton("👑 إدارة المشرفين", callback_data="manage_admins"))
    kb.add(InlineKeyboardButton("🚫 حظر مستخدمين", callback_data="admin_ban"))
    kb.add(InlineKeyboardButton("📢 إضافة قناة إجبارية", callback_data="add_mandatory"))
    kb.add(InlineKeyboardButton("🗑 إزالة قناة إجبارية", callback_data="remove_mandatory"))
    kb.add(InlineKeyboardButton("🎰 إضافة قناة سحب", callback_data="add_roulette_channel"))
    kb.add(InlineKeyboardButton("🗑 إزالة قناة سحب", callback_data="remove_roulette_channel"))
    kb.add(InlineKeyboardButton("📣 إذاعة للمستخدمين", callback_data="broadcast"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
    return kb

def admins_management_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("➕ إضافة مشرف", callback_data="add_admin"))
    kb.add(InlineKeyboardButton("🗑 إزالة مشرف", callback_data="remove_admin"))
    kb.add(InlineKeyboardButton("📋 قائمة المشرفين", callback_data="admins_list"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel"))
    return kb

def my_channels_kb(user_id):
    user_channels = get_user_channels(user_id)
    kb = InlineKeyboardMarkup(row_width=1)
    
    if user_channels:
        for channel in user_channels:
            kb.add(InlineKeyboardButton(f"📢 @{channel['channel_username']}", callback_data=f"view_channel_{channel['channel_id']}"))
    else:
        kb.add(InlineKeyboardButton("🔗 ربط قناة", callback_data="bind_channel"))
    
    kb.add(InlineKeyboardButton("🔗 ربط قناة جديدة", callback_data="bind_channel"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
    return kb

def channel_selection_kb(user_id):
    user_channels = get_user_channels(user_id)
    kb = InlineKeyboardMarkup(row_width=1)
    
    if user_channels:
        for channel in user_channels:
            kb.add(InlineKeyboardButton(f"📢 @{channel['channel_username']}", callback_data=f"select_{channel['channel_id']}"))
    else:
        kb.add(InlineKeyboardButton("🔗 ربط قناة جديدة", callback_data="bind_channel"))
    
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
    return kb

def get_channel_roulette_markup(roulette_id: str, is_active: bool):
    kb = InlineKeyboardMarkup(row_width=2)
    
    kb.add(InlineKeyboardButton("🎯 انضمام", callback_data=f"join_{roulette_id}"))
    
    kb.row(
        InlineKeyboardButton("⏹ ايقاف انضمام", callback_data=f"stop_{roulette_id}"),
        InlineKeyboardButton("🎁 سحب", callback_data=f"draw_{roulette_id}")
    )
    
    kb.add(InlineKeyboardButton("🔔 ذكرني إذا فزت", callback_data=f"notify_{roulette_id}"))
    
    return kb

def ban_users_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("🚫 حظر مستخدم", callback_data="ban_user"))
    kb.add(InlineKeyboardButton("✅ فك حظر مستخدم", callback_data="unban_user"))
    kb.add(InlineKeyboardButton("📋 قائمة المحظورين", callback_data="banned_list"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel"))
    return kb

def help_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
    return kb

def policy_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
    return kb

def mandatory_channel_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⏩ تخطي", callback_data="skip_mandatory"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
    return kb

# --- دوال مساعدة ---
def is_channel_member(channel_id, user_id):
    try:
        member = bot.get_chat_member(channel_id, user_id)
        return member.status not in ['left', 'kicked']
    except:
        return False

def update_roulette_message(roulette_id: str):
    active_roulettes = get_active_roulettes()
    r = active_roulettes.get(roulette_id)
    if not r:
        return

    try:
        participants_count = len(r['participants'])
        
        footer_text = f"\n\n🎰 <a href='https://t.me/Psx_mpbot'>روليت السر</a>؛ <a href='https://t.me/xg_dev124'>سحوبات السر</a>"
        updated_text = f"<code>👥 عدد المشاركين: {participants_count}</code>\n\n{r['text']}{footer_text}"
        
        bot.edit_message_text(
            chat_id=r['main_channel_id'],
            message_id=r['channel_message_id'],
            text=updated_text,
            parse_mode="HTML",
            reply_markup=get_channel_roulette_markup(roulette_id, r['active'])
        )
    except Exception as e:
        print(f"خطأ في تحديث الروليت: {e}")

def send_broadcast_message(message_text):
    users = data.get('user_data', {})
    success_count = 0
    fail_count = 0
    
    for user_id_str in users.keys():
        try:
            bot.send_message(int(user_id_str), message_text)
            success_count += 1
            time.sleep(0.05)
        except Exception as e:
            if "bot was blocked" in str(e).lower():
                # إشعار بحظر البوت
                user_data = users.get(user_id_str, {})
                notify_user_blocked_bot(
                    int(user_id_str), 
                    user_data.get('username', 'لا يوجد'), 
                    user_data.get('first_name', 'لا يوجد')
                )
            fail_count += 1
    
    return success_count, fail_count

# --- نشر الروليت في قنوات السحوبات ---
def publish_to_roulette_channels(roulette_text, roulette_id, main_channel_username):
    roulette_channels = get_roulette_channels()
    if not roulette_channels:
        return
    
    announcement_text = f"""سحب جديد في قناة: {main_channel_username}
{roulette_text}

🎰 <a href='https://t.me/xg_dev124'>سحوبات السر</a>: أضغط هنا"""
    
    for channel_id, channel_data in roulette_channels.items():
        try:
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("شاهد السحب", url=f"https://t.me/{main_channel_username}"))
            
            bot.send_message(
                chat_id=int(channel_id),
                text=announcement_text,
                parse_mode="HTML",
                reply_markup=kb
            )
        except Exception as e:
            print(f"خطأ في النشر إلى قناة السحوبات: {e}")

# --- المعالجات الرئيسية ---
@bot.message_handler(commands=['start'])
def start_cmd(message: Message):
    user_id = message.from_user.id
    
    if is_user_banned(user_id):
        bot.send_message(message.chat.id, "❌ تم حظرك من استخدام البوت.")
        return
    
    if not get_global_setting('bot_is_active') and not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ البوت متوقف.")
        return

    save_user_data(user_id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    
    if user_id not in ADMIN_IDS and str(user_id) not in data.get('admins', {}):
        notify_admin_new_user(user_id, message.from_user.username, message.from_user.first_name)

    is_joined, not_joined_channels = check_mandatory_join(user_id)
    if not is_joined and not is_admin(user_id):
        kb = InlineKeyboardMarkup()
        for channel_username in not_joined_channels:
            kb.add(InlineKeyboardButton(f"🔗 @{channel_username}", url=f"https://t.me/{channel_username}"))
        kb.add(InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub"))
        bot.send_message(message.chat.id, f"📛 اشترك في القنوات أولاً لاستخدام البوت:", reply_markup=kb)
        return

    user_states.pop(user_id, None)
    
    welcome_text = get_welcome_text(message.from_user.first_name)
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_kb(user_id))

@bot.message_handler(commands=['admin'])
def admin_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return
    bot.send_message(message.chat.id, "⚙️ لوحة الإدارة:", reply_markup=admin_panel_kb())

# --- معالجات Callbacks ---
@bot.callback_query_handler(func=lambda c: c.data == "create_roulette")
def handle_create_roulette(call):
    user_id = call.from_user.id
    
    is_joined, not_joined_channels = check_mandatory_join(user_id)
    if not is_joined and not is_admin(user_id):
        bot.answer_callback_query(call.id, "📛 اشترك في القنوات أولاً!", show_alert=True)
        return
        
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📢 اختر القناة لنشر الروليت:",
        reply_markup=channel_selection_kb(user_id)
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("select_"))
def handle_select_channel(call):
    user_id = call.from_user.id
    channel_id = call.data.split("_")[1]
    
    # البحث عن القناة مباشرة من البيانات المخزنة
    user_channels = get_user_channels(user_id)
    selected_channel = None
    
    for channel in user_channels:
        if str(channel['channel_id']) == str(channel_id):
            selected_channel = channel
            break
    
    if not selected_channel:
        bot.answer_callback_query(call.id, "❌ القناة غير موجودة!", show_alert=True)
        return
    
    # التحقق من أن البوت مشرف في القناة
    if not is_bot_admin_in_channel(int(channel_id)):
        bot.answer_callback_query(call.id, "❌ البوت ليس مشرفاً في هذه القناة!", show_alert=True)
        return
    
    # التحقق من أن المستخدم مشرف في القناة
    try:
        if not is_user_admin_in_channel(int(channel_id), user_id):
            bot.answer_callback_query(call.id, "❌ أنت لست مشرفاً في هذه القناة!", show_alert=True)
            return
    except Exception as e:
        print(f"خطأ في التحقق من صلاحيات المستخدم: {e}")
        bot.answer_callback_query(call.id, "❌ حدث خطأ في التحقق من الصلاحيات!", show_alert=True)
        return
    
    user_temp_data[user_id] = {
        'main_channel_id': selected_channel['channel_id'],
        'main_channel_username': selected_channel['channel_username']
    }
    
    bot.answer_callback_query(call.id, "✅ تم اختيار القناة!")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="✍️ أرسل كليشة الروليت:"
    )
    user_states[user_id] = 'awaiting_text'

@bot.callback_query_handler(func=lambda c: c.data == "bind_channel")
def handle_bind_channel(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🔗 أضف البوت مشرف في قناتك ثم أعد توجيه رسالة أو أرسل رابط القناة:"
    )
    user_states[user_id] = 'awaiting_channel'

@bot.callback_query_handler(func=lambda c: c.data == "my_channels")
def handle_my_channels(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    user_channels = get_user_channels(user_id)
    
    if user_channels:
        channels_text = "📺 قنواتك:\n\n"
        for i, channel in enumerate(user_channels, 1):
            channels_text += f"{i}. @{channel['channel_username']}\n"
        channels_text += f"\n📊 إجمالي القنوات: {len(user_channels)}"
    else:
        channels_text = "📺 لم تقم بربط أي قناة بعد."
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=channels_text,
        reply_markup=my_channels_kb(user_id)
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("view_channel_"))
def handle_view_channel(call):
    user_id = call.from_user.id
    channel_id = call.data.split("_")[2]
    
    user_channels = get_user_channels(user_id)
    for channel in user_channels:
        if str(channel['channel_id']) == str(channel_id):
            bot.answer_callback_query(call.id, f"القناة: @{channel['channel_username']}", show_alert=True)
            return
    
    bot.answer_callback_query(call.id, "❌ القناة غير موجودة!", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data == "help")
def handle_help(call):
    bot.answer_callback_query(call.id)
    help_text = """❓ **مساعدة**

🎯 كيفية إنشاء روليت:
1. اضغط على "ابدأ روليت"
2. اختر القناة (يجب أن يكون البوت مشرفاً)
3. أرسل كليشة الروليت
4. حدد عدد الفائزين
5. أضف قناة شرط (اختياري)
6. انشر الروليت

📝 ملاحظات:
- يمكنك ربط أكثر من قناة
- يجب أن تكون مشرفاً في القناة
- يمكنك المشاركة في روليت الآخرين
- سيتم إشعارك إذا فزت"""
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=help_text,
        parse_mode="Markdown",
        reply_markup=help_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data == "usage_policy")
def handle_usage_policy(call):
    bot.answer_callback_query(call.id)
    policy_text = """📜 **سياسة الاستخدام**

1. الالتزام بآداب المحادثة
2. عدم انشاء سحوبات مخالفة
3. يحق للإدارة حظر أي مستخدم
4. السحوبات للمشتركين في القنات فقط

⚠️ أي مخالفة تؤدي إلى الحظر الفوري"""
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=policy_text,
        parse_mode="Markdown",
        reply_markup=policy_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data == "check_sub")
def handle_check_sub(call):
    user_id = call.from_user.id
    is_joined, not_joined_channels = check_mandatory_join(user_id)
    
    if is_joined:
        mark_user_subscribed(user_id)
        bot.answer_callback_query(call.id, "✅ تم الاشتراك!", show_alert=True)
        
        welcome_text = get_welcome_text(call.from_user.first_name)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=welcome_text,
            reply_markup=main_menu_kb(user_id)
        )
    else:
        bot.answer_callback_query(call.id, f"❌ لم تشترك بعد", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data == "back_main")
def handle_back_main(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    user_states.pop(user_id, None)
    
    welcome_text = get_welcome_text(call.from_user.first_name)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=welcome_text,
        reply_markup=main_menu_kb(user_id)
    )

@bot.callback_query_handler(func=lambda c: c.data == "skip_mandatory")
def handle_skip_mandatory(call):
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)
    user_temp_data[user_id]['mandatory_channel'] = None
    publish_roulette(user_id)
    user_states.pop(user_id, None)
    user_temp_data.pop(user_id, None)

# --- معالجات الإدارة ---
@bot.callback_query_handler(func=lambda c: c.data == "admin_panel")
def handle_admin_panel(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="⚙️ لوحة الإدارة:",
        reply_markup=admin_panel_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data == "admin_stats")
def handle_admin_stats(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    total_users = get_users_count()
    active_roulettes_count = len(get_active_roulettes())
    mandatory_channels_count = get_mandatory_channels_count()
    banned_users_count = len(get_banned_users())
    roulette_channels_count = get_roulette_channels_count()
    admins_count = get_admins_count()
    
    total_user_channels = 0
    user_channels_data = data.get('user_channels', {})
    for user_id_str, channels in user_channels_data.items():
        total_user_channels += len(channels)
    
    stats_text = f"""📊 **الإحصائيات:**

👥 المستخدمين: {total_users}
🎯 الروليت النشطة: {active_roulettes_count}
📢 القنوات الإجبارية: {mandatory_channels_count}
🎰 قنوات السحوبات: {roulette_channels_count}
🚫 المستخدمين المحظورين: {banned_users_count}
📺 القنوات المرتبطة: {total_user_channels}
👑 المشرفين المضافين: {admins_count}"""
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=stats_text,
        parse_mode="Markdown",
        reply_markup=admin_panel_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data == "admin_users")
def handle_admin_users(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    users = data.get('user_data', {})
    if not users:
        bot.answer_callback_query(call.id, "❌ لا يوجد مستخدمين.", show_alert=True)
        return
    
    users_text = "👥 **آخر 10 مستخدمين:**\n\n"
    for i, (user_id, user_data) in enumerate(list(users.items())[-10:], 1):
        username = f"@{user_data['username']}" if user_data['username'] else "لا يوجد"
        name = user_data['first_name'] or "لا يوجد"
        users_text += f"{i}. {name} ({username}) - {user_id}\n"
    
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel"))
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=users_text,
        parse_mode="Markdown",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data == "manage_admins")
def handle_manage_admins(call):
    user_id = call.from_user.id
    if user_id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ فقط المطور يمكنه إدارة المشرفين!", show_alert=True)
        return
        
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="👑 **إدارة المشرفين:**",
        parse_mode="Markdown",
        reply_markup=admins_management_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data == "add_admin")
def handle_add_admin(call):
    user_id = call.from_user.id
    if user_id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ فقط المطور يمكنه إضافة مشرفين!", show_alert=True)
        return
        
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="👑 أرسل أيدي المستخدم الذي تريد جعله مشرف:"
    )
    user_states[user_id] = 'awaiting_add_admin'

@bot.callback_query_handler(func=lambda c: c.data == "remove_admin")
def handle_remove_admin(call):
    user_id = call.from_user.id
    if user_id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ فقط المطور يمكنه إزالة مشرفين!", show_alert=True)
        return
        
    admins = get_admins()
    if not admins:
        bot.answer_callback_query(call.id, "❌ لا يوجد مشرفين مضافين.", show_alert=True)
        return
    
    kb = InlineKeyboardMarkup()
    for admin_id, admin_data in admins.items():
        username = f"@{admin_data['username']}" if admin_data['username'] else "لا يوجد يوزر"
        name = admin_data['first_name'] or "لا يوجد اسم"
        kb.add(InlineKeyboardButton(f"{name} ({username})", callback_data=f"remove_admin_{admin_id}"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="manage_admins"))
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🗑 اختر المشرف الذي تريد إزالته:",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("remove_admin_"))
def handle_remove_admin_confirm(call):
    user_id = call.from_user.id
    if user_id not in ADMIN_IDS:
        bot.answer_callback_query(call.id, "❌ فقط المطور يمكنه إزالة مشرفين!", show_alert=True)
        return
        
    admin_id = call.data.split("_")[2]
    remove_admin(admin_id)
    bot.answer_callback_query(call.id, "✅ تم إزالة المشرف!", show_alert=True)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="👑 **إدارة المشرفين:**",
        parse_mode="Markdown",
        reply_markup=admins_management_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data == "admins_list")
def handle_admins_list(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    admins = get_admins()
    if not admins:
        admins_text = "👑 **لا يوجد مشرفين مضافين.**"
    else:
        admins_text = "👑 **قائمة المشرفين المضافين:**\n\n"
        for i, (admin_id, admin_data) in enumerate(admins.items(), 1):
            username = f"@{admin_data['username']}" if admin_data['username'] else "لا يوجد يوزر"
            name = admin_data['first_name'] or "لا يوجد اسم"
            added_by = admin_data['added_by']
            added_date = admin_data['added_date']
            admins_text += f"{i}. {name} ({username})\n🆔 الأيدي: {admin_id}\n⏰ تاريخ الإضافة: {added_date}\n\n"
    
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="manage_admins"))
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=admins_text,
        parse_mode="Markdown",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data == "admin_ban")
def handle_admin_ban(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🚫 **إدارة الحظر:**",
        parse_mode="Markdown",
        reply_markup=ban_users_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data == "ban_user")
def handle_ban_user(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🚫 أرسل أيدي المستخدم لحظره:"
    )
    user_states[user_id] = 'awaiting_ban_user'

@bot.callback_query_handler(func=lambda c: c.data == "unban_user")
def handle_unban_user(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="✅ أرسل أيدي المستخدم لفك حظره:"
    )
    user_states[user_id] = 'awaiting_unban_user'

@bot.callback_query_handler(func=lambda c: c.data == "banned_list")
def handle_banned_list(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    banned_users = get_banned_users()
    if not banned_users:
        users_text = "✅ لا يوجد مستخدمين المحظورين."
    else:
        users_text = "🚫 **المستخدمين المحظورين:**\n\n"
        for i, (user_id, ban_data) in enumerate(banned_users.items(), 1):
            users_text += f"{i}. {user_id} - {ban_data['banned_date']}\n"
    
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="admin_ban"))
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=users_text,
        parse_mode="Markdown",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data == "add_mandatory")
def handle_add_mandatory(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📢 أعد توجيه رسالة من القناة التي تريد إضافتها إجبارية:"
    )
    user_states[user_id] = 'awaiting_mandatory_channel'

@bot.callback_query_handler(func=lambda c: c.data == "remove_mandatory")
def handle_remove_mandatory(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    mandatory_channels = get_mandatory_channels()
    if not mandatory_channels:
        bot.answer_callback_query(call.id, "❌ لا توجد قنوات إجبارية.", show_alert=True)
        return
    
    kb = InlineKeyboardMarkup()
    for channel_id, channel_data in mandatory_channels.items():
        kb.add(InlineKeyboardButton(f"@{channel_data['username']}", callback_data=f"remove_mandatory_{channel_id}"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel"))
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🗑 اختر القناة التي تريد إزالتها:",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("remove_mandatory_"))
def handle_remove_mandatory_channel(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    channel_id = call.data.split("_")[2]
    remove_mandatory_channel(channel_id)
    bot.answer_callback_query(call.id, "✅ تم إزالة القناة الإجبارية!", show_alert=True)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="⚙️ لوحة الإدارة:",
        reply_markup=admin_panel_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data == "add_roulette_channel")
def handle_add_roulette_channel(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🎰 أعد توجيه رسالة من قناة السحوبات:"
    )
    user_states[user_id] = 'awaiting_roulette_channel'

@bot.callback_query_handler(func=lambda c: c.data == "remove_roulette_channel")
def handle_remove_roulette_channel(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    roulette_channels = get_roulette_channels()
    if not roulette_channels:
        bot.answer_callback_query(call.id, "❌ لا توجد قنوات سحوبات.", show_alert=True)
        return
    
    kb = InlineKeyboardMarkup()
    for channel_id, channel_data in roulette_channels.items():
        kb.add(InlineKeyboardButton(f"@{channel_data['username']}", callback_data=f"remove_roulette_{channel_id}"))
    kb.add(InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel"))
    
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🗑 اختر قناة السحوبات التي تريد إزالتها:",
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("remove_roulette_"))
def handle_remove_roulette_channel_confirm(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    channel_id = call.data.split("_")[2]
    remove_roulette_channel(channel_id)
    bot.answer_callback_query(call.id, "✅ تم إزالة قناة السحوبات!", show_alert=True)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="⚙️ لوحة الإدارة:",
        reply_markup=admin_panel_kb()
    )

@bot.callback_query_handler(func=lambda c: c.data == "broadcast")
def handle_broadcast(call):
    user_id = call.from_user.id
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ لست أدمن.", show_alert=True)
        return
        
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📣 أرسل نص الإذاعة:"
    )
    user_states[user_id] = 'awaiting_broadcast'

# --- معالجات الروليت ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("join_"))
def handle_join_roulette(call):
    user_id = call.from_user.id
    roulette_id = call.data.split("_")[1]
    
    if is_user_banned(user_id):
        bot.answer_callback_query(call.id, "❌ تم حظرك من المشاركة!", show_alert=True)
        return
    
    active_roulettes = get_active_roulettes()
    if roulette_id not in active_roulettes:
        bot.answer_callback_query(call.id, "❌ الروليت انتهت!", show_alert=True)
        return
    
    roulette = active_roulettes[roulette_id]
    
    if not roulette['active']:
        bot.answer_callback_query(call.id, "❌ الروليت متوقفة!", show_alert=True)
        return
    
    if user_id == roulette['creator_id']:
        bot.answer_callback_query(call.id, "❌ لا يمكنك المشاركة!", show_alert=True)
        return
    
    if str(user_id) not in roulette['participants']:
        roulette['participants'].append(str(user_id))
        save_roulette(roulette_id, roulette)
        update_roulette_message(roulette_id)
        bot.answer_callback_query(call.id, "✅ تمت المشاركة!", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "✅ أنت مشارك!", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data.startswith("notify_"))
def handle_notify_win(call):
    user_id = call.from_user.id
    roulette_id = call.data.split("_")[1]
    bot.answer_callback_query(call.id, "✅ سيتم إشعارك إذا فزت! 🔔", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data.startswith("stop_"))
def handle_stop_roulette(call):
    user_id = call.from_user.id
    roulette_id = call.data.split("_")[1]
    
    active_roulettes = get_active_roulettes()
    if roulette_id not in active_roulettes:
        bot.answer_callback_query(call.id, "❌ الروليت انتهت!", show_alert=True)
        return
    
    roulette = active_roulettes[roulette_id]
    
    if user_id != roulette['creator_id'] and not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ فقط المنشئ يمكنه إيقاف الروليت!", show_alert=True)
        return
    
    roulette['active'] = False
    save_roulette(roulette_id, roulette)
    update_roulette_message(roulette_id)
    bot.answer_callback_query(call.id, "✅ تم إيقاف المشاركة! ⏹", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data.startswith("draw_"))
def handle_start_draw(call):
    user_id = call.from_user.id
    roulette_id = call.data.split("_")[1]
    
    active_roulettes = get_active_roulettes()
    if roulette_id not in active_roulettes:
        bot.answer_callback_query(call.id, "❌ الروليت انتهت!", show_alert=True)
        return
    
    roulette = active_roulettes[roulette_id]
    
    if user_id != roulette['creator_id'] and not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ فقط المنشئ يمكنه السحب!", show_alert=True)
        return
    
    if not roulette['participants']:
        bot.answer_callback_query(call.id, "❌ لا يوجد مشاركين!", show_alert=True)
        return
    
    participants = roulette['participants']
    winners_count = min(roulette['winners_count'], len(participants))
    winners = random.sample(participants, winners_count)
    
    roulette['winners'] = winners
    roulette['active'] = False
    save_roulette(roulette_id, roulette)
    
    # إنشاء نص الفائزين مع روابط صحيحة
    winners_text = "🏆 **الفائزون في الروليت هم:**\n\n"
    for i, winner_id in enumerate(winners, 1):
        try:
            winner_chat = bot.get_chat(int(winner_id))
            username = f"@{winner_chat.username}" if winner_chat.username else "لا يوجد يوزر"
            name = winner_chat.first_name or "لا يوجد اسم"
            # استخدام رابط المستخدم الصحيح
            winners_text += f"{i}. [{name}](tg://user?id={winner_id}) | {username}\n"
        except Exception as e:
            print(f"خطأ في جلب بيانات الفائز: {e}")
            winners_text += f"{i}. المستخدم {winner_id}\n"
    
    try:
        # إرسال رسالة بالرد على رسالة الروليت الأصلية
        bot.send_message(
            roulette['main_channel_id'],
            winners_text,
            parse_mode="Markdown",
            reply_to_message_id=roulette['channel_message_id']
        )
    except Exception as e:
        print(f"خطأ في إرسال رسالة الفائزين: {e}")
        # محاولة بديلة بدون رد
        try:
            bot.send_message(
                roulette['main_channel_id'],
                winners_text,
                parse_mode="Markdown"
            )
        except:
            pass
    
    update_roulette_message(roulette_id)
    
    for winner_id in winners:
        try:
            bot.send_message(winner_id, "🎉 **مبروك! لقد فزت في الروليت** 🎉")
        except Exception as e:
            if "bot was blocked" in str(e).lower():
                # إشعار بحظر البوت من الفائز
                try:
                    winner_chat = bot.get_chat(int(winner_id))
                    notify_user_blocked_bot(
                        int(winner_id), 
                        winner_chat.username if winner_chat.username else 'لا يوجد',
                        winner_chat.first_name or 'لا يوجد'
                    )
                except:
                    pass
    
    bot.answer_callback_query(call.id, f"✅ تم سحب {winners_count} فائز! 🎁", show_alert=True)

# --- معالج الرسائل ---
@bot.message_handler(content_types=['text'])
def handle_messages(message: Message):
    user_id = message.from_user.id
    current_state = user_states.get(user_id)
    
    if current_state == 'awaiting_channel':
        channel_id = None
        channel_username = None
        
        if message.forward_from_chat and message.forward_from_chat.type == "channel":
            channel = message.forward_from_chat
            channel_id = channel.id
            channel_username = channel.username
        elif message.text.startswith('@'):
            channel_username = message.text.replace('@', '').strip()
            try:
                chat = bot.get_chat(f"@{channel_username}")
                if chat.type == "channel":
                    channel_id = chat.id
                    channel_username = chat.username
            except:
                pass
        elif 't.me/' in message.text:
            try:
                username = message.text.split('t.me/')[-1].split('/')[0]
                chat = bot.get_chat(f"@{username}")
                if chat.type == "channel":
                    channel_id = chat.id
                    channel_username = chat.username
            except:
                pass
        
        if channel_id and channel_username:
            if not is_bot_admin_in_channel(channel_id):
                bot.send_message(message.chat.id, "❌ البوت ليس مشرفاً في هذه القناة! أضف البوت كمسؤول أولاً.")
                return
            
            if add_user_channel(user_id, channel_id, channel_username):
                bot.send_message(message.chat.id, f"✅ تم ربط القناة: @{channel_username}")
            else:
                bot.send_message(message.chat.id, f"✅ القناة مضافة مسبقاً: @{channel_username}")
            
            user_states.pop(user_id, None)
            
            welcome_text = get_welcome_text(message.from_user.first_name)
            bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_kb(user_id))
        else:
            bot.send_message(message.chat.id, "❌ أعد توجيه رسالة من قناة أو أرسل رابط القناة!")

    elif current_state == 'awaiting_text':
        user_temp_data[user_id]['roulette_text'] = message.text
        bot.send_message(message.chat.id, "📝 عدد الفائزين:")
        user_states[user_id] = 'awaiting_winners'

    elif current_state == 'awaiting_winners':
        try:
            count = int(message.text)
            if count > 0:
                user_temp_data[user_id]['winners_count'] = count
                bot.send_message(message.chat.id, "📢 أعد توجيه رسالة من قناة الشرط أو اضغط تخطي:", reply_markup=mandatory_channel_kb())
                user_states[user_id] = 'awaiting_mandatory'
            else:
                bot.send_message(message.chat.id, "❌ أدخل رقم صحيح!")
        except:
            bot.send_message(message.chat.id, "❌ أدخل رقم صحيح!")

    elif current_state == 'awaiting_mandatory':
        if message.forward_from_chat and message.forward_from_chat.type == "channel":
            channel = message.forward_from_chat
            user_temp_data[user_id]['mandatory_channel'] = {
                'channel_id': channel.id,
                'channel_username': channel.username
            }
            publish_roulette(user_id)
            user_states.pop(user_id, None)
            user_temp_data.pop(user_id, None)
        else:
            bot.send_message(message.chat.id, "❌ أعد توجيه رسالة من قناة أو اضغط تخطي!")

    elif current_state == 'awaiting_ban_user':
        if not is_admin(user_id):
            return
            
        try:
            user_to_ban = int(message.text)
            ban_user(user_to_ban)
            bot.send_message(message.chat.id, f"✅ تم حظر المستخدم: {user_to_ban}")
            user_states.pop(user_id, None)
        except:
            bot.send_message(message.chat.id, "❌ أدخل أيدي صحيح!")

    elif current_state == 'awaiting_unban_user':
        if not is_admin(user_id):
            return
            
        try:
            user_to_unban = int(message.text)
            unban_user(user_to_unban)
            bot.send_message(message.chat.id, f"✅ تم فك حظر المستخدم: {user_to_unban}")
            user_states.pop(user_id, None)
        except:
            bot.send_message(message.chat.id, "❌ أدخل أيدي صحيح!")

    elif current_state == 'awaiting_mandatory_channel':
        if not is_admin(user_id):
            return
            
        if message.forward_from_chat and message.forward_from_chat.type == "channel":
            channel = message.forward_from_chat
            try:
                bot_member = bot.get_chat_member(channel.id, bot.get_me().id)
                if bot_member.status in ['administrator', 'creator']:
                    add_mandatory_channel(channel.id, channel.username)
                    bot.send_message(message.chat.id, f"✅ تم إضافة القناة الإجبارية: @{channel.username}")
                    user_states.pop(user_id, None)
                else:
                    bot.send_message(message.chat.id, "❌ البوت ليس مشرفاً في القناة!")
            except:
                bot.send_message(message.chat.id, "❌ خطأ في إضافة القناة!")
        else:
            bot.send_message(message.chat.id, "❌ أعد توجيه رسالة من قناة!")

    elif current_state == 'awaiting_roulette_channel':
        if not is_admin(user_id):
            return
            
        if message.forward_from_chat and message.forward_from_chat.type == "channel":
            channel = message.forward_from_chat
            try:
                bot_member = bot.get_chat_member(channel.id, bot.get_me().id)
                if bot_member.status in ['administrator', 'creator']:
                    add_roulette_channel(channel.id, channel.username)
                    bot.send_message(message.chat.id, f"✅ تم إضافة قناة السحوبات: @{channel.username}")
                    user_states.pop(user_id, None)
                else:
                    bot.send_message(message.chat.id, "❌ البوت ليس مشرفاً في القناة!")
            except:
                bot.send_message(message.chat.id, "❌ خطأ في إضافة القناة!")
        else:
            bot.send_message(message.chat.id, "❌ أعد توجيه رسالة من قناة!")

    elif current_state == 'awaiting_broadcast':
        if not is_admin(user_id):
            return
            
        processing_msg = bot.send_message(message.chat.id, "🔄 جاري إرسال الإذاعة للمستخدمين...")
        
        success_count, fail_count = send_broadcast_message(message.text)
        
        result_text = f"✅ تمت الإذاعة بنجاح!\n\n✅ تم الإرسال: {success_count}\n❌ فشل الإرسال: {fail_count}"
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=processing_msg.message_id,
            text=result_text
        )
        
        user_states.pop(user_id, None)

    elif current_state == 'awaiting_add_admin':
        if user_id not in ADMIN_IDS:
            return
            
        try:
            new_admin_id = int(message.text)
            # الحصول على بيانات المستخدم
            try:
                new_admin_chat = bot.get_chat(new_admin_id)
                username = new_admin_chat.username
                first_name = new_admin_chat.first_name
            except:
                username = None
                first_name = "غير معروف"
            
            add_admin(new_admin_id, user_id, username, first_name)
            bot.send_message(message.chat.id, f"✅ تم إضافة المشرف الجديد!\n\n👤 الاسم: {first_name}\n📱 اليوزر: @{username if username else 'لا يوجد'}\n🆔 الأيدي: {new_admin_id}")
            user_states.pop(user_id, None)
        except ValueError:
            bot.send_message(message.chat.id, "❌ أدخل أيدي صحيح!")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ حدث خطأ: {e}")

def publish_roulette(user_id: int):
    data = user_temp_data.get(user_id)
    if not data:
        return

    roulette_id = str(uuid.uuid4())
    
    footer_text = f"\n\n🎰 <a href='https://t.me/Psx_mpbot'>روليت السر</a>؛ <a href='https://t.me/xg_dev124'>سحوبات السر</a>"
    initial_text = f"<code>👥 عدد المشاركين: 0</code>\n\n{data['roulette_text']}{footer_text}"
    
    try:
        channel_message = bot.send_message(
            chat_id=data['main_channel_id'],
            text=initial_text,
            parse_mode="HTML",
            reply_markup=get_channel_roulette_markup(roulette_id, True)
        )
    except Exception as e:
        bot.send_message(user_id, f"❌ فشل النشر! تأكد أن البوت مشرف في القناة.")
        return

    roulette_data = {
        'creator_id': user_id,
        'main_channel_id': data['main_channel_id'],
        'main_channel_username': data['main_channel_username'],
        'channel_message_id': channel_message.message_id,
        'text': data['roulette_text'],
        'winners_count': data['winners_count'],
        'participants': [],
        'active': True,
        'winners': [],
        'mandatory_channel': data.get('mandatory_channel')
    }
    
    save_roulette(roulette_id, roulette_data)
    
    publish_to_roulette_channels(data['roulette_text'], roulette_id, data['main_channel_username'])
    
    user_info = data.get('user_data', {}).get(str(user_id), {})
    notify_new_roulette(
        user_id, 
        user_info.get('username', 'لا يوجد'), 
        user_info.get('first_name', 'لا يوجد'), 
        data['main_channel_username'],
        data['main_channel_id']
    )
    
    bot.send_message(user_id, f"✅ تم النشر في @{data['main_channel_username']}")

# --- التشغيل ---
set_bot_commands()
print("🚀 البوت شغال بسرعة فائقة!")
print("✅ تم إضافة نظام إدارة المشرفين")
print("🎯 جميع الأزرار تعمل")
print("📢 ربط أكثر من قناة")
print("⚡ سرعة استجابة عالية")
print("🔔 إشعارات جديدة للمطور")
print("🏆 روابط الفائزين صحيحة")
print("🚫 إشعارات حظر البوت")
print("👑 نظام المشرفين المضافين")

while True:
    try:
        bot.infinity_polling(timeout=30, long_polling_timeout=10)
    except Exception as e:
        print(f"⚠️ إعادة الاتصال: {e}")
        time.sleep(2)