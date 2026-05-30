from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from core.middleware import AuthMiddleware, LoggingMiddleware
from features.start import router as start_router
from features.deploy import router as deploy_router
from features.manage import router as manage_router
from features.admin import router as admin_router


def create_bot() -> tuple[Bot, Dispatcher]:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())

    dp.include_router(start_router)
    dp.include_router(deploy_router)
    dp.include_router(manage_router)
    dp.include_router(admin_router)

    return bot, dp
