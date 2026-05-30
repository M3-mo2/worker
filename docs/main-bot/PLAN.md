# Main Bot — خطة البناء الكاملة

## نظرة عامة

الـ Main Bot هو البوت الأساسي اللي المستخدمين بيتكلموا معاه على تيليجرام. بيستقبل ملفات PHP والتوكنات، وبعتهم للـ Worker عشان ينشرهم. كمان بيدير البوتات (إيقاف، تشغيل، حذف، حالة).

```
المستخدم (Telegram) ←→ Main Bot ←→ Worker API ←→ PHP-FPM
```

---

## التقنيات

| التقنية | الإصدار | ليها |
|---------|---------|------|
| Python | 3.11+ | لغة البناء |
| aiogram | 3.13+ | مكتبة تيليجرام async |
| httpx | 0.27+ | HTTP client async للـ Worker API |
| asyncpg | 0.30+ | PostgreSQL driver async |
| PostgreSQL | 15+ | قاعدة البيانات |
| Docker | — | التغليف |
| Railway | — | الاستضافة |

**ليه المكتبات دي؟**
- `aiogram` — حديثة، async، سريعة، community قوية
- `httpx` — async HTTP client، أحسن من aiohttp في الـ API
- `asyncpg` — أسرع PostgreSQL driver للـ Python

---

## المعمارية

### المبدأ الأساسي

كل **feature** ليها مجلد خاص بيها فيه handlers + messages. الكيبوردات والـ validators والـ database في `core/` عشان مفيش تعارض ولا تكرار.

```
main-bot/
├── main.py                          # entry point — بسيط جدا
├── config.py                        # كل المتغيرات في مكان واحد
│
├── core/                            # البنية التحتية المشتركة
│   ├── __init__.py
│   ├── bot.py                       # إنشاء البوت + تسجيل الـ routers
│   ├── db.py                        # PostgreSQL — كل عمليات الداتابيز
│   ├── worker.py                    # Worker API client
│   ├── keyboards.py                 # كل الكيبوردات في مكان واحد
│   ├── middleware.py                 # auth + rate limit + logging
│   └── validators.py                # التحقق من الملفات + التوكنات
│
├── features/                        # كل feature ليها مجلد
│   ├── __init__.py
│   │
│   ├── start/                       # الترحيب + المساعدة
│   │   ├── __init__.py
│   │   ├── handlers.py
│   │   └── messages.py
│   │
│   ├── deploy/                      # نشر البوتات
│   │   ├── __init__.py
│   │   ├── handlers.py
│   │   └── messages.py
│   │
│   └── manage/                      # إدارة البوتات
│       ├── __init__.py
│       ├── handlers.py
│       └── messages.py
│
├── requirements.txt
├── Dockerfile
└── railway.toml
```

---

## هيكل الملفات بالتفصيل

### `main.py` — Entry Point

```python
import asyncio
import logging
from core.bot import create_bot
from core.db import init as init_db, close as close_db

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    bot, dp = create_bot()
    
    try:
        logging.info("Main Bot started!")
        await dp.start_polling(bot)
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(main)
```

**الحجم المتوقع:** ~20 سطر
**المسؤولية:** تشغيل البوت فقط — مفيش أي business logic هنا

---

### `config.py` — المتغيرات

```python
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WORKER_URL = os.getenv("WORKER_URL")
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

**المسؤولية:** قراءة المتغيرات من الـ environment — مفيش أي logic

---

### `core/bot.py` — إنشاء البوت

```python
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from features.start import router as start_router
from features.deploy import router as deploy_router
from features.manage import router as manage_router

def create_bot() -> tuple[Bot, Dispatcher]:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # تسجيل الـ routers بالترتيب
    dp.include_router(start_router)
    dp.include_router(deploy_router)
    dp.include_router(manage_router)
    
    return bot, dp
```

**المسؤولية:** إنشاء البوت + تسجيل كل الـ routers — نقطة واحدة للتجميع

---

### `core/db.py` — قاعدة البيانات

```python
import asyncpg
from config import DATABASE_URL

pool: asyncpg.Pool = None

# === التهيئة ===

