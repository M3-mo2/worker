# bot_v2/bot/tasks/failure_reporter.py
# Contains the background task for periodically checking and reporting bot failures.

import asyncio
import time
import traceback
from collections import defaultdict
from typing import Dict, Any, Optional

import aiosqlite # For interacting with queue.db

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_all_users
from bot.utils.time import _start_of_day # For AI usage logs
# Placeholder for _now_ts

# --- Temporary Placeholders for now. These will be properly imported from other modules later ---

# Placeholder for _now_ts (from bot.utils.time)
def _now_ts():
    from datetime import datetime
    return int(datetime.now().timestamp()) # Simplified for now

# DB_NAME will come from bot.core.database
from bot.core.database import DB_NAME


# --- Functions ---

def extract_sender_id(update_data: Dict[str, Any]) -> Optional[int]:
    """Extracts sender ID from a Telegram update dictionary."""
    try:
        if 'message' in update_data:
            return update_data['message']['from']['id']
        if 'callback_query' in update_data:
            return update_data['callback_query']['from']['id']
        if 'inline_query' in update_data:
            return update_data['inline_query']['from']['id']
        if 'my_chat_member' in update_data:
            return update_data['my_chat_member']['from']['id']

    except (KeyError, TypeError):
        pass
    return None


async def failure_reporter_task(interval: int = 600): # Every 10 minutes
    """
    Background task to monitor webhook failures and notify users.
    """
    print("🕵️‍♂️ بدء مهمة مراقب الأعطال (Failure Reporter)...")
    while True:
        await asyncio.sleep(interval)
        try:
            # 1. Get all unreported failed updates
            async with aiosqlite.connect(DB_NAME, timeout=30) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT id, owner_id, token FROM queue WHERE reported = 0 ORDER BY id ASC"
                ) as cursor:
                    failed_updates = await cursor.fetchall()
            
            if not failed_updates:
                continue

            # 2. Group by bot token
            updates_by_token = defaultdict(list)
            for update_row in failed_updates:
                updates_by_token[update_row['token']].append(update_row)

            updates_to_mark_reported = []
            
            # 3. Check counts for each token
            for token, updates in updates_by_token.items():
                if len(updates) >= 5: # Threshold for reporting
                    owner_id = updates[0]['owner_id']
                    
                    all_users = load_all_users()
                    # Check user preference for failure notifications
                    if not all_users.get(str(owner_id), {}).get('notify_failures', True):
                        continue
                    
                    for update in updates:
                        updates_to_mark_reported.append(update['id'])

                    try:
                        # Use client to get bot entity, or placeholder if client not available
                        bot_info = await client.get_entity(int(token.split(':')[0]))
                        bot_name = f"@{bot_info.username}"
                    except:
                        bot_name = f"`{token[:8]}...`" # Mask token if name can't be fetched

                    report_msg = (
                        f"🚨 **تنبيه عطل متكرر في بوتك!**\n"
                        f"🤖 البوت: {bot_name}\n\n"
                        f"لقد فشل آخر **{len(updates)}** تحديثات متتالية في الوصول للبوت الخاص بك لأنه لا يستجيب (ربما متوقف أو به خطأ Fatal Error).\n\n"
                        "⚠️ يرجى فحص البوت وتشغيله يدوياً أو مراجعة سجل الأخطاء."
                    )
                    try:
                        await client.send_message(owner_id, report_msg)
                        print(f"[Reporter] Sent failure notification to {owner_id} for bot {token[:8]}")
                    except Exception as e:
                        print(f"[Reporter] Failed to send to {owner_id}: {e}")

            # 4. Update the database
            if updates_to_mark_reported:
                async with aiosqlite.connect(DB_NAME, timeout=30) as db:
                    await db.execute(
                        f"UPDATE queue SET reported = 1 WHERE id IN ({','.join('?' for _ in updates_to_mark_reported)})",
                        updates_to_mark_reported
                    )
                    await db.commit()
                    print(f"[Reporter] Marked {len(updates_to_mark_reported)} updates as reported.")

        except Exception as e:
            print(f"🔥 خطأ في مراقب الأعطال: {e}\n{traceback.format_exc()}")

print("✅ Failure Reporter task module initialized.")
