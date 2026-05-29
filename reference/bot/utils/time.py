# bot_v2/bot/utils/time.py
# Contains reusable time-related utility functions.

import time
from datetime import datetime, timedelta
from typing import Optional

# Placeholder for _TZ (from main.py and admin.py)
try:
    # Python 3.9+ preferred
    from zoneinfo import ZoneInfo
    _TZ = ZoneInfo("Africa/Cairo")
except ImportError:
    _TZ = None  # fallback to system time if zoneinfo not available


def _now_ts() -> int:
    """Returns the current Unix timestamp."""
    if _TZ:
        return int(datetime.now(_TZ).timestamp())
    return int(time.time())

def _start_of_day(ts: Optional[int] = None) -> int:
    """Returns the Unix timestamp for the start of the day (00:00:00)."""
    ts = ts or _now_ts()
    if _TZ:
        dt = datetime.fromtimestamp(ts, _TZ).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        dt = datetime.utcfromtimestamp(ts).replace(hour=0, minute=0, second=0, microsecond=0)
    return int(dt.timestamp())

def _start_of_week(ts: Optional[int] = None) -> int:
    """Returns the Unix timestamp for the start of the current week (Monday 00:00:00)."""
    ts = ts or _now_ts()
    if _TZ:
        dt = datetime.fromtimestamp(ts, _TZ)
    else:
        dt = datetime.utcfromtimestamp(ts)
    start = dt - timedelta(days=dt.weekday())
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(start.timestamp())

def _start_of_month(ts: Optional[int] = None) -> int:
    """Returns the Unix timestamp for the start of the current month (1st day, 00:00:00)."""
    ts = ts or _now_ts()
    if _TZ:
        dt = datetime.fromtimestamp(ts, _TZ)
    else:
        dt = datetime.utcfromtimestamp(ts)
    start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return int(start.timestamp())

def _start_of_year(ts: Optional[int] = None) -> int:
    """Returns the Unix timestamp for the start of the current year (Jan 1st, 00:00:00)."""
    ts = ts or _now_ts()
    if _TZ:
        dt = datetime.fromtimestamp(ts, _TZ)
    else:
        dt = datetime.utcfromtimestamp(ts)
    start = dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return int(start.timestamp())

print("✅ Time utilities module initialized.")
