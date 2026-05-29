# bot_v2/bot/services/user_service.py
# Centralized service for managing user-related logic such as status, roles, and data.

import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from bot.core.config import settings
from bot.core.data_manager import load_admin_list, load_banned_list, load_all_users, save_all_users, load_stats, save_stats, stats_lock
from bot.utils.time import _now_ts, _start_of_day, _start_of_week, _start_of_month, _start_of_year, _TZ

def check_user_status(user_id: int) -> str:
    """
    Checks user status with admin priority.
    Returns: 'sudo', 'admin', 'banned', or 'user'.
    """
    # SUDO users are highest priority
    if user_id in settings.telegram.SUDO_USERS:
        return 'sudo'
    
    admins = load_admin_list()
    if str(user_id) in admins:
        return 'admin'
    
    banned = load_banned_list()
    if str(user_id) in banned:
        return 'banned'
        
    return 'user' # default to normal user

def get_user_data(user_id: int) -> Dict[str, Any]:
    """Retrieves a user's data from all_users.json."""
    all_users = load_all_users()
    return all_users.get(str(user_id), {})

def save_user_data(user_id: int, user_data: Dict[str, Any]):
    """Saves a user's data to all_users.json."""
    all_users = load_all_users()
    all_users[str(user_id)] = user_data
    save_all_users(all_users)

def increment_stat(user_id: int, stat_name: str, count: int = 1):
    """
    Thread-safe increment of a statistic for both global and per-user counters,
    and append a timestamped event to stats['events'] for period queries.
    """
    user_id_str = str(user_id)
    with stats_lock:
        stats = load_stats()

        # Ensure keys exist
        if "global" not in stats or not isinstance(stats["global"], dict):
            stats["global"] = {}
        if "users" not in stats or not isinstance(stats["users"], dict):
            stats["users"] = {}

        # Increment global counters
        stats["global"][stat_name] = stats["global"].get(stat_name, 0) + int(count)

        # Increment user-specific
        if user_id_str not in stats["users"]:
            stats["users"][user_id_str] = {}
        stats["users"][user_id_str][stat_name] = stats["users"][user_id_str].get(stat_name, 0) + int(count)

        # Append event (timestamped) for time-based queries
        events = stats.get("events", [])
        events.append({
            "ts": _now_ts(),
            "user": user_id_str,
            "stat": stat_name,
            "count": int(count)
        })
        stats["events"] = events

        save_stats(stats)


def count_events(stat_name: Optional[str] = None, user_id: Optional[int] = None, start_ts: int = 0, end_ts: Optional[int] = None) -> int:
    """
    Count events stored in stats.json between start_ts and end_ts.
    - stat_name: if provided, filter by that stat
    - user_id: if provided (int or str), filter by that user
    Returns integer sum.
    """
    end_ts = end_ts or _now_ts()
    s = 0
    stats = load_stats()
    events = stats.get("events", [])
    user_str = str(user_id) if user_id is not None else None
    for ev in events:
        try:
            ts = int(ev.get("ts", 0))
        except:
            continue
        if ts < start_ts or ts > end_ts:
            continue
        if stat_name and ev.get("stat") != stat_name:
            continue
        if user_str and ev.get("user") != user_str:
            continue
        s += int(ev.get("count", 1))
    return s


print("✅ User Service initialized.")