async def init():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS bots (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                bot_token TEXT NOT NULL,
                bot_username TEXT,
                status TEXT DEFAULT 'running',
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_bots_user ON bots(user_id)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_bots_status ON bots(user_id, status)")

async def close():
    if pool:
        await pool.close()

# === عمليات البوتات ===

async def add_bot(user_id: int, bot_token: str, bot_username: str = None) -> int:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO bots (user_id, bot_token, bot_username) VALUES ($1, $2, $3) RETURNING id",
            user_id, bot_token, bot_username
        )
        return row["id"]

async def get_user_bots(user_id: int) -> list[dict]:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT * FROM bots WHERE user_id = $1 ORDER BY created_at DESC",
            user_id
        )
        return [dict(r) for r in rows]

async def get_bot_by_id(bot_id: int) -> dict | None:
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM bots WHERE id = $1", bot_id)
        return dict(row) if row else None

async def get_active_bot(user_id: int) -> dict | None:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM bots WHERE user_id = $1 AND status = 'running' ORDER BY created_at DESC LIMIT 1",
            user_id
        )
        return dict(row) if row else None

async def update_status(bot_id: int, status: str):
    async with pool.acquire() as conn:
        await conn.execute("UPDATE bots SET status = $1 WHERE id = $2", status, bot_id)

async def delete_bot(bot_id: int):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM bots WHERE id = $1", bot_id)
```

**المسؤولية:** كل عمليات قاعدة البيانات — أي feature محتاج data بينده هنا

---

### `core/worker.py` — Worker API Client

```python
import httpx
from config import WORKER_URL, INTERNAL_SECRET

class WorkerService:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30)
        self.base = WORKER_URL
        self.headers = {"X-Internal-Secret": INTERNAL_SECRET}

    async def deploy(self, user_id: int, bot_token: str, file_path: str) -> dict:
        with open(file_path, "rb") as f:
            r = await self.client.post(
                f"{self.base}/deploy",
                headers=self.headers,
                data={"user_id": user_id, "bot_token": bot_token},
                files={"file": ("bot.php", f, "application/x-php")}
            )
        return r.json()

    async def stop(self, user_id: int) -> dict:
        r = await self.client.post(
            f"{self.base}/stop",
            headers=self.headers,
            json={"user_id": user_id}
        )
        return r.json()

    async def status(self, user_id: int) -> dict:
        r = await self.client.get(
            f"{self.base}/status/{user_id}",
            headers=self.headers
        )
        return r.json()

    async def health(self) -> dict:
        r = await self.client.get(f"{self.base}/health")
        return r.json()

worker = WorkerService()
```

**المسؤولية:** كل التواصل مع الـ Worker — لو الـ API اتغيّر بتعدّل هنا بس

---

### `core/keyboards.py` — الكيبوردات

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# === كيبوردات قائمة البوتات ===

def bots_list_keyboard(bots: list) -> InlineKeyboardMarkup:
    buttons = []
    for bot in bots:
        icon = "🟢" if bot["status"] == "running" else "🔴"
        name = bot["bot_username"] or f"Bot #{bot['id']}"
        buttons.append([InlineKeyboardButton(
            text=f"{icon} {name}",
            callback_data=f"manage:view:{bot['id']}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# === كيبوردات إدارة بوت واحد ===

def bot_actions_keyboard(bot_id: int, status: str) -> InlineKeyboardMarkup:
    buttons = []
    if status == "running":
        buttons.append(InlineKeyboardButton(text="⏹ إيقاف", callback_data=f"manage:stop:{bot_id}"))
    else:
        buttons.append(InlineKeyboardButton(text="▶ تشغيل", callback_data=f"manage:start:{bot_id}"))
    
    buttons.append(InlineKeyboardButton(text="🗑 حذف", callback_data=f"manage:delete:{bot_id}"))
    buttons.append(InlineKeyboardButton(text="🔙 رجوع", callback_data="manage:back"))
    
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

# === كيبوردات التأكيد ===

def confirm_keyboard(action: str, bot_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ أيوه", callback_data=f"manage:confirm:{action}:{bot_id}"),
        InlineKeyboardButton(text="❌ لا", callback_data=f"manage:cancel:{bot_id}"),
    ]])
```

**نظام الـ callback_data:**
```
manage:view:123           ← عرض بوت 123
manage:stop:123           ← إيقاف بوت 123
manage:start:123          ← تشغيل بوت 123
manage:delete:123         ← طلب حذف 123
manage:confirm:delete:123 ← تأكيد حذف 123
manage:cancel:123         ← إلغاء 123
manage:back               ← رجوع للقائمة الرئيسية
```

