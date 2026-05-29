# bot_v2/bot/handlers/profile.py
# Contains handlers for user's personal profile, stats, and notification preferences.

import time
from datetime import datetime, timedelta
from telethon import events
from telethon.tl.custom import Button
from typing import TYPE_CHECKING, Dict, Any, Optional

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.database import count_events, get_total_stat, get_user_stat_names

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status, get_user_data, save_user_data

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message
from bot.utils.time import _now_ts, _start_of_day, _start_of_week, _start_of_month, _start_of_year

# Local Imports from bot_v2 handlers (for now, will be refactored later)


# --- Handlers ---
async def my_stats_handler(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    now = _now_ts()
    day_start = _start_of_day()
    week_start = _start_of_week()
    month_start = _start_of_month()
    year_start = _start_of_year()

    stat_keys = await get_user_stat_names(sender_id)
    if not stat_keys:
        return await safe_edit_message(event, "**📊 إحصائياتك:**\n\nلا توجد إحصائيات مسجلة لك بعد.", buttons=[[Button.inline("↩️ القائمة الرئيسية", data="main_menu")]])

    message = "**📊 إحصائياتك الشخصية:**\n\n"
    stat_names = {
        'file_uploads': 'الملفات المرفوعة',
        'file_deletes': 'الملفات المحذوفة',
        'bots_started': 'البوتات التي تم تشغيلها',
        'bots_stopped': 'البوتات التي تم إيقافها',
        'folders_created': 'المجلدات المنشأة',
        'folders_deleted': 'المجلدات المحذوفة',
        'user_join': 'انضمام'
    }

    def fmt(n):
        try:
            return f"{int(n):,}"
        except:
            return str(n)

    for key in sorted(stat_keys):
        total = await get_total_stat(sender_id, key)
        today_count = await count_events(stat_name=key, user_id=sender_id, start_ts=day_start, end_ts=now)
        week_count  = await count_events(stat_name=key, user_id=sender_id, start_ts=week_start, end_ts=now)
        month_count = await count_events(stat_name=key, user_id=sender_id, start_ts=month_start, end_ts=now)
        year_count  = await count_events(stat_name=key, user_id=sender_id, start_ts=year_start, end_ts=now)
        display_name = stat_names.get(key, key)
        message += f"- **{display_name}:** إجمالي `{fmt(total)}` — (اليوم `{fmt(today_count)}` / الأسبوع `{fmt(week_count)}` / الشهر `{fmt(month_count)}` / السنة `{fmt(year_count)}`)\n"

    buttons = [[Button.inline("↩️ القائمة الرئيسية", data="main_menu")]]
    await safe_edit_message(event, message, buttons=buttons)


async def toggle_failure_notify_handler(event: events.CallbackQuery.Event):
    sender_id = str(event.sender_id)
    user_status = check_user_status(sender_id)
    if user_status == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)

    user_data = get_user_data(int(sender_id))
    if not user_data:
        user_data = {} # Handle case where user isn't registered yet
    
    current_status = user_data.get('notify_failures', True)
    new_status = not current_status
    user_data['notify_failures'] = new_status
    save_user_data(int(sender_id), user_data)
    status_text = "مفعلة ✅" if new_status else "معطلة ❌"
    await event.answer(f"تم تغيير حالة تنبيهات الأعطال إلى: {status_text}", alert=True)
    
    # Reload main menu to reflect change in button text
    from bot.handlers.main_menu import main_menu_callback_handler
    from bot.handlers.main_menu import main_menu_callback_handler # Forward reference
    await main_menu_callback_handler(event)


def setup(client_instance: "TelegramClient"):
    """Registers all profile handlers with the TelegramClient."""
    client_instance.on(events.CallbackQuery(pattern=b"my_stats"))(my_stats_handler)
    client_instance.on(events.CallbackQuery(pattern=b"toggle_failure_notify"))(toggle_failure_notify_handler)
    print("✅ Profile handlers registered.")
