from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from core.db import count_user_bots
from core.keyboards import main_reply_keyboard
from .messages import WELCOME_NEW, WELCOME_BACK, HELP

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, user_id: int):
    count = await count_user_bots(user_id)
    if count > 0:
        await message.answer(
            WELCOME_BACK.format(count=count),
            reply_markup=main_reply_keyboard()
        )
    else:
        await message.answer(
            WELCOME_NEW,
            reply_markup=main_reply_keyboard()
        )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP, reply_markup=main_reply_keyboard())


@router.message(lambda m: m.text == "❓ مساعدة")
async def btn_help(message: Message):
    await message.answer(HELP, reply_markup=main_reply_keyboard())
