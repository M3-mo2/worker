# bot_v2/bot/utils/dev_logger.py
import logging
import os
import json
import inspect
from datetime import datetime

# --- Developer Mode Configuration ---
# اجعل هذا True لتفعيل السجلات التفصيلية لكل خطوة في البوت
DEV_MODE = False

def log_step(action: str, message: str, details: dict = None):
    """
    Logs a detailed step in the bot's execution flow if DEV_MODE is True.
    Prints to console with timestamp, caller info, and data dump.
    """
    if not DEV_MODE:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Attempt to get caller information (File, Function, Line)
    try:
        frame = inspect.stack()[1]
        filename = os.path.basename(frame.filename)
        func_name = frame.function
        lineno = frame.lineno
        caller_info = f"{filename}:{lineno} >> {func_name}()"
    except Exception:
        caller_info = "Unknown Caller"

    log_entry = (
        f"\n[DEV_SYS] ⏰ {timestamp} | 📍 {action}\n"
        f"📂 Source: {caller_info}\n"
        f"📝 Message: {message}\n"
    )

    if details:
        try:
            details_str = json.dumps(details, default=str, indent=4, ensure_ascii=False)
            log_entry += f"📊 Data Dump:\n{details_str}\n"
        except Exception:
            log_entry += f"📊 Data Dump (Raw): {str(details)}\n"
    
    log_entry += "_" * 60
    print(log_entry)