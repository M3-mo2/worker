import os
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from core.worker import WorkerService, select_best_worker
from core.db import add_bot, get_user_bots, get_bot_by_id, update_status, update_bot_username, increment_worker_bots
from core.validators import validate_php_file, validate_bot_token
from core.keyboards import (
    main_reply_keyboard, deploy_keyboard, deploy_success_keyboard,
    cancel_keyboard, error_retry_keyboard
)
from .messages import (
    ASK_FILE, ASK_TOKEN, DEPLOYING, UPLOADING, REGISTERING,
    SUCCESS, TOKEN_USED, WORKER_DOWN, DEPLOY_ERROR, CANCELLED,
    ALREADY_DEPLOYING, QUICK_TOKEN, FILE_OUTSIDE_DEPLOY, TOKEN_OUTSIDE_DEPLOY
)

router = Router()


class DeployStates(StatesGroup):
    waiting_file = State()
    waiting_token = State()


async def get_bot_username(token: str) -> str | None:
    try:
        import httpx
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"https://api.telegram.org/bot{token}/getMe")
            data = r.json()
            if data.get("ok"):
                return f"@{data['result']['username']}"
    except Exception:
        pass
    return None


# === بدء عملية النشر ===

async def start_deploy(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state in (DeployStates.waiting_file, DeployStates.waiting_token):
        await message.answer(ALREADY_DEPLOYING)
        return

    await state.clear()
    await message.answer(ASK_FILE, reply_markup=cancel_keyboard())
    await state.set_state(DeployStates.waiting_file)


@router.message(Command("deploy"))
async def cmd_deploy(message: Message, state: FSMContext):
    await start_deploy(message, state)


@router.message(lambda m: m.text == "🚀 نشر بوت")
async def btn_deploy(message: Message, state: FSMContext):
    await start_deploy(message, state)


@router.callback_query(F.data == "deploy:new")
async def cb_deploy_new(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await start_deploy(callback.message, state)


# === استقبال الملف ===

@router.message(DeployStates.waiting_file, F.document)
async def handle_file(message: Message, state: FSMContext):
    error = validate_php_file(message.document)
    if error:
        await message.answer(error, reply_markup=cancel_keyboard())
        return

    await message.answer("⏳ جاري تحميل الملف...")

    file_info = await message.bot.get_file(message.document.file_id)
    os.makedirs("data/bots", exist_ok=True)
    path = f"data/bots/{message.from_user.id}_bot.php"
    await message.bot.download_file(file_info.file_path, path)

    await state.update_data(file_path=path)
    await message.answer(ASK_TOKEN, reply_markup=cancel_keyboard())
    await state.set_state(DeployStates.waiting_token)


@router.message(DeployStates.waiting_file)
async def handle_file_wrong(message: Message):
    await message.answer(
        "📎 ارفع ملف PHP مش نص.\n\nابعتلي ملف بامتداد `.php`",
        reply_markup=cancel_keyboard()
    )


# === استقبال التوكن ===

@router.message(DeployStates.waiting_token, F.text)
async def handle_token(message: Message, state: FSMContext):
    error = validate_bot_token(message.text)
    if error:
        await message.answer(error, reply_markup=cancel_keyboard())
        return

    data = await state.get_data()
    file_path = data.get("file_path")

    if not file_path or not os.path.exists(file_path):
        await message.answer("❌ الملف ات_حذف. ابدأ النشر من الأول.", reply_markup=main_reply_keyboard())
        await state.clear()
        return

    token = message.text.strip()

    # جلب username البوت
    bot_username = await get_bot_username(token)

    # رسالة loading
    loading_msg = await message.answer(DEPLOYING)

    # اختيار أفضل Worker
    await loading_msg.edit_text("🔍 جاري اختيار أفضل سيرفر...")
    best_worker = await select_best_worker()
    if not best_worker:
        await loading_msg.edit_text(WORKER_DOWN, reply_markup=error_retry_keyboard())
        await state.clear()
        return

    ws = WorkerService(best_worker["url"], best_worker["secret"])

    # رفع الملف للـ Worker
    await loading_msg.edit_text(UPLOADING)
    result = await ws.deploy(
        user_id=message.from_user.id,
        bot_token=token,
        file_path=file_path
    )

    if result.get("status") == "ok":
        # تسجيل webhook
        await loading_msg.edit_text(REGISTERING)

        # استخراج webhook_secret من الـ Worker
        webhook_secret = result.get("webhook_secret")

        # تسجيل الـ routing في Cloudflare KV
        await ws.register_routing(str(message.from_user.id))

        # تعيين webhook بـ Cloudflare URL + secret_token
        await ws.set_webhook(message.from_user.id, token, webhook_secret)

        # حفظ في الداتابيز
        bot_id = await add_bot(message.from_user.id, token, bot_username, best_worker["id"])
        await increment_worker_bots(best_worker["id"])

        # تحديث الـ username لو اتجاب
        if bot_username:
            await update_bot_username(bot_id, bot_username)

        # رابط البوت
        bot_link = f"https://t.me/{bot_username.replace('@', '')}" if bot_username else ""

        await loading_msg.edit_text(
            SUCCESS.format(bot_username=bot_username or "البوت"),
            reply_markup=deploy_success_keyboard(bot_link)
        )
    else:
        detail = result.get("detail", "خطأ غير معروف")

        if "already" in str(detail).lower() or "conflict" in str(detail).lower():
            # التوكن مستخدم
            existing_bots = await get_user_bots(message.from_user.id)
            existing = next((b for b in existing_bots if b["bot_token"] == token), None)
            if existing:
                await loading_msg.edit_text(
                    TOKEN_USED.format(bot_username=existing.get("bot_username", f"Bot #{existing['id']}")),
                    reply_markup=error_retry_keyboard()
                )
            else:
                await loading_msg.edit_text(
                    TOKEN_USED.format(bot_username="بوت تاني"),
                    reply_markup=error_retry_keyboard()
                )
        else:
            await loading_msg.edit_text(
                DEPLOY_ERROR.format(error_message=detail),
                reply_markup=error_retry_keyboard()
            )

    await state.clear()


@router.message(DeployStates.waiting_token)
async def handle_token_wrong(message: Message):
    await message.answer(
        "🔑 ابعتلي التوكن كنص مش كملف.\n\nالشكل: `123456789:ABCdefGHI...`",
        reply_markup=cancel_keyboard()
    )


# === إلغاء ===

@router.callback_query(F.data == "deploy:cancel")
async def cb_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(CANCELLED)
    await callback.message.answer("اختر من القائمة:", reply_markup=main_reply_keyboard())


# === Quick Action — يبعت توكن مباشرة ===

@router.message(F.text.regexp(r"^\d{8,12}:[A-Za-z0-9_-]{35}$"))
async def handle_quick_token(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        return

    error = validate_bot_token(message.text)
    if error:
        return

    await state.update_data(pending_token=message.text.strip())
    await message.answer(QUICK_TOKEN, reply_markup=cancel_keyboard())
    await state.set_state(DeployStates.waiting_file)


# === يبعت ملف وهو مش في deploy ===

@router.message(F.document)
async def handle_file_outside_deploy(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == DeployStates.waiting_file.state:
        return
    await message.answer(FILE_OUTSIDE_DEPLOY, reply_markup=main_reply_keyboard())
