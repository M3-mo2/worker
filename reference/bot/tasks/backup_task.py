# bot_v2/bot/tasks/backup_task.py
import asyncio
import os
from datetime import datetime
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_admin_settings
from bot.utils.backup import create_backup_zip
from bot.services.telegram import send_message_to_admin

async def daily_backup_task():
    """
    Background task that performs a full source code backup every 24 hours
    if enabled in admin settings.
    """
    print("📦 خدمة النسخ الاحتياطي اليومي جاهزة...")
    
    while True:
        # Wait for 24 hours (86400 seconds)
        # We wait first to avoid immediate backup on restart loop
        await asyncio.sleep(86400) 
        
        try:
            admin_settings = load_admin_settings()
            if admin_settings.get('daily_backup', False):
                print("🔄 بدء عملية النسخ الاحتياطي اليومي التلقائي...")
                
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                root_dir = os.getcwd() # Assuming running from project root
                folder_name = os.path.basename(root_dir)
                zip_filename = f"{folder_name}_daily_backup_{timestamp}.zip"
                zip_path = os.path.join(root_dir, zip_filename)
                
                # Run zip in thread to avoid blocking event loop
                await asyncio.to_thread(create_backup_zip, root_dir, zip_path)
                
                for admin_id in settings.telegram.SUDO_USERS:
                    try:
                        await client.send_file(
                            admin_id,
                            zip_path,
                            caption=f"🔄 **نسخة احتياطية يومية تلقائية**\n🗂 المجلد: `{folder_name}`\n📅 التاريخ: `{timestamp}`",
                            force_document=True
                        )
                    except Exception as e:
                        print(f"Failed to send daily backup to {admin_id}: {e}")
                        # Fallback: send just text notification
                        await send_message_to_admin(admin_id, f"🔄 Daily backup failed to send file to you.")
                
                # Clean up
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                    
        except Exception as e:
            print(f"❌ Daily backup task failed: {e}")
