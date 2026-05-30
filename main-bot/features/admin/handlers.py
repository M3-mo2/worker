import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_IDS
from core.db import (
    add_worker, get_all_workers, get_active_workers, get_worker_by_id,
    get_worker_by_url, update_worker_status, delete_worker,
    count_workers, get_bots_by_worker
)
from core.worker import worker as worker_service
from core.keyboards import main_reply_keyboard
from .messages import (
    NO_WORKERS, WORKERS_LIST, WORKER_DETAILS,
    ADD_WORKER_ASK_URL, ADD_WORKER_ASK_SECRET, ADD_WORKER_SUCCESS,
    ADD_WORKER_EXISTS, DELETE_WORKER_CONFIRM, DELETE_WORKER_DONE,
    DELETE_WORKER_HAS_BOTS, MAINTENANCE_ON, MAINTENANCE_OFF,
    STATUS_ACTIVE, STATUS_MAINTENANCE, STATUS_DEAD,
    HEALTH_CHECK_RUNNING, HEALTH_CHECK_DONE
)

router = Router()


class AddWorkerStates(StatesGroup):
    waiting_url = State()
    waiting_secret = State()


def is_admin(user_id: int) -> bool:
    if not ADMIN_IDS:
        return True
    return user_id in ADMIN_IDS


def format_status(status: str) -> str:
    if status == "active":
        return STATUS_ACTIVE
    elif status == "maintenance":
        return STATUS_MAINTENANCE
    else:
        return STATUS_DEAD


def format_date(dt) -> str:
    if dt is None:
        return "لم يُفحص"
    if isinstance(dt, str):
        return dt[:16]
    return dt.strftime("%Y-%m-%d %H:%M")


# === قائمة الـ Workers ===

@router.message(Command("workers"))
async def cmd_workers(message: Message, user_id: int):
    if not is_admin(user_id):
        return await message.answer("❌ مش عندك صلاحية")

    workers = await get_all_workers()
    if not workers:
        return await message.answer(NO_WORKERS, reply_markup=main_reply_keyboard())

    lines = [WORKERS_LIST.format(count=len(workers))]
    for w in workers:
        status = format_status(w["status"])
        lines.append(f"• #{w['id']} — {status} — {w['bots_count']} بوت — {w['url']}")

    await message.answer("\n".join(lines), reply_markup=main_reply_keyboard())


# === إضافة Worker ===

async def start_add_worker(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ مش عندك صلاحية")

    await message.answer(ADD_WORKER_ASK_URL)
    await state.set_state(AddWorkerStates.waiting_url)


@router.message(Command("add_worker"))
async def cmd_add_worker(message: Message, state: FSMContext):
    await start_add_worker(message, state)


@router.message(AddWorkerStates.waiting_url, F.text)
async def handle_worker_url(message: Message, state: FSMContext):
    url = message.text.strip().rstrip("/")

    if not url.startswith("http"):
        return await message.answer("❌ الرابط لازم يبدأ بـ http:// أو https://")

    existing = await get_worker_by_url(url)
    if existing:
        await state.clear()
        return await message.answer(
            ADD_WORKER_EXISTS.format(url=url),
            reply_markup=main_reply_keyboard()
        )

    await state.update_data(worker_url=url)
    await message.answer(ADD_WORKER_ASK_SECRET.format(url=url))
    await state.set_state(AddWorkerStates.waiting_secret)


@router.message(AddWorkerStates.waiting_secret, F.text)
async def handle_worker_secret(message: Message, state: FSMContext):
    data = await state.get_data()
    url = data.get("worker_url")
    secret = message.text.strip()

    if ":" in secret:
        return await message.answer(
            "❌ ده توكن بوت مش الـ INTERNAL_SECRET\n\n"
            "الـ INTERNAL_SECRET هو string طويل زي:\n"
            "`26c29f5306ee74dd9517bafee1d1a9560081145df7551af5fa9d2eec9fba0e42`\n\n"
            "ابعت الـ INTERNAL_SECRET الصح:"
        )

    worker_id = await add_worker(url, secret)
    await state.clear()

    await message.answer(
        ADD_WORKER_SUCCESS.format(url=url),
        reply_markup=main_reply_keyboard()
    )


# === حذف Worker ===

@router.message(Command("del_worker"))
async def cmd_del_worker(message: Message, user_id: int):
    if not is_admin(user_id):
        return await message.answer("❌ مش عندك صلاحية")

    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("❌ الاستخدام: /del_worker <worker_id>")

    try:
        worker_id = int(parts[1])
    except ValueError:
        return await message.answer("❌ الـ ID لازم يكون رقم")

    w = await get_worker_by_id(worker_id)
    if not w:
        return await message.answer("❌ الـ Worker ده مش موجود")

    bots = await get_bots_by_worker(worker_id)
    if bots:
        return await message.answer(
            DELETE_WORKER_HAS_BOTS.format(count=len(bots))
        )

    await delete_worker(worker_id)
    await message.answer(DELETE_WORKER_DONE.format(id=worker_id))


# === تبديل حالة Worker (صيانة) ===

@router.message(Command("worker_maintenance"))
async def cmd_maintenance(message: Message, user_id: int):
    if not is_admin(user_id):
        return await message.answer("❌ مش عندك صلاحية")

    parts = message.text.split()
    if len(parts) < 2:
        return await message.answer("❌ الاستخدام: /worker_maintenance <worker_id>")

    try:
        worker_id = int(parts[1])
    except ValueError:
        return await message.answer("❌ الـ ID لازم يكون رقم")

    w = await get_worker_by_id(worker_id)
    if not w:
        return await message.answer("❌ الـ Worker ده مش موجود")

    if w["status"] == "active":
        await update_worker_status(worker_id, "maintenance")
        await message.answer(MAINTENANCE_ON.format(id=worker_id))
    else:
        await update_worker_status(worker_id, "active")
        await message.answer(MAINTENANCE_OFF.format(id=worker_id))


# === فحص الـ Workers ===

@router.message(Command("health_check"))
async def cmd_health_check(message: Message, user_id: int):
    if not is_admin(user_id):
        return await message.answer("❌ مش عندك صلاحية")

    workers = await get_all_workers()
    if not workers:
        return await message.answer("مفيش Workers مسجلين")

    msg = await message.answer(HEALTH_CHECK_RUNNING)

    results = []
    for w in workers:
        from core.worker import WorkerService
        ws = WorkerService(w["url"], w["secret"])
        result = await ws.health()

        if result.get("status") == "ok":
            await update_worker_status(w["id"], "active")
            results.append(f"🟢 #{w['id']} — {w['url']}")
        else:
            await update_worker_status(w["id"], "dead")
            results.append(f"🔴 #{w['id']} — {w['url']}")

    await msg.edit_text(
        HEALTH_CHECK_DONE.format(results="\n".join(results))
    )
