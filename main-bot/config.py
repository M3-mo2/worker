import os
import sys
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WORKER_URL = os.getenv("WORKER_URL", "")
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET", "")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
MAX_FILE_SIZE = 10 * 1024 * 1024

CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID", "")
CF_KV_ID = os.getenv("CF_KV_ID", "")
CF_API_TOKEN = os.getenv("CF_API_TOKEN", "")
CF_WEBHOOK_BASE = os.getenv("CF_WEBHOOK_BASE", "")

if not BOT_TOKEN:
    print("❌ BOT_TOKEN مش موجود!")
    print("")
    print("حط المتغيرات كده:")
    print('  export BOT_TOKEN="توكن_البوت"')
    print('  export WORKER_URL="https://worker-url.up.railway.app"')
    print('  export INTERNAL_SECRET="السر_المشترك"')
    print("")
    print("أو أنشئ ملف .env:")
    print('  BOT_TOKEN=توكن_البوت')
    print('  WORKER_URL=https://worker-url.up.railway.app')
    print('  INTERNAL_SECRET=السر_المشترك')
    sys.exit(1)
