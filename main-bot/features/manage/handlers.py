import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from core.db import (
    get_user_bots, get_bot_by_id, get_active_bot, get_worker_by_id,
    update_status, delete_bot, count_user_bots, decrement_worker_bots
)
from core.worker import WorkerService, select_best_worker
from core.keyboards import (
    main_reply_keyboard, bots_list_keyboard, bot_actions_keyboard,
    confirm_keyboard, stop_done_keyboard, delete_done_keyboard,
    restart_done_keyboard, back_keyboard
)
from .messages import (
    NO_BOTS, YOUR_BOTS, BOT_DETAILS_RUNNING, BOT_DETAILS_STOPPED,
    STOP_CONFIRM, STOP_DONE, DELETE_CONFIRM, DELETE_DONE,
    RESTARTING, RESTART_DONE, STATUS_HEADER, STATUS_RUNNING,
    STATUS_STOPPED, STATUS_TOTAL, NOT_YOUR_BOT, BOT_DELETED,
    NO_ACTIVE_BOT
)

router = Router()


def format_date(dt) -> str:
    if dt is None:
        return "غير معروف"
    if isinstance(dt, str):
        return dt[:16]
    return dt.strftime("%Y-%m-%d %H:%M")


def get_bot_link(bot_username: str | None) -> str:
    if bot_username and bot_username.startswith("@"):
        return f"https://t.me/{bot_username[1:]}"
    return ""


async def verify_bot_ownership(callback: CallbackQuery, bot_id: int) -> dict | None:
    bot = await get_bot_by_id(bot_id)
    if not bot:
        await callback.answer(BOT_DELETED, show_alert=True)
        return None
    if bot["user_id"] != callback.from_user.id:
        await callback.answer(NOT_YOUR_BOT, show_alert=True)
        return None
    return bot


async def get_ws_for_bot(bot: dict) -> WorkerService:
    if bot.get("worker_id"):
        w = await get_worker_by_id(bot["worker_id"])
        if w and w["status"] == "active":
            return WorkerService(w["url"], w["secret"])
    best = await select_best_worker()
    if best:
        return WorkerService(best["url"], best["secret"])
    return WorkerService()


# === قائمة البوتات ===

async def show_bots_list(message: Message, user_id: int):
    bots = await get_user_bots(user_id)
    if not bots:
        await message.answer(NO_BOTS, reply_markup=main_reply_keyboard())
        return
    await message.answer(
        YOUR_BOTS.format(count=len(bots)),
        reply_markup=bots_list_keyboard(bots)
    )


@router.message(Command("bots"))
async def cmd_bots(message: Message, user_id: int):
    await show_bots_list(message, user_id)


@router.message(lambda m: m.text == "📋 بوتاتي")
async def btn_bots(message: Message, user_id: int):
    await show_bots_list(message, user_id)


@router.callback_query(F.data == "manage:list")
async def cb_list(callback: CallbackQuery, user_id: int):
    await callback.answer()
    bots = await get_user_bots(user_id)
    if not bots:
        await callback.message.edit_text(NO_BOTS)
        await callback.message.answer("اختر من القائمة:", reply_markup=main_reply_keyboard())
        return
    await callback.message.edit_text(
        YOUR_BOTS.format(count=len(bots)),
        reply_markup=bots_list_keyboard(bots)
    )


# === عرض تفاصيل بوت ===

@router.callback_query(F.data.startswith("manage:view:"))
async def cb_view(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[2])
    bot = await verify_bot_ownership(callback, bot_id)
    if not bot:
        return

    bot_link = get_bot_link(bot.get("bot_username"))
    created = format_date(bot.get("created_at"))

    if bot["status"] == "running":
        text = BOT_DETAILS_RUNNING.format(
            bot_username=bot.get("bot_username") or f"Bot #{bot['id']}",
            created=created,
            bot_link=bot_link
        )
    else:
        text = BOT_DETAILS_STOPPED.format(
            bot_username=bot.get("bot_username") or f"Bot #{bot['id']}",
            created=created
        )

    await callback.message.edit_text(
        text,
        reply_markup=bot_actions_keyboard(bot["id"], bot["status"])
    )


# === إيقاف بوت ===

@router.callback_query(F.data.startswith("manage:stop:"))
async def cb_stop(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[2])
    bot = await verify_bot_ownership(callback, bot_id)
    if not bot:
        return

    bot_name = bot.get("bot_username") or f"Bot #{bot['id']}"
    await callback.message.edit_text(
        STOP_CONFIRM.format(bot_username=bot_name),
        reply_markup=confirm_keyboard("stop", bot_id)
    )


@router.callback_query(F.data.startswith("manage:confirm:stop:"))
async def cb_confirm_stop(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[3])
    bot = await verify_bot_ownership(callback, bot_id)
    if not bot:
        return

    ws = await get_ws_for_bot(bot)
    await ws.stop(callback.from_user.id)
    await update_status(bot_id, "stopped")

    bot_name = bot.get("bot_username") or f"Bot #{bot['id']}"
    await callback.message.edit_text(
        STOP_DONE.format(bot_username=bot_name),
        reply_markup=stop_done_keyboard(bot_id)
    )


# === تشغيل بوت ===

