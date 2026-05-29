# bot_v2/bot/tasks/__init__.py
# This __init__.py file is responsible for aggregating and starting
# all background tasks within the 'tasks' sub-package.

import asyncio
from typing import TYPE_CHECKING

from . import expiry_checker
from . import failure_reporter
from . import ai_queue
from . import backup_task
from . import top_developers_checker

if TYPE_CHECKING:
    from telethon import TelegramClient

async def start_all_tasks(client: "TelegramClient"):
    """
    Starts all background tasks for the bot.
    """
    # Initialize the database for tasks if it hasn't been already (e.g. from core.database)
    # This might be redundant if bot.core.database.init_db() is called elsewhere during startup
    # For now, it's safer to ensure DB is ready if a task directly interacts with it.
    from bot.core.database import init_db as init_core_db
    await init_core_db() 
    
    # Start the individual task functions as asyncio tasks
    asyncio.create_task(expiry_checker.periodic_expiry_check())
    asyncio.create_task(failure_reporter.failure_reporter_task())
    asyncio.create_task(ai_queue.ai_queue_worker())
    asyncio.create_task(backup_task.daily_backup_task())
    asyncio.create_task(top_developers_checker.top_developers_checker_task())

    print("✅ All background tasks initiated.")

print("✅ Tasks package initialized.")
