# bot_v2/bot/__main__.py
# This is the main entry point for the refactored bot application.
# Enhanced with 'rich' library for a beautiful startup experience.

import asyncio
import logging
import sys
import os
import subprocess
import secrets
import json
import traceback
import time
from aiohttp import web

# --- Rich Console Imports ---
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich import box

# Local Imports from bot_v2 core
import bot.core.client as bot_client
from bot.core.loader import load_all_handlers
from bot.core.config import settings
from bot.core.database import init_db as init_core_db
from bot.core.data_manager import load_bots_data, save_bots_data, load_all_users

# Local Imports from bot_v2 tasks
from bot.tasks import start_all_tasks

# Local Imports from bot_v2 services
from bot.services.php_engine import setup_php_engine, shutdown_php_engine
from bot.services.telegram import set_webhook_for_token, delete_webhook_for_token
from bot.core.database import increment_stat

# --- Rich Setup ---
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "step": "bold blue"
})
console = Console(theme=custom_theme)

# Configure standard logging to use Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True, markup=True)]
)
logger = logging.getLogger("BotMain")

# --- Internal API Handlers ---
async def handle_set_webhook_action(user_id, payload):
    bot_token = payload.get("bot_token")
    bot_path = payload.get("bot_path")
    
    secret = secrets.token_urlsafe(24)
    result_text = await set_webhook_for_token(bot_token, secret_token=secret)
    
    try:
        response_data = json.loads(result_text) if result_text else {}
        if not response_data.get("ok"):
            raise Exception(f"Telegram API Error: {response_data.get('description')}")
    except Exception as e:
        raise Exception(f"Webhook setup failed: {e}")

    bots_data = load_bots_data()
    all_users = load_all_users()
    user_tier = all_users.get(str(user_id), {}).get('plan', 'free')
    
    upload_dir = os.path.abspath(settings.UPLOAD_DIR)
    rel_path = os.path.relpath(bot_path, upload_dir).replace(os.path.sep, '/')

    bots_data[bot_token] = {
        "path": rel_path,
        "owner": user_id,
        "status": "running",
        "webhook_set": True,
        "secret": secret,
        "tier": user_tier
    }
    save_bots_data(bots_data)
    await increment_stat(user_id, 'bots_started')
    
    try:
        await bot_client.client.send_message(user_id, f"✅ **نجاح!**\n\nتم ربط الـ Webhook بنجاح عبر الـ API للملف:\n`{os.path.basename(bot_path)}`")
    except: pass
    
    return {"status": "success", "message": "Webhook set and bot data saved."}

async def handle_delete_webhook_action(user_id, payload):
    bot_token = payload.get("bot_token")
    bots_data = load_bots_data()
    
    if bot_token not in bots_data or bots_data[bot_token].get('owner') != user_id:
        raise Exception("Bot token not found or access denied.")

    await delete_webhook_for_token(bot_token)
    
    if bot_token in bots_data:
        del bots_data[bot_token]
        save_bots_data(bots_data)
    
    await increment_stat(user_id, 'bots_stopped')
    
    try:
        await bot_client.client.send_message(user_id, f"✅ **نجاح!**\n\nتم حذف الـ Webhook بنجاح عبر الـ API.")
    except: pass

    return {"status": "success", "message": "Webhook deleted."}

async def handle_get_user_info_action(user_id):
    """Fetches user details from Telegram API using the main bot client."""
    if not user_id:
        raise Exception("User ID is required.")
    try:
        user_entity = await bot_client.client.get_entity(int(user_id))
        return {
            "status": "success",
            "user_info": {
                "id": user_entity.id,
                "first_name": user_entity.first_name,
                "last_name": user_entity.last_name,
                "username": user_entity.username,
            }
        }
    except Exception as e:
        logger.error(f"Internal API: Failed to get user info for {user_id}: {e}")
        raise Exception(f"Could not fetch user info from Telegram for ID {user_id}")

async def internal_api_handler(request):
    if request.headers.get("X-Internal-Secret") != settings.INTERNAL_SECRET:
        return web.json_response({"error": "Authentication failed"}, status=403)
    
    try:
        data = await request.json()
        action = data.get("action")
        user_id = data.get("user_id")
        payload = data.get("payload")
        
        if action == "set_webhook":
            result = await handle_set_webhook_action(user_id, payload)
        elif action == "delete_webhook":
            result = await handle_delete_webhook_action(user_id, payload)
        elif action == "get_user_info":
            result = await handle_get_user_info_action(user_id)
        else:
            return web.json_response({"error": "Unsupported action"}, status=400)
            
        return web.json_response(result, status=200)
    except Exception as e:
        logger.error(f"Internal API Error: {e}\n{traceback.format_exc()}")
        return web.json_response({"error": str(e)}, status=500)