---

### `core/middleware.py` — الفلترة

```python
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from config import ADMIN_IDS

class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # استخراج user_id حسب نوع الـ event
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return await handler(event, data)
        
        # ممكن نضيف rate limiting هنا بعدين
        # ممكن نضيف banned users check هنا بعدين
        
        data["user_id"] = user_id
        return await handler(event, data)
```

**المسؤولية:** فلترة الطلبات — ممكن نضيف rate limit و banned users بعدين

---

### `core/validators.py` — التحقق

```python
from aiogram.types import Document
from config import MAX_FILE_SIZE

def validate_php_file(document: Document) -> str | None:
    """يرجع None لو الم_file_ صح، أو رسالة خطأ لو غلط"""
    if not document.file_name or not document.file_name.endswith(".php"):
        return "❌ لازم الملف يكون .php"
    if document.file_size and document.file_size > MAX_FILE_SIZE:
        return "❌ الملف كبير جدا (الحد 10MB)"
    if document.file_size == 0:
        return "❌ الملف فاضي"
    return None

def validate_bot_token(token: str) -> str | None:
    """يرجع None لو التوكن صح، أو رسالة خطأ لو غلط"""
    token = token.strip()
    if ":" not in token:
        return "❌ التوكن غلط. الشكل: 123456:ABC-DEF"
    parts = token.split(":")
    if len(parts) != 2 or not parts[0].isdigit():
        return "❌ التوكن غلط. الشكل: 123456:ABC-DEF"
    return None
```

---

### `features/start/__init__.py`

```python
from .handlers import router
```

---

### `features/start/handlers.py`

```python
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from .messages import WELCOME, HELP

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP)
```

---

### `features/start/messages.py`

```python
WELCOME = """👋 أهلاً بيك في بوت الاستضافة!

ابعتلي ملف PHP + توكن البوت بتاعك وأنا هنشغلك البوت.

📋 الأوامر:
/deploy — نشر بوت جديد
/bots — عرض بوتاتك
/status — حالة البوت
/stop — إيقاف البوت
/help — مساعدة
"""

HELP = """📋 الأوامر المتاحة:

/deploy — نشر بوت جديد (ابعت ملف PHP + توكن)
/bots — عرض كل بوتاتك
/status — حالة البوت النشط
/stop — إيقاف البوت النشط
/delete — حذف البوت
/restart — إعادة تشغيل البوت
/help — الرسالة دي

💡 محتاج مساعدة؟ ابعت /start
"""
```

---

### `features/deploy/__init__.py`

```python
from .handlers import router
```

---

### `features/deploy/handlers.py`

```python
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from core.worker import worker
from core.db import add_bot
from core.validators import validate_php_file, validate_bot_token
from .messages import *

router = Router()

class DeployStates(StatesGroup):
    waiting_file = State()
    waiting_token = State()

@router.message(Command("deploy"))
async def cmd_deploy(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(ASK_FILE)
    await state.set_state(DeployStates.waiting_file)

@router.message(DeployStates.waiting_file, F.document)
async def handle_file(message: Message, state: FSMContext):
    error = validate_php_file(message.document)
    if error:
        return await message.answer(error)
    
    # تحميل الملف
    file = await message.bot.get_file(message.document.file_id)
    path = f"/tmp/{message.from_user.id}_bot.php"
    await message.bot.download_file(file.file_path, path)
    
    await state.update_data(file_path=path)
    await message.answer(ASK_TOKEN)
    await state.set_state(DeployStates.waiting_token)

@router.message(DeployStates.waiting_file)
async def handle_file_wrong(message: Message):
    await message.answer("📎 ابعتلي ملف PHP مش نص")

@router.message(DeployStates.waiting_token, F.text)
async def handle_token(message: Message, state: FSMContext):
    error = validate_bot_token(message.text)
    if error:
        return await message.answer(error)
    
    data = await state.get_data()
    await message.answer(DEPLOYING)
    
    result = await worker.deploy(
        user_id=message.from_user.id,
        bot_token=message.text.strip(),
        file_path=data["file_path"]
    )
    
    if result.get("status") == "ok":
        await add_bot(message.from_user.id, message.text.strip())
        await message.answer(SUCCESS)
    else:
        detail = result.get("detail", "خطأ غير معروف")
        await message.answer(FAILED.format(error=detail))
    
    await state.clear()

@router.message(DeployStates.waiting_token)
async def handle_token_wrong(message: Message):
    await message.answer("🔑 ابعتلي التوكن كنص مش كملف")
```

