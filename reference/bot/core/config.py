# bot_v2/bot/core/config.py
# This file acts as a centralized and structured gateway to all configuration variables.
# It is now fully self-contained with direct definitions, as per user request.

import os

# --- Environment Strategy ---
# Auto-detect Railway via RAILWAY_PUBLIC_DOMAIN env var
# Falls back to "test" for local development
RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
if RAILWAY_PUBLIC_DOMAIN:
    ENVIRONMENT = "production"
    ABDO_URL = f"https://{RAILWAY_PUBLIC_DOMAIN}"
else:
    ENVIRONMENT = "test"
    ABDO_URL = "https://abdomoh.giize.com/2"

# --- Development Mode ---
# Separate from ENVIRONMENT. Keeps Next.js and FastAPI in development mode.
DEV_MODE = False

if ENVIRONMENT == "production":

    DEV_MODE = False

    # --- Production Environment ---
    API_ID = 26271463
    API_HASH = 'fd104b418f19e5c8e4bc7f3e346640f2'
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '6874716859:AAEWYByXEcYoeSgCJYszfJpxg7t2JosfOms')

    # Ports (4000 series)
    WEBHOOK_PORT = 4000
    WEBAPP_FRONTEND_PORT = 4001
    WEBAPP_BACKEND_PORT = 4002
    INTERNAL_API_PORT = 4003
    MAIN_BOT_INTERNAL_API_PORT = 4004
    WEBAPP_PORT = 4005  # Code Editor
    PHP_HOST_PORT = '4010'
    PHP_ENGINE_FREE_PORT = '4011'
    PHP_ENGINE_PAID_PORT = '4012'

    # Prefix
    PROJECT_PREFIX = "php-bot-prod"
    INSTANCE_SUFFIX = "a"

elif ENVIRONMENT == "test":
    # --- Test Environment ---
    API_ID = 26271463
    API_HASH = 'fd104b418f19e5c8e4bc7f3e346640f2'
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '7589660490:AAHl15up0j2j7rL0lhMbARzHK2Oc7uUVyX4')

    # Ports (4100 series - to avoid conflicts with production)
    WEBHOOK_PORT = 4100
    WEBAPP_FRONTEND_PORT = 4101
    WEBAPP_BACKEND_PORT = 4102
    INTERNAL_API_PORT = 4103
    MAIN_BOT_INTERNAL_API_PORT = 4104
    WEBAPP_PORT = 4105  # Code Editor
    PHP_HOST_PORT = '4110'
    PHP_ENGINE_FREE_PORT = '4111'
    PHP_ENGINE_PAID_PORT = '4112'

    # Prefix
    PROJECT_PREFIX = "php-bot-test"
    INSTANCE_SUFFIX = "b"

# --- Common Config Settings ---
WEBAPP_FRONTEND_HOST = "0.0.0.0"
WEBAPP_BACKEND_HOST = "0.0.0.0"
INTERNAL_API_HOST = '127.0.0.1'
WEBAPP_HOST = "0.0.0.0"
WEBHOOK_HOST = '0.0.0.0'

ADMIN_ID = int(os.environ.get('ADMIN_ID', '6969088145'))
SUDO_USERS = [ADMIN_ID, 1209659601, 6740515648, 6508129575]
WEBHOOK_BASE_URL = ABDO_URL
EDITOR_BASE_URL = ABDO_URL
INTERNAL_SECRET = 'change_this_internal_secret'

# --- Web App URLs (Dynamically linked to ports) ---
if ENVIRONMENT == "production":
    WEBAPP_URL = f"{ABDO_URL}/web-app-host" if ABDO_URL else f"http://localhost:{WEBAPP_FRONTEND_PORT}"
else:
    # Test WebApp URL (has /2/ prefix)
    WEBAPP_URL = f"{ABDO_URL}/web-app-host" if ABDO_URL else f"http://localhost:{WEBAPP_FRONTEND_PORT}"

WEBAPP_DEV_URL = f"http://localhost:{WEBAPP_FRONTEND_PORT}" if DEV_MODE else WEBAPP_URL

# --- AI Service Keys ---
GEMINI_API_KEYS = [
    "AIzaSyAAtLe_QT07S_Rv63Pz4kBpFHiy9o3MDpo",
    "AIzaSyCdeLcamviyhbbQmHmJdSQ-cfA86rVH-VQ",
    "AIzaSyAZF_vbrWuIBlaLWZcgF-0MKYEH1pL6nJo",
    "AIzaSyDdDb2w4ar1w03jzZz9zVeUvAtHbcKb-4I",
    "AIzaSyBjkjXzkDWaWo9KxXUPzcMi9iYj2sSCSjA",
    "AIzaSyD5rwlIL1r58qfcnyycPxDSxpAb-lggCBE",
]
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

# --- Webhook Dispatcher Settings ---
MAX_PAYLOAD_BYTES = 1024 * 1024  # 1 MB
REQUEST_TIMEOUT = 6  # seconds

# --- AI Limits ---
DEFAULT_AI_FREE_LIMIT = 2  # Default daily limit for free users using system keys

# --- Marketplace Version ---
MARKETPLACE_VERSION = "v1.1"

# Internal endpoint for developer API
INTERNAL_DEV_API_ENDPOINT = f"http://api.host:{INTERNAL_API_PORT}/api/request_action"

# --- Path Configuration (IMPORTANT) ---
# Define paths relative to the project root to ensure consistency across different execution points.
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CONFIG_DIR, '..', '..'))
UPLOAD_DIR = os.path.join(PROJECT_ROOT, 'user_bots')

# --- Database and Storage Paths (للويب أب) ---
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

