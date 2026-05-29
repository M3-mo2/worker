# bot_v2/bot/tasks/expiry_checker.py
# Contains the background task for periodically checking and managing subscription expiries.

import asyncio
import time
from datetime import datetime, timedelta
import traceback
from typing import Dict, Any, Tuple

from telethon.errors.rpcerrorlist import UserIsBlockedError, PeerIdInvalidError

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_all_users, save_all_users
from bot.services.billing_service import check_subscription_expiry
from bot.utils.time import _now_ts, _TZ # Using time utilities


# --- Temporary Placeholders for now. These will be properly imported from other modules later ---




# --- Functions ---

async def periodic_expiry_check(interval_seconds: int = 6 * 3600): # 6 hours
    """
    Runs in the background, checking all users for expired subscriptions periodically.
    Also sends a warning 6 hours before expiry.
    """
    print(f"[ExpiryCheck] ⏰ الفاحص الدوري للاشتراكات سيبدأ... الفاصل الزمني: {interval_seconds} ثانية")
    
    six_hours_in_seconds = interval_seconds # Using the interval for warning as well
    
    while True:
        await asyncio.sleep(interval_seconds)
        print("[ExpiryCheck] 🏃‍♂️ جاري بدء الفحص الدوري لجميع المستخدمين...")
        
        try:
            all_users = load_all_users()
            if not all_users:
                print("[ExpiryCheck] ℹ️ لا يوجد مستخدمون للفحص.")
                continue

            users_to_check = list(all_users.items()) 
            demoted_count = 0
            warning_count = 0
            users_file_updated = False
            now = _now_ts()

            for user_id_str, user_data in users_to_check:
                
                # 1. Check for expiry (demotion)
                was_demoted, updated_data = check_subscription_expiry(user_id_str, user_data, current_time=now)
                
                if was_demoted:
                    all_users[user_id_str] = updated_data
                    demoted_count += 1
                    users_file_updated = True
                    continue

                # 2. Check for upcoming expiry (send warning)
                if user_data.get('plan') == 'pro':
                    expiry_ts = user_data.get('plan_expiry')
                    if not expiry_ts:
                        continue # PRO user without expiry date (permanent)

                    warning_sent = user_data.get('expiry_warning_sent', False)
                    
                    if not warning_sent and (expiry_ts > now) and (expiry_ts <= (now + six_hours_in_seconds)):
                        try:
                            user_id_int = int(user_id_str)
                            
                            remaining_seconds = expiry_ts - now
                            remaining_hours = max(1, round(remaining_seconds / 3600))
                            
                            warning_message = (
                                "🔔 **تنبيه قرب انتهاء الاشتراك!**\n\n"
                                f"اشتراكك (PRO) سينتهي خلال **{remaining_hours} ساعات** تقريباً.\n\n"
                                "يرجى التواصل مع المطور لتجديد اشتراكك لضمان استمرار الخدمة."
                            )
                            
                            await client.send_message(user_id_int, warning_message, parse_mode='md')
                            
                            all_users[user_id_str]['expiry_warning_sent'] = True
                            users_file_updated = True
                            warning_count += 1
                            print(f"[ExpiryCheck] 🔔 تم إرسال تحذير للمستخدم {user_id_str}")
                            
                        except UserIsBlockedError:
                            print(f"[ExpiryCheck] 🚫 المستخدم {user_id_str} حظر البوت. لا يمكن إرسال تحذير.")
                        except PeerIdInvalidError:
                            print(f"[ExpiryCheck] 🤷‍♂️ لم يتم العثور على المستخدم {user_id_str}. (PeerIdInvalid)")
                        except Exception as e:
                            print(f"[ExpiryCheck] ❌ فشل إرسال التحذير للمستخدم {user_id_str}: {e}")

            if users_file_updated:
                print(f"[ExpiryCheck] 💾 تم تحديث ملف all_users.json (تحذيرات: {warning_count}, تخفيض رتبة: {demoted_count})")
                save_all_users(all_users)
            else:
                print("[ExpiryCheck] ✅ لم تنتهِ صلاحية أي اشتراكات أو تتطلب تحذيراً هذه المرة.")
                
        except Exception as e:
            print(f"[ExpiryCheck] ❌❌ خطأ فادح أثناء الفحص الدوري: {e}")
            print(traceback.format_exc()) 
            
        print(f"[ExpiryCheck] 😴 اكتمل الفحص. سأنتظر {interval_seconds} ثانية أخرى...")

print("✅ Expiry Checker task module initialized.")