---

### `features/deploy/messages.py`

```python
ASK_FILE = """📎 ابعتلي ملف الـ PHP بتاع البوت

💡 الملف لازم يكون .php وحجمه أقل من 10MB"""

ASK_TOKEN = """🔑 تمام! ابعتلي توكن البوت من @BotFather

الشكل: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`"""

DEPLOYING = "⏳ جاري نشر البوت..."

SUCCESS = """✅ تم نشر البوت بنجاح!

📱 افتح البوت على تيليجرام وجربه
📋 لو عايز تشوف بوتاتك: /bots"""

FAILED = """❌ حصلت مشكلة أثناء النشر:

{error}

💡 جرب تاني أو ابعت /help"""
```

---

### `features/manage/__init__.py`

```python
from .handlers import router
```

---

### `features/manage/handlers.py`

```python
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from core.db import get_user_bots, get_bot_by_id, update_status, delete_bot
from core.worker import worker
from core.keyboards import bots_list_keyboard, bot_actions_keyboard, confirm_keyboard
from .messages import *

router = Router()

# === أوامر نصية ===

@router.message(Command("bots"))
async def cmd_bots(message: Message):
    bots = await get_user_bots(message.from_user.id)
    if not bots:
        return await message.answer(NO_BOTS)
    await message.answer(YOUR_BOTS, reply_markup=bots_list_keyboard(bots))

@router.message(Command("status"))
async def cmd_status(message: Message):
    result = await worker.status(message.from_user.id)
    status = result.get("status", "not_found")
    await message.answer(STATUS_TEXT.format(status=STATUS_MAP.get(status, status)))

@router.message(Command("stop"))
async def cmd_stop(message: Message):
    bot = await get_active_bot(message.from_user.id)
    if not bot:
        return await message.answer(NO_ACTIVE_BOT)
    
    await worker.stop(message.from_user.id)
    await update_status(bot["id"], "stopped")
    await message.answer(STOPPED)

@router.message(Command("restart"))
async def cmd_restart(message: Message):
    bot = await get_active_bot(message.from_user.id)
    if not bot:
        return await message.answer(NO_ACTIVE_BOT)
    
    await message.answer(RESTARTING)
    await worker.stop(message.from_user.id)
    
    result = await worker.deploy(
        user_id=message.from_user.id,
        bot_token=bot["bot_token"],
        file_path=f"/tmp/{message.from_user.id}_bot.php"
    )
    
    if result.get("status") == "ok":
        await update_status(bot["id"], "running")
        await message.answer(RESTARTED)
    else:
        await message.answer(RESTART_FAILED)

# === Callback handlers ===

@router.callback_query(F.data.startswith("manage:view:"))
async def cb_view(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[2])
    bot = await get_bot_by_id(bot_id)
    
    if not bot or bot["user_id"] != callback.from_user.id:
        return await callback.answer("❌ مش بوتك!", show_alert=True)
    
    text = BOT_DETAILS.format(
        bot_id=bot["id"],
        status="شغال 🟢" if bot["status"] == "running" else "موقوف 🔴",
        created=bot["created_at"].strftime("%Y-%m-%d %H:%M")
    )
    await callback.message.edit_text(
        text,
        reply_markup=bot_actions_keyboard(bot["id"], bot["status"])
    )

@router.callback_query(F.data.startswith("manage:stop:"))
async def cb_stop(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[2])
    bot = await get_bot_by_id(bot_id)
    
    if not bot or bot["user_id"] != callback.from_user.id:
        return await callback.answer("❌ مش بوتك!", show_alert=True)
    
    await worker.stop(callback.from_user.id)
    await update_status(bot_id, "stopped")
    await callback.answer("✅ تم الإيقاف")
    
    bot = await get_bot_by_id(bot_id)
    await callback.message.edit_reply_markup(
        reply_markup=bot_actions_keyboard(bot_id, bot["status"])
    )

@router.callback_query(F.data.startswith("manage:start:"))
async def cb_start(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[2])
    bot = await get_bot_by_id(bot_id)
    
    if not bot or bot["user_id"] != callback.from_user.id:
        return await callback.answer("❌ مش بوتك!", show_alert=True)
    
    result = await worker.deploy(
        user_id=callback.from_user.id,
        bot_token=bot["bot_token"],
        file_path=f"/tmp/{callback.from_user.id}_bot.php"
    )
    
    if result.get("status") == "ok":
        await update_status(bot_id, "running")
        await callback.answer("✅ تم التشغيل")
        bot = await get_bot_by_id(bot_id)
        await callback.message.edit_reply_markup(
            reply_markup=bot_actions_keyboard(bot_id, bot["status"])
        )
    else:
        await callback.answer("❌ فشل التشغيل", show_alert=True)

@router.callback_query(F.data.startswith("manage:delete:"))
async def cb_delete_confirm(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[2])
    bot = await get_bot_by_id(bot_id)
    
    if not bot or bot["user_id"] != callback.from_user.id:
        return await callback.answer("❌ مش بوتك!", show_alert=True)
    
    await callback.message.edit_text(
        DELETE_CONFIRM,
        reply_markup=confirm_keyboard("delete", bot_id)
    )

@router.callback_query(F.data.startswith("manage:confirm:delete:"))
async def cb_delete(callback: CallbackQuery):
    bot_id = int(callback.data.split(":")[3])
    bot = await get_bot_by_id(bot_id)
    
    if not bot or bot["user_id"] != callback.from_user.id:
        return await callback.answer("❌ مش بوتك!", show_alert=True)
    
    await worker.stop(callback.from_user.id)
    await delete_bot(bot_id)
    await callback.message.edit_text(DELETED)

@router.callback_query(F.data.startswith("manage:cancel:"))
async def cb_cancel(callback: CallbackQuery):
    await callback.message.edit_text(CANCELLED)

@router.callback_query(F.data == "manage:back")
async def cb_back(callback: CallbackQuery):
    bots = await get_user_bots(callback.from_user.id)
    if not bots:
        await callback.message.edit_text(NO_BOTS)
    else:
        await callback.message.edit_text(
            YOUR_BOTS,
            reply_markup=bots_list_keyboard(bots)
        )
```

---

### `features/manage/messages.py`

```python
NO_BOTS = "📭 مفيش عندك بوتات حالياً\n\nابعت /deploy عشان تنشر بوت جديد"

YOUR_BOTS = "📋 بوتاتك:"

BOT_DETAILS = """🤖 بوت #{bot_id}