# Use separate database for test mode to avoid locks with main bot
if ENVIRONMENT == "production":
    DB_PATH = os.path.join(DATA_DIR, 'main_bot.db')
else:
    DB_PATH = os.path.join(DATA_DIR, 'main_bot_test.db')

USER_BOTS_DIR = os.path.join(PROJECT_ROOT, 'user_bots')
MARKETPLACE_DIR = os.path.join(PROJECT_ROOT, 'marketplace')
ALL_USERS_JSON = os.path.join(DATA_DIR, 'all_users.json')
BOTS_JSON = os.path.join(DATA_DIR, 'bots.json')


# You can also define new, structured configuration classes here if needed.
# For example:
class TelegramConfig:
    """Holds all Telegram-related credentials."""
    def __init__(self, api_id, api_hash, bot_token, sudo_users):
        self.API_ID = api_id
        self.API_HASH = api_hash
        self.BOT_TOKEN = bot_token
        self.SUDO_USERS = sudo_users

class WebConfig:
    """Holds configurations for all web services."""
    def __init__(self, abdo_url, webhook_base_url, editor_base_url, webhook_port, webapp_port, internal_api_port, main_bot_internal_port, webhook_host, webapp_host, internal_api_host, webapp_frontend_port, webapp_backend_port, webapp_url, webapp_dev_url):
        self.BASE_URL = abdo_url
        self.WEBHOOK_BASE_URL = webhook_base_url
        self.EDITOR_BASE_URL = editor_base_url
        self.WEBHOOK_PORT = webhook_port
        self.WEBHOOK_HOST = webhook_host
        self.WEBAPP_PORT = webapp_port
        self.WEBAPP_HOST = webapp_host
        self.INTERNAL_API_PORT = internal_api_port
        self.INTERNAL_API_HOST = internal_api_host
        self.MAIN_BOT_INTERNAL_API_PORT = main_bot_internal_port
        self.WEBAPP_FRONTEND_PORT = webapp_frontend_port
        self.WEBAPP_BACKEND_PORT = webapp_backend_port
        self.WEBAPP_URL = webapp_url
        self.WEBAPP_DEV_URL = webapp_dev_url
        # Production Domain
        self.DOMAIN = os.environ.get("DOMAIN", "abdomoh.giize.com")
        self.WEBAPP_BACKEND_HOST = os.environ.get("WEBAPP_BACKEND_HOST", "0.0.0.0")


class PhpEngineConfig:
    """Holds configurations for the local PHP engine (Caddy + PHP-FPM). Replaces DockerConfig."""
    def __init__(self, caddy_port=None):
        # Single Caddy port -- uses Railway $PORT or falls back to config value
        self.CADDY_PORT = int(caddy_port or os.environ.get("PHP_ENGINE_PORT", os.environ.get("PORT", "8000")))
        self.CADDY_BASE_URL = f"http://127.0.0.1:{self.CADDY_PORT}"
        # Backward compatibility aliases (so existing code referencing docker config doesn't break)
        self.PHP_ENGINE_FREE_PORT = str(self.CADDY_PORT)
        self.PHP_ENGINE_PAID_PORT = str(self.CADDY_PORT)

# Create instances of the structured config classes
# This makes accessing settings more organized, e.g., `settings.telegram.API_ID`
telegram_settings = TelegramConfig(API_ID, API_HASH, BOT_TOKEN, SUDO_USERS)
web_settings = WebConfig(ABDO_URL, WEBHOOK_BASE_URL, EDITOR_BASE_URL, WEBHOOK_PORT, WEBAPP_PORT, INTERNAL_API_PORT, MAIN_BOT_INTERNAL_API_PORT, WEBHOOK_HOST, WEBAPP_HOST, INTERNAL_API_HOST, WEBAPP_FRONTEND_PORT, WEBAPP_BACKEND_PORT, WEBAPP_URL, WEBAPP_DEV_URL)
php_engine_settings = PhpEngineConfig()

# For direct access, you can also create a single settings object
class Settings:
    def __init__(self):
        self.telegram = telegram_settings
        self.web = web_settings
        self.php_engine = php_engine_settings
        # Backward compatibility alias
        self.docker = php_engine_settings
        self.DEV_MODE = DEV_MODE

        # Railway: everything runs on localhost (no Docker gateway needed)
        self.web.INTERNAL_API_HOST = '127.0.0.1'
        
        # Keep direct access for AI keys and other miscellaneous settings
        self.GEMINI_API_KEYS = GEMINI_API_KEYS
        self.GROQ_API_KEY = GROQ_API_KEY
        self.INTERNAL_SECRET = INTERNAL_SECRET
        self.DEFAULT_AI_FREE_LIMIT = DEFAULT_AI_FREE_LIMIT
        self.MAX_PAYLOAD_BYTES = MAX_PAYLOAD_BYTES
        self.REQUEST_TIMEOUT = REQUEST_TIMEOUT
        self.INTERNAL_DEV_API_ENDPOINT = INTERNAL_DEV_API_ENDPOINT
        self.UPLOAD_DIR = UPLOAD_DIR
        self.PROJECT_ROOT = PROJECT_ROOT
        self.MARKETPLACE_VERSION = MARKETPLACE_VERSION
        
        # Database and Storage Paths (للويب أب)
        self.DATA_DIR = DATA_DIR
        self.DB_PATH = DB_PATH
        self.USER_BOTS_DIR = USER_BOTS_DIR
        self.MARKETPLACE_DIR = MARKETPLACE_DIR
        self.ALL_USERS_JSON = ALL_USERS_JSON
        self.BOTS_JSON = BOTS_JSON

# The single, global instance of settings that the rest of the app will import and use.
settings = Settings()

print(f"✅ Core settings module initialized. Caddy Port: {settings.php_engine.CADDY_PORT}")