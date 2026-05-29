#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import time
import asyncio
import logging
import hmac
from pathlib import Path
from aiohttp import web, ClientSession, ClientTimeout
import aiofiles
import aiosqlite

# Import settings from the core package
from bot.core.config import settings

# ===== إعدادات المسارات (Standardized) =====
# نستخدم نفس المسار الموجود في إعدادات البوت لضمان التطابق التام
DATA_DIR = Path(settings.PROJECT_ROOT) / 'data'

BOTS_FILE = DATA_DIR / 'bots.json'
HOST_SETTINGS_FILE = DATA_DIR / 'host_settings.json'
DB_PATH = DATA_DIR / 'main_bot.db' # Using the main shared DB
LOG_FILE = DATA_DIR / 'webhook_dispatch_log.txt'

INTERNAL_SECRET = settings.INTERNAL_SECRET
ENGINE_URL = settings.php_engine.CADDY_BASE_URL
ENGINE_FREE_URL = ENGINE_URL
ENGINE_PAID_URL = ENGINE_URL
MAX_PAYLOAD_BYTES = settings.MAX_PAYLOAD_BYTES
REQUEST_TIMEOUT = settings.REQUEST_TIMEOUT
HOST = settings.web.WEBHOOK_HOST
PORT = settings.web.WEBHOOK_PORT

logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] %(levelname)s %(message)s')
logger = logging.getLogger('dispatcher')

# ===== وضع المطور (Developer Mode) =====
DEV_MODE = getattr(settings, 'DEV_MODE', False)  # Unified with main config

# ===== global placeholders =====
_client = None
_db_lock = asyncio.Lock()

# متغيرات للكاش الذكي (عشان السرعة والتحديث الفوري)
_BOTS_CACHE = {}      # هنا هنحفظ البيانات في الرامات
_LAST_MTIME = 0.0     # هنا هنحفظ وقت آخر تعديل للملف
_HOST_SETTINGS_CACHE = {}
_HS_LAST_MTIME = 0.0

# ===== Helpers =====
async def logline(s: str):
    """تسجيل الأحداث في وضع المطور"""
    if not DEV_MODE:
        return
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {s}\n"
    
    # الكتابة في الملف والطباعة في الكونسول
    print(f"📝 {s}")
    try:
        async with aiofiles.open(LOG_FILE, 'a', encoding='utf-8') as f:
            await f.write(log_message)
    except Exception as e:
        print(f"❌ Failed to write to log: {e}")

async def load_bots():
    """
    دالة ذكية بتحمل البوتات فقط لو الملف اتغير.
    """
    global _BOTS_CACHE, _LAST_MTIME
    
    try:
        if not BOTS_FILE.exists():
            # لو الملف مش موجود أصلاً
            logger.error(f"Bots file not found at {BOTS_FILE}")
            return {}

        # بنجيب وقت آخر تعديل للملف (عملية سريعة جداً)
        current_mtime = os.path.getmtime(BOTS_FILE)

        # المقارنة: هل وقت التعديل اختلف عن آخر مرة؟
        if current_mtime != _LAST_MTIME:
            # لو اختلف، يبقى الملف اتعدل -> نقرأه من جديد
            async with aiofiles.open(BOTS_FILE, 'r', encoding='utf-8') as f:
                data = await f.read()
                _BOTS_CACHE = json.loads(data)
                _LAST_MTIME = current_mtime # نحدث وقت آخر تعديل
                # logger.info("Bots reloaded from disk due to file change")
        
        # لو مفيش تغيير، بنرجع القديم من الرامات علطول
        return _BOTS_CACHE

    except Exception as e:
        # لو حصل أي خطأ، نرجع آخر نسخة شغالة معانا
        logger.error(f"Error loading bots: {e}")
        return _BOTS_CACHE

async def load_host_settings_cached():
    """تحميل إعدادات الاستضافة مع الكاش"""
    global _HOST_SETTINGS_CACHE, _HS_LAST_MTIME
    try:
        if not HOST_SETTINGS_FILE.exists():
            return {}
        
        current_mtime = os.path.getmtime(HOST_SETTINGS_FILE)
        if current_mtime != _HS_LAST_MTIME:
            async with aiofiles.open(HOST_SETTINGS_FILE, 'r', encoding='utf-8') as f:
                data = await f.read()
                _HOST_SETTINGS_CACHE = json.loads(data)
                _HS_LAST_MTIME = current_mtime
        return _HOST_SETTINGS_CACHE
    except Exception as e:
        return _HOST_SETTINGS_CACHE

def constant_time_compare(a: str, b: str) -> bool:
    try:
        return hmac.compare_digest(a.encode(), b.encode())
    except Exception:
        return False

