# bot_v2/bot/handlers/admin/stats.py
# Contains handlers for displaying global and user-specific statistics.

import os
import time
import asyncio
from datetime import datetime, timedelta
from io import BytesIO
from telethon import events
from telethon.tl.custom import Button
from typing import TYPE_CHECKING, Dict, Any, List, Optional

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_all_users, load_bots_data
from bot.core.state import conversation_manager
from bot.services.telegram import get_user_info
from bot.core.database import (
    get_total_stat, 
    count_events, 
    get_global_total_stat, 
    count_global_events,
    get_user_stat_names
)

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status
from bot.services.image_service import generate_stats_dashboard
from bot.handlers.admin.marketplace_stats import get_marketplace_stats

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message
from bot.utils.time import _TZ, _now_ts, _start_of_day, _start_of_week, _start_of_month, _start_of_year

# Local Imports from bot_v2 handlers (for now, will be refactored later)


# --- UI Functions ---
async def send_stats_menu(event: events.CallbackQuery.Event):
    text = "**📊 قسم الإحصائيات المتقدمة**\n\nاختر نوع التقارير التي تود إصدارها الآن:"
    buttons = [
        [Button.inline("📈 تقرير نصي شامل", data='admin:global_stats')],
        [Button.inline("🖼️ إصدار لوحة بيانات (Image)", data='admin:generate_stats_image')],
        [Button.inline("👤 إحصائيات مستخدم محدد", data='admin:user_stats')],
        [Button.inline("⬅️ رجوع", data='admin:main_menu')]
    ]
    await safe_edit_message(event, text, buttons=buttons)


# --- Callbacks ---

async def stats_menu_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    await send_stats_menu(event)


async def global_stats_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)

    users = load_all_users()
    total_users = len(users)
    bots_data = load_bots_data()
    running_bots = sum(1 for t, info in bots_data.items() if info.get('status') == 'running')
    total_bots = len(bots_data)

    now_ts = _now_ts()
    day_start = _start_of_day(now_ts)
    week_start = _start_of_week(now_ts)
    month_start = _start_of_month(now_ts)

    async def ev_count(key, start):
        return await count_global_events(stat_name=key, start_ts=start, end_ts=now_ts)

    def fmt(n):
        try: return f"{int(n):,}"
        except: return str(n)

    # --- Header ---
    ts_display = datetime.fromtimestamp(now_ts, _TZ).strftime("%Y-%m-%d | %I:%M %p")
    text = f"📊 <b>التقرير الإحصائي الشامل للنظام</b> 📊\n"
    text += f"📅 تاريخ التقرير: <code>{ts_display}</code>\n"
    text += "━━━━━━━━━━━━━━━━━━━━\n\n"

    # --- Section: Users ---
    j_d = await ev_count('user_join', day_start)
    j_w = await ev_count('user_join', week_start)
    j_m = await ev_count('user_join', month_start)
    
    text += f"👥 <b>إدارة المستخدمين والمرور:</b>\n"
    text += f"🔘 إجمالي الأعضاء: <code>{fmt(total_users)}</code> مستخدم\n"
    text += f"   ├── انضمام اليوم: <code>+{fmt(j_d)}</code> 📈\n"
    text += f"   ├── انضمام الأسبوع: <code>+{fmt(j_w)}</code> ✨\n"
    text += f"   └── انضمام الشهر: <code>+{fmt(j_m)}</code> 🏆\n\n"

    # --- Section: Bot Infrastructure ---
    s_d = await ev_count('bots_started', day_start)
    s_w = await ev_count('bots_started', week_start)
    
    text += f"🤖 <b>البنية التحتية للبوتات:</b>\n"
    text += f"🔘 البوتات المسجلة: <code>{fmt(total_bots)}</code> بوت\n"
    text += f"🔘 البوتات النشطة: <code>{fmt(running_bots)}</code> (قيد العمل حالياً) ✅\n"
    text += f"   ├── تشغيل (اليوم): <code>+{fmt(s_d)}</code> ▶️\n"
    text += f"   └── تشغيل (الأسبوع): <code>+{fmt(s_w)}</code> 🔥\n\n"

    # --- Section: File Operations ---
    u_total = await get_global_total_stat('file_uploads')
    u_d = await ev_count('file_uploads', day_start)
    u_w = await ev_count('file_uploads', week_start)
    
    c_total = await get_global_total_stat('folders_created')
    c_d = await ev_count('folders_created', day_start)

    text += f"📂 <b>إدارة المحتوى والملفات:</b>\n"
    text += f"🔘 إجمالي الملفات: <code>{fmt(u_total)}</code> ملف\n"
    text += f"   ├── رفع اليوم: <code>+{fmt(u_d)}</code> 📥\n"
    text += f"   └── رفع الأسبوع: <code>+{fmt(u_w)}</code> 📤\n"
    text += f"🔘 إجمالي المجلدات: <code>{fmt(c_total)}</code> مجلد\n"
    text += f"   └── إنشاء اليوم: <code>+{fmt(c_d)}</code> 📁\n\n"

    text += "━━━━━━━━━━━━━━━━━━━━\n"
    text += f"✨ <i>توقيع النظام: BotManager Pro Dashboard</i>"

    back_button = Button.inline("⬅️ رجوع للمنيو", data="admin:stats_menu")
    image_button = Button.inline("🖼️ إصدار لوحة البيانات (Image)", data="admin:generate_stats_image")
    
    await safe_edit_message(event, text, buttons=[[image_button], [back_button]], parse_mode='html')