@router.callback_query(F.data.startswith("manage:start:"))
async def cb_start(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[2])
    bot = await verify_bot_ownership(callback, bot_id)
    if not bot:
        return

    file_path = f"data/bots/{callback.from_user.id}_bot.php"
    ws = await get_ws_for_bot(bot)
    result = await ws.deploy(
        user_id=callback.from_user.id,
        bot_token=bot["bot_token"],
        file_path=file_path
    )

    if result.get("status") == "ok":
        webhook_secret = result.get("webhook_secret")
        await ws.register_routing(str(callback.from_user.id))
        await ws.set_webhook(callback.from_user.id, bot["bot_token"], webhook_secret)
        await update_status(bot_id, "running")
        await callback.answer("✅ تم التشغيل")
        bot = await get_bot_by_id(bot_id)
        bot_link = get_bot_link(bot.get("bot_username"))
        created = format_date(bot.get("created_at"))
        text = BOT_DETAILS_RUNNING.format(
            bot_username=bot.get("bot_username") or f"Bot #{bot['id']}",
            created=created,
            bot_link=bot_link
        )
        await callback.message.edit_text(
            text,
            reply_markup=bot_actions_keyboard(bot_id, "running")
        )
    else:
        await callback.answer("❌ فشل التشغيل", show_alert=True)


# === إعادة تشغيل ===

@router.callback_query(F.data.startswith("manage:restart:"))
async def cb_restart(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[2])
    bot = await verify_bot_ownership(callback, bot_id)
    if not bot:
        return

    bot_name = bot.get("bot_username") or f"Bot #{bot['id']}"
    await callback.message.edit_text(RESTARTING.format(bot_username=bot_name))

    ws = await get_ws_for_bot(bot)
    await ws.stop(callback.from_user.id)

    file_path = f"data/bots/{callback.from_user.id}_bot.php"
    result = await ws.deploy(
        user_id=callback.from_user.id,
        bot_token=bot["bot_token"],
        file_path=file_path
    )

    if result.get("status") == "ok":
        webhook_secret = result.get("webhook_secret")
        await ws.register_routing(str(callback.from_user.id))
        await ws.set_webhook(callback.from_user.id, bot["bot_token"], webhook_secret)
        await update_status(bot_id, "running")
        bot_link = get_bot_link(bot.get("bot_username"))
        await callback.message.edit_text(
            RESTART_DONE.format(bot_username=bot_name),
            reply_markup=restart_done_keyboard(bot_link)
        )
    else:
        await callback.message.edit_text(
            f"❌ فشل إعادة تشغيل {bot_name}",
            reply_markup=back_keyboard()
        )


# === حذف بوت ===

@router.callback_query(F.data.startswith("manage:delete:"))
async def cb_delete(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[2])
    bot = await verify_bot_ownership(callback, bot_id)
    if not bot:
        return

    bot_name = bot.get("bot_username") or f"Bot #{bot['id']}"
    await callback.message.edit_text(
        DELETE_CONFIRM.format(bot_username=bot_name),
        reply_markup=confirm_keyboard("delete", bot_id)
    )


@router.callback_query(F.data.startswith("manage:confirm:delete:"))
async def cb_confirm_delete(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[3])
    bot = await verify_bot_ownership(callback, bot_id)
    if not bot:
        return

    ws = await get_ws_for_bot(bot)
    await ws.stop(callback.from_user.id)
    await delete_bot(bot_id)

    bot_name = bot.get("bot_username") or f"Bot #{bot['id']}"
    await callback.message.edit_text(
        DELETE_DONE.format(bot_username=bot_name),
        reply_markup=delete_done_keyboard()
    )


# === إلغاء ===

@router.callback_query(F.data.startswith("manage:cancel:"))
async def cb_cancel(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[2])
    bot = await get_bot_by_id(bot_id)
    if not bot:
        await callback.message.edit_text(BOT_DELETED)
        return

    bot_link = get_bot_link(bot.get("bot_username"))
    created = format_date(bot.get("created_at"))

    if bot["status"] == "running":
        text = BOT_DETAILS_RUNNING.format(
            bot_username=bot.get("bot_username") or f"Bot #{bot['id']}",
            created=created,
            bot_link=bot_link
        )
    else:
        text = BOT_DETAILS_STOPPED.format(
            bot_username=bot.get("bot_username") or f"Bot #{bot['id']}",
            created=created
        )

    await callback.message.edit_text(
        text,
        reply_markup=bot_actions_keyboard(bot["id"], bot["status"])
    )


# === رجوع ===

@router.callback_query(F.data == "manage:back")
async def cb_back(callback: CallbackQuery, user_id: int):
    await callback.answer()
    bots = await get_user_bots(user_id)
    if not bots:
        await callback.message.edit_text(NO_BOTS)
        await callback.message.answer("اختر من القائمة:", reply_markup=main_reply_keyboard())
        return
    await callback.message.edit_text(
        YOUR_BOTS.format(count=len(bots)),
        reply_markup=bots_list_keyboard(bots)
    )


# === حالة البوتات ===

@router.message(Command("status"))
async def cmd_status(message: Message, user_id: int):
    bots = await get_user_bots(user_id)
    if not bots:
        await message.answer(NO_BOTS, reply_markup=main_reply_keyboard())
        return

    lines = [STATUS_HEADER]
    running = 0
    stopped = 0

    for bot in bots:
        name = bot.get("bot_username") or f"Bot #{bot['id']}"
        if bot["status"] == "running":
            lines.append(STATUS_RUNNING.format(username=name))
            running += 1
        else:
            lines.append(STATUS_STOPPED.format(username=name))
            stopped += 1

    lines.append(STATUS_TOTAL.format(total=len(bots)))

    await message.answer("\n".join(lines), reply_markup=main_reply_keyboard())


# === إيقاف سريع ===

@router.message(Command("stop"))
async def cmd_stop(message: Message, user_id: int):
    bot = await get_active_bot(user_id)
    if not bot:
        await message.answer(NO_ACTIVE_BOT, reply_markup=main_reply_keyboard())
        return

    bot_name = bot.get("bot_username") or f"Bot #{bot['id']}"
    await message.answer(
        STOP_CONFIRM.format(bot_username=bot_name),
        reply_markup=confirm_keyboard("stop", bot["id"])
    )
