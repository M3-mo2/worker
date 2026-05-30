import os
import httpx
import logging
import asyncio
from config import (
    WORKER_URL, INTERNAL_SECRET,
    CF_ACCOUNT_ID, CF_KV_ID, CF_API_TOKEN, CF_WEBHOOK_BASE
)


class WorkerService:
    def __init__(self, url: str = None, secret: str = None):
        self.client = httpx.AsyncClient(timeout=30)
        self.base = url or WORKER_URL
        self.headers = {"X-Internal-Secret": secret or INTERNAL_SECRET}

    async def deploy(self, user_id: int, bot_token: str, file_path: str) -> dict:
        try:
            if not os.path.exists(file_path):
                return {"detail": "الملف مش موجود. ابدأ النشر من الأول."}

            with open(file_path, "rb") as f:
                r = await self.client.post(
                    f"{self.base}/deploy",
                    headers=self.headers,
                    data={"user_id": user_id, "bot_token": bot_token},
                    files={"file": ("bot.php", f, "application/x-php")}
                )

            if r.status_code == 403:
                return {"detail": "السر (INTERNAL_SECRET) غلط. تأكد من إعدادات الـ Worker."}
            if r.status_code == 400:
                data = r.json()
                return {"detail": data.get("detail", "طلب غير صالح")}
            if r.status_code != 200:
                return {"detail": f"خطأ من الـ Worker: {r.status_code}"}

            return r.json()
        except FileNotFoundError:
            return {"detail": "الملف مش موجود. ابدأ النشر من الأول."}
        except Exception as e:
            logging.error(f"Worker deploy error: {e}")
            return {"detail": "الخدمة مش متاحة دلوقتي"}

    async def stop(self, user_id: int) -> dict:
        try:
            r = await self.client.post(
                f"{self.base}/stop",
                headers=self.headers,
                json={"user_id": user_id}
            )
            return r.json()
        except Exception as e:
            logging.error(f"Worker stop error: {e}")
            return {"detail": "الخدمة مش متاحة دلوقتي"}

    async def status(self, user_id: int) -> dict:
        try:
            r = await self.client.get(
                f"{self.base}/status/{user_id}",
                headers=self.headers
            )
            return r.json()
        except Exception as e:
            logging.error(f"Worker status error: {e}")
            return {"status": "unknown"}

    async def health(self) -> dict:
        try:
            r = await self.client.get(f"{self.base}/health")
            return r.json()
        except Exception as e:
            logging.error(f"Worker health error: {e}")
            return {"status": "unreachable"}

    async def register_routing(self, user_id: str) -> dict:
        if not all([CF_ACCOUNT_ID, CF_KV_ID, CF_API_TOKEN, CF_WEBHOOK_BASE]):
            logging.warning("Cloudflare config missing, skipping KV registration")
            return {"status": "skipped", "reason": "missing config"}

        url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{CF_ACCOUNT_ID}/storage/kv/namespaces/{CF_KV_ID}/values/{user_id}"
        )
        headers = {
            "Authorization": f"Bearer {CF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        try:
            r = await self.client.put(
                url,
                headers=headers,
                content=self.base.encode()
            )
            data = r.json()
            if data.get("success"):
                logging.info(f"KV registered: {user_id} -> {self.base}")
                return {"status": "ok"}
            else:
                errors = data.get("errors", [])
                logging.error(f"KV registration failed: {errors}")
                return {"status": "error", "detail": str(errors)}
        except Exception as e:
            logging.error(f"KV registration error: {e}")
            return {"status": "error", "detail": str(e)}

    def get_webhook_url(self, user_id: int) -> str:
        if CF_WEBHOOK_BASE:
            return f"{CF_WEBHOOK_BASE}/webhook/{user_id}"
        return f"{self.base}/webhook/{user_id}"

    async def set_webhook(self, user_id: int, bot_token: str, secret_token: str = None) -> bool:
        webhook_url = self.get_webhook_url(user_id)
        payload = {
            "url": webhook_url,
            "allowed_updates": ["message", "callback_query", "inline_query"]
        }
        if secret_token:
            payload["secret_token"] = secret_token
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.post(
                    f"https://api.telegram.org/bot{bot_token}/setWebhook",
                    json=payload
                )
                data = r.json()
                if data.get("ok"):
                    logging.info(f"Webhook set: {webhook_url}")
                    return True
                else:
                    logging.error(f"setWebhook failed: {data}")
                    return False
        except Exception as e:
            logging.error(f"setWebhook error: {e}")
            return False


# === Load Balancing ===

async def select_best_worker() -> dict | None:
    from core.db import get_active_workers
    workers = await get_active_workers()
    if not workers:
        return None
    return min(workers, key=lambda w: w["bots_count"])


async def get_worker_for_user(user_id: int) -> WorkerService | None:
    from core.db import get_active_bot
    bot = await get_active_bot(user_id)
    if bot and bot.get("worker_id"):
        from core.db import get_worker_by_id
        w = await get_worker_by_id(bot["worker_id"])
        if w and w["status"] == "active":
            return WorkerService(w["url"], w["secret"])
    return None


async def health_check_all_workers():
    from core.db import get_all_workers, update_worker_status, update_worker_health
    workers = await get_all_workers()
    for w in workers:
        ws = WorkerService(w["url"], w["secret"])
        result = await ws.health()
        if result.get("status") == "ok":
            if w["status"] == "dead":
                await update_worker_status(w["id"], "active")
            await update_worker_health(w["id"])
        else:
            if w["status"] == "active":
                await update_worker_status(w["id"], "dead")
                logging.warning(f"Worker #{w['id']} is dead: {w['url']}")


async def health_check_loop(interval: int = 60):
    while True:
        try:
            await health_check_all_workers()
        except Exception as e:
            logging.error(f"Health check error: {e}")
        await asyncio.sleep(interval)


# Default worker instance (for backward compatibility)
worker = WorkerService()