📊 الحالة: {status}
📅 اتสร: {created}"""

NO_ACTIVE_BOT = "📭 مفيش بوت نشط حالياً"

STOPPED = "⏹ تم إيقاف البوت"

RESTARTING = "🔄 جاري إعادة التشغيل..."

RESTARTED = "✅ تم إعادة التشغيل بنجاح!"

RESTART_FAILED = "❌ فشل إعادة التشغيل"

DELETE_CONFIRM = "⚠️ متأكد إنك عايز ت_delete_ البوت؟\n\nالملف هيتحذف من السيرفر."

DELETED = "🗑 تم حذف البوت"

CANCELLED = "👌 تم الإلغاء"

STATUS_MAP = {
    "running": "شغال 🟢",
    "stopped": "موقوف 🔴",
    "not_found": "مش موجود ❓"
}

STATUS_TEXT = "📊 حالة البوت: {status}"
```

---

## قاعدة البيانات — PostgreSQL

### الجداول

```sql
CREATE TABLE bots (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,           -- Telegram user ID
    bot_token TEXT NOT NULL,            -- Bot token from BotFather
    bot_username TEXT,                  -- Bot username (optional)
    status TEXT DEFAULT 'running',      -- running | stopped
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_bots_user ON bots(user_id);
CREATE INDEX idx_bots_status ON bots(user_id, status);
```

### العمليات

| الدالة | الوظيفة |
|--------|---------|
| `add_bot(user_id, token, username)` | إضافة بوت جديد |
| `get_user_bots(user_id)` | كل بوتات المستخدم |
| `get_bot_by_id(bot_id)` | بوت بالـ ID |
| `get_active_bot(user_id)` | البوت النشط |
| `update_status(bot_id, status)` | تحديث الحالة |
| `delete_bot(bot_id)` | حذف البوت |

---

## سير العمل (Workflows)

### 1. نشر بوت جديد

```
المستخدم: /deploy
    ↓
البوت: "ابعتلي ملف PHP"
    ↓
المستخدم: [يرفع ملف.php]
    ↓
البوت: validate_php_file()
    ↓ (لو غلط)
البوت: "الملف لازم يكون .php" → STOP
    ↓ (لو صح)
البوت: يحمّل الملف → /tmp/{user_id}_bot.php
البوت: "ابعتلي توكن البوت"
    ↓
المستخدم: 123456:ABC-DEF
    ↓
البوت: validate_bot_token()
    ↓ (لو غلط)
البوت: "التوكن غلط" → STOP
    ↓ (لو صح)
البوت: worker.deploy(user_id, token, file_path)
    ↓
Worker: يحفظ الملف + يسجّل webhook
    ↓
البوت: db.add_bot(user_id, token)
البوت: "✅ تم النشر!"
```

### 2. عرض البوتات

```
المستخدم: /bots
    ↓
البوت: db.get_user_bots(user_id)
    ↓ (لو مفيش)
البوت: "مفيش بوتات" → STOP
    ↓ (لو فيه)
البوت: يعرض قائمة بأزرار inline
    ↓
المستخدم: يضغط على بوت
    ↓
البوت: يعرض تفاصيل + أزرار (إيقاف/تشغيل/حذف)
```

### 3. إيقاف بوت

```
المستخدم: يضغط "إيقاف"
    ↓
البوت: worker.stop(user_id)
    ↓
Worker: يحذف webhook من تيليجرام
    ↓
البوت: db.update_status(bot_id, "stopped")
البوت: يحدّث الأزرار (الزر "تشغيل" يظهر)
```

### 4. حذف بوت

```
المستخدم: يضغط "حذف"
    ↓
البوت: "متأكد؟" + أزرار تأكيد
    ↓
المستخدم: يضغط "أيوه"
    ↓
البوت: worker.stop(user_id)
البوت: db.delete_bot(bot_id)
البوت: "تم الحذف"
```

---

## Environment Variables

| المتغير | الوصف | مثال |
|---------|-------|------|
| `BOT_TOKEN` | توكن البوت من BotFather | `123456:ABC-DEF` |
| `WORKER_URL` | عنوان الـ Worker | `https://worker.up.railway.app` |
| `INTERNAL_SECRET` | السر المشترك مع الـ Worker | `a1b2c3d4...` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `ADMIN_IDS` | IDs الأدمنات (اختياري) | `123456,789012` |

---

## البناء — الترتيب

### المرحلة 1: الأساس
1. إنشاء المجلدات والملفات
2. `config.py` + `requirements.txt`
3. `core/db.py` — قاعدة البيانات
4. `core/worker.py` — Worker client
5. `core/validators.py` — التحقق
6. `core/keyboards.py` — الكيبوردات
7. `core/bot.py` — إنشاء البوت
8. `main.py` — entry point

### المرحلة 2: Features
1. `features/start/` — الترحيب
2. `features/deploy/` — النشر
3. `features/manage/` — الإدارة

### المرحلة 3: التغليف
1. `Dockerfile`
2. `railway.toml`
3. اختبار على Railway

### المرحلة 4: تحسينات (بدين)
1. Rate limiting في middleware
2. Banned users
3. Admin commands
4. Logging
5. Error handling أفضل
6. Marketplace (بوتات جاهزة)

---

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

---

## railway.toml

```toml
[build]
builder = "dockerfile"

[deploy]
startCommand = "python main.py"
healthcheckPath = "/health"
restartPolicyType = "on_failure"
```

---

## ملاحظات أمنية

1. **التوكنات** بتتخزن في PostgreSQL مش في ملفات
2. **الـ INTERNAL_SECRET** لازم يكون معقد وطويل
3. **الـ DATABASE_URL** لازم يكون في environment variables مش في الكود
4. **المستخدم** ميقدرش يشوف بوتات مستخدم تاني (كل query فيها `user_id`)
5. **الملفات** بتتحفظ في `/tmp` — بتمسح لما الـ container ي restart

---

## ملاحظات تقنية

1. **FSM storage** — `MemoryStorage` — الـ state بيروح لما الـ container ي restart. ممكن نغيّره لـ Redis بعدين لو محتاجين persistence
2. **File storage** — الملفات في `/tmp` — مش persistent. الـ Worker هو اللي بيحفظ الملفات نهائياً
3. **Connection pool** — asyncpg بيستخدم pool — مناسب للـ concurrent requests
4. **Timeout** — httpx client.timeout = 30s — مناسب للـ Worker API calls