async def generate_stats_image_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)

    await event.answer("🎨 جاري توليد لوحة البيانات الاحترافية (Ultra-Premium)...", cache_time=0)
    
    try:
        # 1. Get Bot Info & Avatar
        me = await client.get_me()
        bot_name = f"{me.first_name} {me.last_name or ''}".strip()
        bot_username = me.username
        
        # Download avatar to temp path
        avatar_path = f"/tmp/bot_avatar_{me.id}.jpg"
        if not os.path.exists(avatar_path):
            await client.download_profile_photo('me', file=avatar_path)

        # 2. Fetch rich data metrics
        users = load_all_users()
        bots_data = load_bots_data()
        mp_stats = await get_marketplace_stats()
        
        now = _now_ts()
        d_s = _start_of_day(now)
        w_s = _start_of_week(now)
        m_s = _start_of_month(now)

        async def count_ev(k, s): return await count_global_events(stat_name=k, start_ts=s, end_ts=now)

        stats_data = {
            'users_total': len(users),
            'joins_day': await count_ev('user_join', d_s),
            'joins_week': await count_ev('user_join', w_s),
            'joins_month': await count_ev('user_join', m_s),
            
            'bots_total': len(bots_data),
            'bots_active': sum(1 for t, info in bots_data.items() if info.get('status') == 'running'),
            'starts_day': await count_ev('bots_started', d_s),
            'starts_week': await count_ev('bots_started', w_s),
            
            'files_total': await get_global_total_stat('file_uploads'),
            'uploads_day': await count_ev('file_uploads', d_s),
            'uploads_week': await count_ev('file_uploads', w_s),
            'folders_total': await get_global_total_stat('folders_created'),
            
            # Marketplace Integration
            'mp_total_products': mp_stats.get('total_products', 0),
            'mp_total_downloads': mp_stats.get('total_downloads', 0),
            'mp_today_products': mp_stats.get('today_products', 0),
            'mp_today_downloads': mp_stats.get('today_downloads', 0)
        }

        # 3. Generate dynamic ultra-premium image
        image_stream = await asyncio.to_thread(
            generate_stats_dashboard, 
            stats_data, 
            bot_name=bot_name,
            bot_username=bot_username,
            avatar_path=avatar_path if os.path.exists(avatar_path) else None
        )
        
        # 4. Send to user
        caption = (
            f"💎 <b>لوحة إدارة النظام — الإصدار الفاخر</b>\n\n"
            f"🤖 البوت: <b>{bot_name}</b> (@{bot_username})\n"
            f"🕒 تم التوليد: <code>{datetime.now().strftime('%Y-%m-%d %I:%M %p')}</code>\n"
            f"👤 المسؤول: <a href=\"tg://user?id={sender_id}\">{event.sender.first_name}</a>\n\n"
            f"✨ <i>بيانات حية، دقيقة، ومؤمنة بالكامل</i>"
        )
        
        await client.send_file(
            sender_id, 
            image_stream, 
            caption=caption
        )
        
        # Cleanup avatar after some time or immediately
        if os.path.exists(avatar_path):
            try: os.remove(avatar_path)
            except: pass

    except Exception as e:
        print(f"Error generating ultra-premium stats image: {e}")
        import traceback
        traceback.print_exc()
        await event.answer(f"❌ فشل توليد اللوحة الفاخرة: {e}", alert=True)

async def stats_download_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)

    cached_state = conversation_manager.get_state(sender_id)
    cached_full_text = cached_state.get('context', {}).get('last_stats_text')

    if not cached_full_text:
        await event.answer("❗ لا توجد تفاصيل محفوظة. اضغط على 'الإحصائيات' مرة أخرى للحصول على التفاصيل.", alert=True)
    else:
        bio = BytesIO(cached_full_text.encode('utf-8'))
        bio.name = f"bot_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            await client.send_file(sender_id, bio, caption="📄 تفاصيل الإحصائيات — ملف نصي")
            back_button = Button.inline("◀️ رجوع", data="admin:main_menu")
            await safe_edit_message(event, "📄 تم إرسال ملف التفاصيل في المحادثة الخاصة.", buttons=[[back_button]])
        except Exception as e:
            await event.answer(f"⚠️ حدث خطأ أثناء إرسال الملف: {e}", alert=True)
        # Clear cached stats after sending
        if 'context' in cached_state and 'last_stats_text' in cached_state['context']:
            del cached_state['context']['last_stats_text']
            conversation_manager.set_state(sender_id, cached_state.get('status'), context=cached_state.get('context'), message_id=cached_state.get('message_id')) # Update state without the text


