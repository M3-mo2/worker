# bot_v2/bot/tasks/ai_queue.py
# Contains the asyncio Queue and worker for processing AI tasks serially.

import asyncio
import time
import traceback
import logging
import os

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message

# Setup logging for the AI queue worker
ai_queue_logger = logging.getLogger('AI_Queue_Worker')
ai_queue_logger.setLevel(logging.INFO)
# Ensure logs directory exists - should be handled by root logging setup or individual module
os.makedirs('logs', exist_ok=True)
ai_queue_log_handler = logging.FileHandler('logs/ai_queue_worker.log', encoding='utf-8')
ai_queue_log_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
if not ai_queue_logger.hasHandlers():
    ai_queue_logger.addHandler(ai_queue_log_handler)


# --- AI Task Queue System ---
AI_QUEUE = asyncio.Queue()

async def ai_queue_worker():
    """
    Background worker: processes AI tasks one by one with a delay to avoid API rate limits.
    """
    ai_queue_logger.info("👷‍♂️ عامل طابور الـ AI جاهز للعمل...")
    while True:
        # 1. Wait for a new task
        task_func, user_id, status_msg = await AI_QUEUE.get()
        
        try:
            # Update user message to indicate task is being processed
            try:
                await safe_edit_message(status_msg, "⚡️ **جاري التنفيذ الآن...**\n(شكراً لانتظارك)")
            except Exception as e:
                ai_queue_logger.warning(f"Failed to update status message for AI task for user {user_id}: {e}")

            # 2. Execute the task function
            await task_func()
            
        except Exception as e:
            ai_queue_logger.error(f"🔥 خطأ في عامل طابور الـ AI للمستخدم {user_id}: {e}\n{traceback.format_exc()}")
            try:
                await safe_edit_message(status_msg, f"❌ حدث خطأ أثناء معالجة طلبك:\n`{e}`")
            except Exception as e_msg:
                ai_queue_logger.warning(f"Failed to send error message to user {user_id} after AI task failure: {e_msg}")
        finally:
            # 3. Mark task as done and enforce a cooldown
            AI_QUEUE.task_done()
            await asyncio.sleep(3) # ⏳ Cooldown period to respect API limits

print("✅ AI Queue task module initialized.")
