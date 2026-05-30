import asyncio
import logging
from core.bot import create_bot
from core.db import init as init_db, close as close_db
from core.worker import health_check_loop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


async def main():
    await init_db()
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
