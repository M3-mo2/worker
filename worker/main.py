import os
import json
import time
import hmac
import logging
import asyncio
from pathlib import Path
from typing import Optional

import httpx
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, Header
from fastapi.responses import JSONResponse, PlainTextResponse

# ===== Config =====
INTERNAL_SECRET = os.environ.get("INTERNAL_SECRET", "")
RAILWAY_PUBLIC_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
CF_WEBHOOK_BASE = os.environ.get("CF_WEBHOOK_BASE", "")
MAIN_BOT_URL = os.environ.get("MAIN_BOT_URL", "")
CADDY_INTERNAL_PORT = int(os.environ.get("CADDY_INTERNAL_PORT", "9000"))

BOTS_DIR = Path("/app/user_bots")
DATA_FILE = Path("/app/data/bots.json")

TELEGRAM_API = "https://api.telegram.org"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("worker")

# ===== In-Memory State =====
bots: dict[str, dict] = {}  # user_id -> bot info
http_client: Optional[httpx.AsyncClient] = None

# ===== FastAPI App =====
app = FastAPI(title="PHP Worker")


# ===== Security =====
async def verify_secret(x_internal_secret: str = Header(...)):
    if not INTERNAL_SECRET:
        raise HTTPException(status_code=500, detail="INTERNAL_SECRET not configured")
    if not hmac.compare_digest(x_internal_secret, INTERNAL_SECRET):
        raise HTTPException(status_code=403, detail="Invalid secret")


# ===== Helpers =====
def get_user_dir(user_id: int) -> Path:
    return BOTS_DIR / str(user_id)


def save_bots():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = DATA_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(bots, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, DATA_FILE)


def load_bots():
    global bots
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            bots = json.load(f)
    logger.info(f"Loaded {len(bots)} bots from disk")


def _normalize_base(raw: str) -> str:
    """يطبّع رابط الأساس: يشيل الفواصل الزايدة ويضيف https:// لو ناقص.

    كده سواء المتغير فيه https:// أو لأ، النتيجة رابط صح من غير تكرار للـ scheme
    (السبب الأصلي لخطأ "invalid webhook URL specified")."""
    raw = (raw or "").strip().rstrip("/")
    if not raw:
        return ""
    if not raw.startswith("http://") and not raw.startswith("https://"):
        raw = "https://" + raw
    return raw


async def set_webhook(user_id: int, bot_token: str, webhook_secret: str):
    # نفضّل الـ Cloudflare router (CF_WEBHOOK_BASE) عشان الرابط نضيف وقابل للتوجيه،
    # وإلا نقعّد على دومين الـ Railway بتاع العامل نفسه.
    base = _normalize_base(CF_WEBHOOK_BASE) or _normalize_base(RAILWAY_PUBLIC_DOMAIN)
    if not base:
        raise HTTPException(
            status_code=500,
            detail="No CF_WEBHOOK_BASE or RAILWAY_PUBLIC_DOMAIN configured",
        )
    webhook_url = f"{base}/webhook/{user_id}"
    resp = await http_client.post(
        f"{TELEGRAM_API}/bot{bot_token}/setWebhook",
        json={
            "url": webhook_url,
            "secret_token": webhook_secret,
            "allowed_updates": ["message", "callback_query", "inline_query"],
        },
    )
    return resp.json()


async def delete_webhook(bot_token: str):
    resp = await http_client.post(f"{TELEGRAM_API}/bot{bot_token}/deleteWebhook")
    return resp.json()


# ===== API Endpoints =====
@app.post("/deploy")
async def deploy(request: Request, _=Depends(verify_secret)):
    form = await request.form()
    user_id = form.get("user_id")
    bot_token = form.get("bot_token")
    file = form.get("file")

    if not all([user_id, bot_token, file]):
        raise HTTPException(status_code=400, detail="Missing user_id, bot_token, or file")

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid user_id")

    if not file.filename.endswith(".php"):
        raise HTTPException(status_code=400, detail="Only .php files are allowed")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 10MB)")

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    # Save file
    user_dir = get_user_dir(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    bot_file = user_dir / "bot.php"
    bot_file.write_bytes(content)
    logger.info(f"Saved bot file for user {user_id}: {bot_file} ({len(content)} bytes)")

    # Save config.json so PHP can read the token
    config_file = user_dir / "config.json"
    config_file.write_text(json.dumps({"bot_token": bot_token}))
    logger.info(f"Saved config for user {user_id} (token length {len(bot_token)})")

    # Generate webhook secret
    webhook_secret = os.urandom(24).hex()

    # Set Telegram webhook
    result = await set_webhook(user_id, bot_token, webhook_secret)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=f"Telegram error: {result.get('description', 'Unknown')}")

    # Save bot info
    bots[str(user_id)] = {
        "user_id": user_id,
        "bot_token": bot_token,
        "webhook_secret": webhook_secret,
        "status": "running",
        "created_at": time.time(),
    }
    save_bots()

    logger.info(f"Deployed bot for user {user_id}")
    return {"status": "ok", "user_id": user_id, "webhook_secret": webhook_secret, "message": "Bot deployed successfully"}