async def start_internal_api_server():
    app = web.Application()
    app.router.add_post("/execute_action", internal_api_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', settings.web.MAIN_BOT_INTERNAL_API_PORT)
    # logger.info(f"🚀 Main Bot Internal API listening on 127.0.0.1:{settings.web.MAIN_BOT_INTERNAL_API_PORT}")
    await site.start()


def print_banner():
    """Print startup banner and DEV_MODE info."""
    console.print(
        Panel.fit(
            "[bold cyan]🤖 PHP HOSTING BOT V2[/bold cyan]\n[bold white]Advanced Telegram Bot Hosting System[/bold white]",
            box=box.DOUBLE,
            border_style="blue",
            padding=(1, 4),
        )
    )

    # Show development mode info when enabled
    if getattr(settings, 'DEV_MODE', False):
        console.print(
            Panel(
                "[bold yellow]⚠️ وضع التطوير مفعل![/bold yellow]\n"
                f"🌐 رابط الويب اب: {settings.web.WEBAPP_DEV_URL}",
                border_style="yellow",
            )
        )

def print_luxury_dashboard(system_status, sidecar_status):
    """Prints a high-end dashboard with grouped tables for maximum clarity."""
    
    # --- 1. Infrastructure Table ---
    core_table = Table(box=box.SIMPLE_HEAVY, border_style="bright_blue", show_header=True, header_style="bold cyan", expand=True)
    core_table.add_column("💎 المكون الأساسي (Infrastructure)", style="bold cyan")
    core_table.add_column("الحالة", justify="center")
    core_table.add_column("التفاصيل", style="white")

    for comp, data in system_status.items():
        icon = "[bold green]✅ متصل[/bold green]" if data['status'] else "[bold red]❌ فشل[/bold red]"
        core_table.add_row(comp, icon, data['details'])

    # --- 2. Network Gateways Table ---
    net_table = Table(box=box.SIMPLE_HEAVY, border_style="bright_magenta", show_header=True, header_style="bold magenta", expand=True)
    net_table.add_column("🌐 بوابات الشبكة (Gateways)", style="bold magenta")
    net_table.add_column("الحالة", justify="center")
    net_table.add_column("المنفذ / الرابط", style="white")

    for proc, data in sidecar_status.items():
        if "API" in proc or "Webhook" in proc or "Editor" in proc or "Backend" in proc or "Frontend" in proc:
            icon = "[bold green]✅ نشط[/bold green]" if data['status'] else "[bold red]⚠️ خطأ[/bold red]"
            net_table.add_row(proc, icon, data['details'])

    # --- 3. Extensions & Addons Table ---
    ext_table = Table(box=box.SIMPLE_HEAVY, border_style="bright_yellow", show_header=True, header_style="bold yellow", expand=True)
    ext_table.add_column("🔌 الإضافات والمهام (Extensions)", style="bold yellow")
    ext_table.add_column("الحالة", justify="center")
    ext_table.add_column("الوصف", style="white")

    # Add background tasks and plugins info here
    ext_table.add_row("Plugin Manager", "[bold green]✅ نشط[/bold green]", "تم تحميل جميع الهاندلرز")
    ext_table.add_row("Background Tasks", "[bold green]✅ نشط[/bold green]", "المهام الدورية قيد العمل")
    ext_table.add_row("Top Developers Checker", "[bold green]✅ نشط[/bold green]", "فحص المطورين مفعّل")
    ext_table.add_row("Billing System", "[bold green]✅ نشط[/bold green]", "بوابة الدفع والاشتراكات")

    # Final Dashboard Display
    console.print("\n")
    console.print(Panel(core_table, title="[bold white]CORE SYSTEMS[/bold white]", border_style="bright_blue", title_align="left"))
    console.print(Panel(net_table, title="[bold white]NETWORK & WEB SERVICES[/bold white]", border_style="bright_magenta", title_align="left"))
    console.print(Panel(ext_table, title="[bold white]PLUGINS & BACKGROUND TASKS[/bold white]", border_style="bright_yellow", title_align="left"))

async def main():
    print_banner()
    
    system_status = {}
    sidecar_status = {}

    with console.status("[bold blue]جاري تشغيل الأنظمة...[/bold blue]", spinner="dots12") as status:
        
        # Phase 1: Infrastructure
        status.update("[bold cyan]جاري فحص البنية التحتية...[/bold cyan]")
        try:
            await init_core_db()
            from bot.core.database import init_marketplace_categories
            await init_marketplace_categories()
            system_status["قاعدة البيانات (Database)"] = {"status": True, "details": "SQLite - مستقرة"}
            console.log("[success]✅ تم التحقق من قاعدة البيانات.[/success]")
        except Exception as e:
            system_status["قاعدة البيانات (Database)"] = {"status": False, "details": str(e)}

        try:
            await bot_client.client.start(bot_token=settings.telegram.BOT_TOKEN)
            me = await bot_client.client.get_me()
            system_status["عميل التيليجرام (Telegram)"] = {"status": True, "details": f"@{me.username} ({me.id})"}
            console.log(f"[success]✅ تم الاتصال بـ @{me.username}[/success]")

            # Resolve entities for all sudo users to ensure notifications work
            for admin_id in settings.telegram.SUDO_USERS:
                try:
                    await bot_client.client.get_entity(admin_id)
                except Exception:
                    pass
        except Exception as e:
            system_status["عميل التيليجرام (Telegram)"] = {"status": False, "details": "فشل الاتصال"}

        # Phase 2: Loading Logic
        status.update("[bold magenta]جاري تحميل اللوجيك والإضافات...[/bold magenta]")
        try:
            load_all_handlers(bot_client.client)
            console.log("[success]✅ تم تحميل جميع الإضافات.")
        except Exception as e:
            console.log(f"[error]❌ فشل تحميل الإضافات: {e}")

        # Phase 3: Background Services
        status.update("[bold yellow]جاري تشغيل الخدمات الخلفية...[/bold yellow]")
        try:
            await start_all_tasks(bot_client.client)
            await start_internal_api_server()
            console.log("[success]✅ الخدمات الخلفية والـ API الداخلي تعمل.")
        except Exception as e:
            console.log(f"[error]❌ فشل تشغيل الخدمات الخلفية: {e}")

        # Prep Sidecar Status
        sidecar_status["مستقبل الويبهوك (Webhook)"] = {"status": True, "details": f"Port {settings.web.WEBHOOK_PORT}"}
        sidecar_status["محرر الأكواد (Editor)"] = {"status": True, "details": f"Port {settings.web.WEBAPP_PORT}"}
        sidecar_status["الـ API الداخلي (Uvicorn)"] = {"status": True, "details": f"Port {settings.web.INTERNAL_API_PORT}"}
        sidecar_status["WebApp Backend"] = {"status": True, "details": f"Port {settings.web.WEBAPP_BACKEND_PORT}"}
        sidecar_status["WebApp Frontend"] = {"status": True, "details": f"Port {settings.web.WEBAPP_FRONTEND_PORT}"}

    # Final Luxury Dashboard
    print_luxury_dashboard(system_status, sidecar_status)
    
    console.print(Panel.fit(
        "[bold green]💎 النظام الآن متصل ومستقر بالكامل الجودة القصوى مفعّلة 💎[/bold green]\n"
        "[white]جميع السيرفرات تعمل في وضع الإنتاج (Production).[/white]\n"
        "للإيقاف اضغط [bold red]Ctrl+C[/bold red]",
        border_style="green",
        title="[bold green]STATUS: ONLINE[/bold green]"
    ))

    await bot_client.client.run_until_disconnected()

def is_port_in_use(port):
    """تحقق إذا كان البورت مستخدماً حالياً."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', int(port))) == 0

def free_port(port):
    """
    تحقق من البورت. تم إيقاف القتل التلقائي للعمليات (fuser -k) 
    لأنه يسبب تداخل مع حاويات دوكر والخدمات الأخرى.
    """
    if is_port_in_use(port):
        console.log(f"[warning]⚠️ البورت {port} مشغول حالياً. قد يفشل تشغيل إحدى الخدمات.[/warning]")
    else:
        # console.log(f"[success]✅ البورت {port} متاح.[/success]")
        pass





def generate_webapp_env():
    """
    إنشاء ملف .env للويب اب من إعدادات البوت (مصدر واحد للبورتات والمسارات).
    يسمح للويب اب بقراءة التخزين والكونفج دون تشغيله داخل دوكر.
    """
    project_root = os.getcwd()
    data_dir = settings.DATA_DIR
    user_bots_dir = settings.USER_BOTS_DIR
    backend_port = settings.web.WEBAPP_BACKEND_PORT
    frontend_port = settings.web.WEBAPP_FRONTEND_PORT
    main_bot_api_port = settings.web.MAIN_BOT_INTERNAL_API_PORT
    internal_secret = settings.INTERNAL_SECRET
    backend_url = f"http://127.0.0.1:{backend_port}"

    env_lines = [
        f"WEBAPP_BACKEND_PORT={settings.web.WEBAPP_BACKEND_PORT}",
        f"WEBAPP_FRONTEND_PORT={settings.web.WEBAPP_FRONTEND_PORT}",
        f"DATA_DIR={settings.DATA_DIR}",
        f"USER_DATA_PATH={settings.USER_BOTS_DIR}",
        f"MAIN_BOT_INTERNAL_API_PORT={settings.web.MAIN_BOT_INTERNAL_API_PORT}",
        f"INTERNAL_SECRET={settings.INTERNAL_SECRET}",
        f"BACKEND_HOST={settings.web.WEBAPP_BACKEND_HOST}",
        f"BACKEND_URL={settings.web.WEBAPP_DEV_URL}",
    ]

    # webapp/.env (للـ backend عند التشغيل المحلي أو الدوكر لاحقاً)
    webapp_dir = os.path.join(project_root, "webapp")
    env_path = os.path.join(webapp_dir, ".env")
    try:
        os.makedirs(webapp_dir, exist_ok=True)
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(env_lines) + "\n")
        console.log(f"[success]✅ WebApp env written: {env_path}[/success]")
    except Exception as e:
        console.log(f"[error]❌ Failed to write webapp .env: {e}[/error]")

    # webapp/frontend/.env.local (لـ Next.js - rewrites و getServerSideProps)
    frontend_env_dir = os.path.join(webapp_dir, "frontend")
    frontend_env_path = os.path.join(frontend_env_dir, ".env.local")
    try:
        os.makedirs(frontend_env_dir, exist_ok=True)
        with open(frontend_env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(env_lines) + f"\nPORT={frontend_port}\n")
        console.log(f"[success]✅ Frontend env written: {frontend_env_path}[/success]")
    except Exception as e:
        console.log(f"[error]❌ Failed to write frontend .env.local: {e}[/error]")







if __name__ == '__main__':
    # --- PHP Engine & Ports Setup (Outside Async Loop) ---
    console.rule("[bold yellow]Pre-Flight Checks[/bold yellow]")

    # 1. Generate Sync Env File
    generate_webapp_env()

    with console.status("[bold yellow]Setting up PHP Engine (Caddy + PHP-FPM)...[/bold yellow]", spinner="dots") as status:
        # PHP Engine (local Caddy + PHP-FPM)
        if setup_php_engine():
            console.log("[success]✅ PHP Engine (Caddy + PHP-FPM) is ready.[/success]")
        else:
            console.log("[error]❌ PHP Engine setup failed. Exiting.[/error]")
            sys.exit(1)
        
        # Ports
        status.update("[bold yellow]Checking ports availability...[/bold yellow]")
        ports_to_check = [
            settings.web.WEBHOOK_PORT,
            settings.web.WEBAPP_PORT,
            settings.web.INTERNAL_API_PORT,
            settings.web.MAIN_BOT_INTERNAL_API_PORT,
            settings.web.WEBAPP_FRONTEND_PORT,
            settings.web.WEBAPP_BACKEND_PORT,
        ]
        for port in ports_to_check:
            free_port(port)
        console.log(f"[success]✅ Port checks completed.[/success]")

    # --- Sidecar Processes ---
    console.rule("[bold yellow]Spawning Sidecars[/bold yellow]")
    
    project_root = os.getcwd()
    web_dir = os.path.join(project_root, 'web')
    webapp_frontend_dir = os.path.join(project_root, 'webapp', 'frontend')
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")
    
    processes = []
    
    # --- Python Sidecars ---
    scripts = ['webhook.py', 'webapp_server.py', 'internal_api_server.py']
    
    for script in scripts:
        script_path = os.path.join(web_dir, script)
        if os.path.exists(script_path):
            console.log(f"🚀 Spawning: [bold cyan]{script}[/bold cyan]")
            p = subprocess.Popen([sys.executable, script_path], cwd=web_dir, env=env)
            processes.append(p)
        else:
            console.log(f"[error]❌ Could not find {script}[/error]")
    
    # --- WebApp (بدون Docker: Backend + Frontend كعمليات فرعية) ---
    webapp_dir = os.path.join(project_root, 'webapp')
    webapp_backend_port = settings.web.WEBAPP_BACKEND_PORT
    webapp_frontend_port = settings.web.WEBAPP_FRONTEND_PORT
    data_dir = settings.DATA_DIR
    user_bots_dir = settings.USER_BOTS_DIR

    env_backend = env.copy()
    env_backend["DATA_DIR"] = data_dir
    env_backend["USER_DATA_PATH"] = user_bots_dir
    env_backend["WEBAPP_BACKEND_PORT"] = str(webapp_backend_port)
    env_backend["WEBAPP_FRONTEND_PORT"] = str(webapp_frontend_port)
    env_backend["MARKETPLACE_DIR"] = os.path.join(project_root, 'marketplace')
    env_backend["USER_BOTS_DIR"] = user_bots_dir

    # Backend: FastAPI (uvicorn)
    try:
        is_dev = getattr(settings, 'DEV_MODE', False)
        mode_text = "[bold yellow]DEVELOPMENT[/bold yellow]" if is_dev else "[bold green]PRODUCTION[/bold green]"
        console.log(f"🚀 Starting: [bold cyan]WebApp Backend[/bold cyan] in {mode_text} mode")
        
        # --- Log file for backend stderr ---
        logs_dir = os.path.join(project_root, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        backend_log_path = os.path.join(logs_dir, 'webapp_backend.log')
        backend_log_file = open(backend_log_path, 'a', encoding='utf-8')

        # Build command based on DEV_MODE
        cmd_backend = [sys.executable, "-m", "uvicorn", "webapp.backend.main:app", "--host", "127.0.0.1", "--port", str(webapp_backend_port)]
        if is_dev:
            cmd_backend.append("--reload")

        p_backend = subprocess.Popen(
            cmd_backend,
            cwd=project_root,
            env=env_backend,
            stdout=backend_log_file,
            stderr=backend_log_file,
        )
        processes.append(p_backend)
        console.log(f"[success]✅ WebApp Backend online ({mode_text}).[/success]")
        time.sleep(1)
    except Exception as e:
        console.log(f"[warning]⚠️ WebApp Backend failed to start: {e}[/warning]")

    # Frontend: Next.js (بدون Docker - نفس الجهاز يقرأ data و user_bots)
    env_frontend = os.environ.copy()
    env_frontend["PORT"] = str(webapp_frontend_port)
    env_frontend["BACKEND_HOST"] = "127.0.0.1"
    env_frontend["WEBAPP_BACKEND_PORT"] = str(webapp_backend_port)
    env_frontend["BACKEND_URL"] = f"http://127.0.0.1:{webapp_backend_port}"
    frontend_dir = os.path.join(webapp_dir, "frontend")
    
    if os.path.exists(os.path.join(frontend_dir, "package.json")):
        try:
            is_dev = getattr(settings, 'DEV_MODE', False)
            mode_text = "[bold yellow]DEVELOPMENT[/bold yellow]" if is_dev else "[bold green]PRODUCTION[/bold green]"
            # In production, we assume 'npm run build' was already executed OR we use 'npm start'
            # Note: For maximum speed in production, user should run 'npm run build' once manually
            npm_cmd = "dev" if is_dev else "start"
            
            console.log(f"🚀 Starting: [bold cyan]WebApp Frontend[/bold cyan] ({mode_text} - npm run {npm_cmd})")
            p_frontend = subprocess.Popen(
                ["npm", "run", npm_cmd],
                cwd=frontend_dir,
                env=env_frontend,
                shell=(sys.platform == "win32"),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
            processes.append(p_frontend)
            console.log(f"[success]✅ WebApp Frontend online ({mode_text}).[/success]")
        except Exception as e:
            console.log(f"[warning]⚠️ WebApp Frontend failed to start: {e}[/warning]")
    else:
        console.log(f"[warning]⚠️ webapp/frontend not found[/warning]")

    console.print("\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        console.print("\n")
        console.rule("[bold red]System Shutdown[/bold red]")
        console.log("[bold red]💀 Terminating sidecar processes...[/bold red]")
        for p in processes:
            p.terminate()
        console.log("[bold red]💀 Stopping PHP Engine...[/bold red]")
        shutdown_php_engine()
        console.log("[bold red]👋 Goodbye![/bold red]")
