import asyncio
import logging
from config import WORKER_URL, INTERNAL_SECRET
from core.bot import create_bot
from core.db import init as init_db, close as close_db, get_worker_by_url, add_worker
from core.worker import health_check_loop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


async def register_default_worker():
    if not WORKER_URL or not INTERNAL_SECRET:
        return
    existing = await get_worker_by_url(WORKER_URL)
    if not existing:
        await add_worker(WORKER_URL, INTERNAL_SECRET)
        logging.info(f"Default worker registered: {WORKER_URL}")


async def main():
    await init_db()
    await register_default_worker()
    bot, dp = create_bot()

    health_task = asyncio.create_task(health_check_loop(60))

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Webhook deleted, starting polling...")
        await dp.start_polling(bot)
    finally:
        health_task.cancel()
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())