@app.post("/stop")
async def stop(request: Request, _=Depends(verify_secret)):
    data = await request.json()
    user_id = data.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")

    user_id = int(user_id)
    bot = bots.get(str(user_id))
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    # Delete webhook
    await delete_webhook(bot["bot_token"])

    # Update status
    bots[str(user_id)]["status"] = "stopped"
    save_bots()

    logger.info(f"Stopped bot for user {user_id}")
    return {"status": "ok", "user_id": user_id, "message": "Bot stopped"}


@app.get("/status/{user_id}")
async def status(user_id: int, _=Depends(verify_secret)):
    bot = bots.get(str(user_id))
    if not bot:
        return {"user_id": user_id, "status": "not_found"}

    return {
        "user_id": user_id,
        "status": bot["status"],
        "created_at": bot.get("created_at"),
    }


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": time.time()}


# ===== Webhook Receiver =====
@app.post("/webhook/{user_id}")
async def webhook(user_id: int, request: Request):
    bot = bots.get(str(user_id))
    if not bot:
        logger.warning(f"Webhook received for UNKNOWN user {user_id} — no bot registered")
        return PlainTextResponse("ok")

    if bot["status"] != "running":
        logger.warning(f"Webhook received for STOPPED bot {user_id} (status={bot['status']})")
        return PlainTextResponse("ok")

    # Validate Telegram secret
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not hmac.compare_digest(secret_token, bot.get("webhook_secret", "")):
        logger.warning(f"Webhook secret MISMATCH for user {user_id} — ignoring")
        return PlainTextResponse("ok")

    # Check payload size
    body = await request.body()
    if len(body) > 1024 * 1024:
        logger.warning(f"Webhook payload too large for user {user_id}: {len(body)} bytes")
        raise HTTPException(status_code=413, detail="Payload too large")

    # Validate JSON
    try:
        json.loads(body)
    except (json.JSONDecodeError, ValueError):
        logger.warning(f"Webhook payload is not valid JSON for user {user_id}: {body[:200]!r}")
        return PlainTextResponse("ok")

    # Forward to Caddy internal for PHP-FPM execution
    internal_url = f"http://127.0.0.1:{CADDY_INTERNAL_PORT}/internal/php/{user_id}/bot.php"
    try:
        resp = await http_client.post(
            internal_url,
            content=body,
            headers={"Content-Type": "application/json"},
            timeout=30.0,
        )
    except httpx.TimeoutException:
        logger.error(f"PHP EXECUTION TIMEOUT (>30s) for user {user_id} at {internal_url}")
        return PlainTextResponse("ok")
    except Exception as e:
        logger.error(f"PHP EXECUTION ERROR for user {user_id} at {internal_url}: {e!r}")
        return PlainTextResponse("ok")

    # Log the outcome of running the bot file so problems are discoverable.
    # PHP echoes errors into the body (display_errors=On), so surface it.
    status = resp.status_code
    preview = resp.text or ""
    if len(preview) > 1000:
        preview = preview[:1000] + "...[truncated]"
    if status != 200:
        logger.error(
            f"PHP file RAN for user {user_id} but returned HTTP {status}. body={preview!r}"
        )
    else:
        logger.info(
            f"PHP file EXECUTED for user {user_id}: HTTP 200, body_preview={preview!r}"
        )
    return PlainTextResponse(resp.content, status_code=status)


# ===== Lifecycle =====
@app.on_event("startup")
async def startup():
    global http_client
    http_client = httpx.AsyncClient(timeout=httpx.Timeout(30.0))

    BOTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    load_bots()

    # Register with main bot
    if MAIN_BOT_URL and RAILWAY_PUBLIC_DOMAIN and INTERNAL_SECRET:
        for attempt in range(5):
            try:
                resp = await http_client.post(
                    f"{MAIN_BOT_URL}/worker/register",
                    json={
                        "worker_url": _normalize_base(RAILWAY_PUBLIC_DOMAIN),
                        "secret": INTERNAL_SECRET,
                    },
                    timeout=10.0,
                )
                if resp.status_code == 200:
                    logger.info("Registered with main bot successfully")
                    break
                logger.warning(f"Registration failed (attempt {attempt + 1}): {resp.status_code}")
            except Exception as e:
                logger.warning(f"Registration error (attempt {attempt + 1}): {e}")
            await asyncio.sleep(3)
    else:
        logger.warning("MAIN_BOT_URL or RAILWAY_PUBLIC_DOMAIN or INTERNAL_SECRET not set, skipping registration")


@app.on_event("shutdown")
async def shutdown():
    if http_client:
        await http_client.aclose()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