# ===== 🗄️ Database Operations (New Queue System) =====
async def init_db():
    async with aiosqlite.connect(DB_PATH, timeout=30) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT NOT NULL,
                owner_id INTEGER NOT NULL,
                path TEXT NOT NULL,
                raw_data TEXT NOT NULL,
                created_at REAL NOT NULL,
                tries INTEGER DEFAULT 0,
                reported INTEGER DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS webhook_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT NOT NULL,
                ts REAL NOT NULL,
                status INTEGER NOT NULL,
                response TEXT
            )
        """)
        await db.execute("CREATE INDEX IF NOT EXISTS idx_queue_token ON queue (token)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_queue_owner ON queue (owner_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_logs_token ON webhook_logs (token)")
        await db.commit()

async def insert_update(token: str, owner_id: int, path: str, raw_data: str) -> int:

    async with _db_lock:
        async with aiosqlite.connect(DB_PATH, timeout=30) as db:
            cursor = await db.execute(
                "INSERT INTO queue (token, owner_id, path, raw_data, created_at, tries) VALUES (?, ?, ?, ?, ?, 0)",
                (token, owner_id, path, raw_data, time.time())
            )
            await db.commit()
            return cursor.lastrowid

async def delete_update(row_id: int):
    """حذف التحديث من الطابور بعد نجاح تسليمه"""
    async with _db_lock:
        async with aiosqlite.connect(DB_PATH, timeout=30) as db:
            await db.execute("DELETE FROM queue WHERE id = ?", (row_id,))
            await db.commit()

async def forward_update(path: str, raw: bytes, engine_base: str) -> tuple[int, str]:
    target = f"{engine_base.rstrip('/')}/{path.lstrip('/')}"
    headers = {
        "Content-Type": "application/json",
        "X-Internal-Secret": INTERNAL_SECRET,
        "X-Forwarded-By": "dispatcher"
    }
    global _client
    if _client is None: return 0, "No HTTP client"
    try:
        async with _client.post(target, data=raw, headers=headers) as resp:
            body = await resp.text()
            return resp.status, body
    except asyncio.TimeoutError:
        return 408, "Timeout detected"
    except Exception as e:
        return 0, str(e)

# ===== Handler =====
async def webhook_handler(request: web.Request):
    token = request.query.get('tk')
    if not token:
        return web.Response(status=400, text="No token provided")
    
    await logline(f"🔵 NEW REQUEST | Token: {token} | IP: {request.remote}")

    try:
        bots = await load_bots()
    except FileNotFoundError:
        return web.Response(status=500, text="bots.json not found")
    except Exception as e:
        await logline(f"LOAD_BOTS_ERR {e}")
        return web.Response(status=500, text="Failed to read bots.json")

    await logline(f"🔍 Checking token in bots.json... (Loaded {len(bots)} bots)")
    bot = bots.get(token)
    if not bot:
        await logline(f"❌ Token NOT FOUND in bots.json")
        return web.Response(status=404, text="Unknown bot token")
    status = bot.get("status", "").lower().strip()
    webhook_set = bool(bot.get("webhook_set", False))

    if status == "stopped" and not webhook_set:
        await logline(f"IGNORED token={token[:8]} (stopped + no webhook)")
        return web.json_response({"ok": True})


    rel_path = (bot.get('path') or '').strip('/')
    if not rel_path:
        return web.Response(status=500, text="Invalid bot path")

    # Fix: Ensure secrets are strings and stripped of whitespace
    bot_secret = str(bot.get('secret') or '').strip()
    header_secret = request.headers.get('X-Telegram-Bot-Api-Secret-Token', '').strip()

    await logline(f"🔐 SECRET CHECK | Configured: '{bot_secret}' | Received Header: '{header_secret}'")

    if bot_secret:
        if not header_secret or not constant_time_compare(bot_secret, header_secret):
            await logline(f"SECRET_MISMATCH token={token[:8]}")
            # Log partial secrets for debugging (first 3 chars + ***)
            safe_bot_sec = bot_secret[:3] + "***" if len(bot_secret) > 3 else "***"
            safe_hdr_sec = header_secret[:3] + "***" if len(header_secret) > 3 else "***"
            await logline(f"SECRET_MISMATCH token={token[:8]} DB={safe_bot_sec} HDR={safe_hdr_sec}")

            return web.Response(status=403, text="Forbidden")
        else:
            await logline(f"✅ SECRET MATCHED successfully.")
    else:
        await logline(f"NO_BOT_SECRET token={token[:8]}")
        # If no secret is configured in bots.json, we log it but might allow it (or block depending on policy)
        # For security, it's better to warn.
        await logline(f"NO_BOT_SECRET_CONFIGURED token={token[:8]}")


    if request.content_length and request.content_length > MAX_PAYLOAD_BYTES:
        return web.Response(status=413, text="Payload too large")


    raw = await request.read()
    if not raw:
        return web.json_response({"ok": True})
    
    raw_str = raw.decode('utf-8', errors='replace')
    await logline(f"📦 PAYLOAD RECEIVED ({len(raw)} bytes):\n{raw_str[:500]}... (truncated)")


    try:
        json.loads(raw_str)
    except Exception:
        await logline(f"❌ INVALID JSON format.")
        return web.Response(status=400, text="Invalid JSON")


    if '..' in rel_path or '//' in rel_path or rel_path.startswith('/'):
        await logline(f"INVALID_PATH token={token[:8]} path={rel_path}")
        return web.json_response({"ok": True})



    owner_id = int(bot.get('owner', 0))


    try:
        row_id = await insert_update(token, owner_id, rel_path, raw_str)
        await logline(f"QUEUED DB_ID={row_id} token={token[:8]}")
        await logline(f"ACCEPTED token={token[:8]} path={rel_path}") # Confirm acceptance
    except Exception as e:
        await logline(f"DB_INSERT_ERR {e}")
        return web.json_response({"ok": True})

    bot_tier = bot.get('tier', 'free')
    
    # --- التحقق من الوضع المجاني العام ---
    host_settings = await load_host_settings_cached()
    if host_settings.get('bot_mode') == 'free':
        bot_tier = 'pro' # ترقية مؤقتة للأداء
    # -------------------------------------

    current_engine_base = ENGINE_PAID_URL if bot_tier == 'pro' else ENGINE_FREE_URL

    response = web.json_response({"ok": True})
    asyncio.create_task(process_forward_task(rel_path, raw, row_id, current_engine_base, bot_tier, token))
    return web.json_response({"ok": True})

async def process_forward_task(rel_path: str, raw: bytes, row_id: int, engine_base: str, tier: str, token: str):
    if tier == 'free': await asyncio.sleep(0.3)
    
    code, body = await forward_update(rel_path, raw, engine_base)
    
    # --- NEW COMPREHENSIVE ERROR CHECK ---
    is_successful = 200 <= code < 300
    final_code = code
    
    # Check for PHP error signatures in the response body, case-insensitively.
    body_lower = body.lower()
    error_signatures = [
        '<b>warning</b>', 
        '<b>fatal error</b>', 
        '<b>parse error</b>',
        '<b>notice</b>',
        'uncaught exception'
    ]
    
    if any(sig in body_lower for sig in error_signatures):
        is_successful = False
        # If the original code was OK, override it to indicate a server error for logging.
        if 200 <= code < 300:
            final_code = 500 # Internal Server Error

    # --- END NEW CHECK ---

    try:
        async with aiosqlite.connect(DB_PATH, timeout=30) as db:
            await db.execute(
                "INSERT INTO webhook_logs (token, ts, status, response) VALUES (?, ?, ?, ?)",
                (token, time.time(), final_code, body) # Log the potentially overridden code
            )
            await db.execute("""
                DELETE FROM webhook_logs WHERE id NOT IN (
                    SELECT id FROM webhook_logs WHERE token = ? ORDER BY id DESC LIMIT 20
                ) AND token = ?
            """, (token, token))
            await db.commit()
    except Exception as e:
        await logline(f"LOG_INSERT_ERR {e}")

    # Use the final success status to manage the queue
    if is_successful:
        await delete_update(row_id)
    else:
        async with aiosqlite.connect(DB_PATH, timeout=30) as db:
            await db.execute("UPDATE queue SET tries = tries + 1 WHERE id = ?", (row_id,))
            await db.commit()

# ===== lifecycle =====
async def on_startup(app):
    global _client
    _client = ClientSession(timeout=ClientTimeout(total=REQUEST_TIMEOUT))
    await init_db()
    await logline("STARTUP: DB initialized, client session ready")

async def on_cleanup(app):
    global _client
    if _client:
        await _client.close()
        _client = None
    await logline("CLEANUP: client closed")

# ===== app =====
app = web.Application()
app.router.add_post('/webhook', webhook_handler)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

if __name__ == '__main__':
    logger.info(f"Starting dispatcher on {HOST}:{PORT} (Free Engine: {ENGINE_FREE_URL}, Paid Engine: {ENGINE_PAID_URL})")
    logger.info(f"Using DATA_DIR: {DATA_DIR}")
    print("تـم تـشـغـل الـويـبـهوك ✅")
    web.run_app(app, host=HOST, port=PORT)