async def user_stats_prompt(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    conversation_manager.set_state(sender_id, "awaiting_user_for_stats", message_id=event.message_id)
    await safe_edit_message(event, "**👤 إحصائيات عضو معين**\n\nأرسل الآن ID المستخدم، أو اليوزرنيم، أو قم بالرد على رسالته.", buttons=[[Button.inline("إلغاء ❌", data="admin:cancel_action")]])


# --- Conversation Handler ---
async def admin_stats_conversation_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    state_data = conversation_manager.get_state(sender_id)
    state_status = state_data.get('status')
    message_id_to_edit = state_data.get('message_id')

    # A helper function to restore the panel after an action
    async def restore_panel(menu_function_to_call):
        if message_id_to_edit:
            try:
                mock_event = await event.client.get_messages(sender_id, ids=message_id_to_edit)
                if mock_event:
                    await menu_function_to_call(mock_event)
            except Exception as e:
                print(f"Error restoring panel: {e}")
                await event.reply("اكتمل الإجراء.")

    # --- USER STATS ---
    if state_status == "awaiting_user_for_stats":
        user_input = event.text
        if event.is_reply:
            reply = await event.get_reply_message()
            user_input = reply.sender_id
        user_info = await get_user_info(user_input)
        if not user_info:
            await event.reply("❌ لم أتمكن من العثور على هذا المستخدم.")
        else:
            user_id = user_info['id']
            user_id_str = str(user_id)

            # compute period starts
            now = _now_ts()
            day_start = _start_of_day()
            week_start = _start_of_week()
            month_start = _start_of_month()
            year_start = _start_of_year()

            def fmt(n):
                try:
                    return f"{int(n):,}"
                except:
                    return str(n)

            stat_keys = await get_user_stat_names(user_id)
            
            if not stat_keys:
                await event.reply(f"**لا توجد إحصائيات مسجلة للمستخدم:** [{user_info['first_name']}](tg://user?id={user_id_str})")
            else:
                message = f"**📊 إحصائيات المستخدم:** [{user_info['first_name']}](tg://user?id={user_id_str})\n\n"
                # a map for nicer names
                stat_names = {
                    'file_uploads': 'الملفات المرفوعة',
                    'file_deletes': 'الملفات المحذوفة',
                    'bots_started': 'البوتات التي تم تشغيلها',
                    'bots_stopped': 'البوتات التي تم إيقافها',
                    'folders_created': 'المجلدات المنشأة',
                    'folders_deleted': 'المجلدات المحذوفة',
                    'user_join': 'انضمام'
                }

                for key in sorted(stat_keys):
                    total = await get_total_stat(user_id, key)
                    # counts from events
                    today_count = await count_events(stat_name=key, user_id=user_id, start_ts=day_start, end_ts=now)
                    week_count  = await count_events(stat_name=key, user_id=user_id, start_ts=week_start, end_ts=now)
                    month_count = await count_events(stat_name=key, user_id=user_id, start_ts=month_start, end_ts=now)
                    year_count  = await count_events(stat_name=key, user_id=user_id, start_ts=year_start, end_ts=now)
                    display_name = stat_names.get(key, key)
                    message += f"- **{display_name}:** إجمالي `{fmt(total)}` — (اليوم `{fmt(today_count)}` / الأسبوع `{fmt(week_count)}` / الشهر `{fmt(month_count)}` / السنة `{fmt(year_count)}`)\n"

                await event.reply(message, parse_mode='md')

        conversation_manager.delete_state(sender_id)
        await restore_panel(send_stats_menu)


def setup(client_instance: "TelegramClient"):
    """Registers all admin stats handlers with the TelegramClient."""
    # Callbacks for menu navigation
    client_instance.on(events.CallbackQuery(pattern=b'admin:stats_menu'))(stats_menu_callback)

    # Callbacks for actions
    client_instance.on(events.CallbackQuery(pattern=b'admin:global_stats'))(global_stats_callback)
    client_instance.on(events.CallbackQuery(pattern=b'admin:generate_stats_image'))(generate_stats_image_callback)
    client_instance.on(events.CallbackQuery(pattern=b'admin:stats_download'))(stats_download_callback)
    client_instance.on(events.CallbackQuery(pattern=b'admin:user_stats'))(user_stats_prompt)

    # NewMessage handler for conversations
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.has_state(e.sender_id) and conversation_manager.get_status(e.sender_id) == "awaiting_user_for_stats"))(admin_stats_conversation_handler)
    print("✅ Admin Statistics handlers registered.")
