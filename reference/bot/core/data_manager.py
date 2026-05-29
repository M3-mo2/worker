# bot_v2/bot/core/data_manager.py
# Centralized module for loading and saving JSON data files.
# All JSON files are now expected to reside in the 'bot_v2/data/' directory.

import json
import os
import threading
from typing import Any, Dict

# --- Configuration for Data Directory ---
DATA_MANAGER_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(DATA_MANAGER_DIR, '..', '..'))
from bot.core.config import settings

# --- Configuration for Data Directory (FIXED PATH) ---
# استرجاع المسار الأصلي
DATA_DIR = os.path.join(settings.PROJECT_ROOT, 'data')

os.makedirs(DATA_DIR, exist_ok=True) # Ensure data directory exists

# --- File Paths ---
BOTS_FILE = os.path.join(DATA_DIR, 'bots.json')
print(f"📂 [DataManager] BOTS_FILE path: {os.path.abspath(BOTS_FILE)}")
ALL_USERS_FILE = os.path.join(DATA_DIR, 'all_users.json')
STATS_FILE = os.path.join(DATA_DIR, 'stats.json')
ADMIN_SETTINGS_FILE = os.path.join(DATA_DIR, 'admin_settings.json')
HOST_SETTINGS_FILE = os.path.join(DATA_DIR, 'host_settings.json')
ADMIN_LIST_FILE = os.path.join(DATA_DIR, 'admins.json')
BANNED_LIST_FILE = os.path.join(DATA_DIR, 'banned_users.json')
GIVEAWAYS_FILE = os.path.join(DATA_DIR, 'giveaways.json')
SITE_SETTINGS_FILE = os.path.join(DATA_DIR, 'site_settings.json')

# --- Locks for Thread-Safe Operations (especially for stats.json) ---
# In the original main.py, stats_lock was defined globally.
# We'll re-implement it here for thread-safe access to stats.json.
stats_lock = threading.Lock()

# --- Generic JSON File Handlers ---
def load_json_file(file_path: str, default_data: Any = {}) -> Any:
    """
    Generic function to load a JSON file.
    If the file does not exist or is invalid JSON, returns default_data.
    """
    if not os.path.exists(file_path):
        save_json_file(file_path, default_data) # Create with default if not exists
        return default_data
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {file_path} is corrupted or empty. Returning default data.")
        save_json_file(file_path, default_data) # Overwrite corrupted file
        return default_data
    except Exception as e:
        print(f"Error loading {file_path}: {e}. Returning default data.")
        return default_data

def save_json_file(file_path: str, data: Any):
    """
    Generic function to save data to a JSON file.
    Atomically saves to prevent data corruption during writes.
    """
    temp_path = f"{file_path}.tmp"
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno()) # Ensure data is written to disk
        os.replace(temp_path, file_path) # Atomic replacement
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        # Clean up temp file if something went wrong
        if os.path.exists(temp_path):
            os.remove(temp_path)

# --- Specific Data Loaders/Savers ---

def load_bots_data() -> Dict:
    """Loads the bots data from the JSON file."""
    return load_json_file(BOTS_FILE, {})

def save_bots_data(data: Dict):
    """Saves the bots data to the JSON file."""
    save_json_file(BOTS_FILE, data)

def load_all_users() -> Dict:
    """Loads all user data."""
    return load_json_file(ALL_USERS_FILE, {})

def save_all_users(data: Dict):
    """Saves all user data."""
    save_json_file(ALL_USERS_FILE, data)

def load_stats() -> Dict:
    """Loads the statistics data from the JSON file. Returns dict with keys 'global' and 'users'."""
    return load_json_file(STATS_FILE, {"global": {}, "users": {}, "events": []}) # Ensure events list is initialized

def save_stats(data: Dict):
    """Atomically save stats to avoid corruption (write to temp then replace)."""
    save_json_file(STATS_FILE, data)

def load_admin_settings() -> Dict:
    """Loads admin settings."""
    return load_json_file(ADMIN_SETTINGS_FILE, {"message_forwarding": True, "bot_status": True, "ai_free_enabled": True, "ai_free_fallback_limit": 5, "ai_agent_free_limit": 5, "ai_pro_daily_limit": 5})

def save_admin_settings(data: Dict):
    """Saves admin settings."""
    save_json_file(ADMIN_SETTINGS_FILE, data)

def load_host_settings() -> Dict:
    """Loads host settings and ensures defaults are present."""
    default_settings = {
        "max_folders": 5, 
        "max_php_files": 10, 
        "allow_php": True, 
        "allow_json": True, 
        "allow_txt": True,
        "bot_mode": "paid",
        "tiers": {
            "free": {
                "max_storage_mb": 50,
                "max_files": 30,
                "max_folders": 5,
                "max_zip_files": 50
            },
            "pro": {
                "max_storage_mb": 1000,
                "max_files": 500,
                "max_folders": 50,
                "max_zip_files": 1000
            }
        }
    }
    data = load_json_file(HOST_SETTINGS_FILE, default_settings)
    
    def recursive_merge(target, source):
        """Recursively merge source dict into target dict."""
        is_updated = False
        for key, value in source.items():
            if key not in target:
                target[key] = value
                is_updated = True
            elif isinstance(value, dict) and isinstance(target.get(key), dict):
                if recursive_merge(target[key], value):
                    is_updated = True
        return is_updated

    if recursive_merge(data, default_settings):
        save_host_settings(data)
        
    return data

def save_host_settings(data: Dict):
    """Saves host settings."""
    save_json_file(HOST_SETTINGS_FILE, data)

def load_admin_list() -> Dict:
    """Loads admin list."""
    return load_json_file(ADMIN_LIST_FILE, {})

def save_admin_list(data: Dict):
    """Saves admin list."""
    save_json_file(ADMIN_LIST_FILE, data)

def load_banned_list() -> Dict:
    """Loads banned users list."""
    return load_json_file(BANNED_LIST_FILE, {})

def save_banned_list(data: Dict):
    """Saves banned users list."""
    save_json_file(BANNED_LIST_FILE, data)

def load_giveaways() -> Dict:
    """Loads giveaways data."""
    return load_json_file(GIVEAWAYS_FILE, {})

def save_giveaways(data: Dict):
    """Saves giveaways data."""
    save_json_file(GIVEAWAYS_FILE, data)

def load_site_settings() -> Dict:
    """Loads site settings with defaults and recursive merge."""
    default_settings = {
        "site_name": "AI Agent",
        "site_description": "بوابة الذكاء الاصطناعي المتكاملة",
        "site_status": "active",
        "bot_avatar": "https://cdn-icons-png.flaticon.com/512/4712/4712035.png",
        "contact_telegram": "https://t.me/your_telegram",
        "contact_youtube": "https://youtube.com/@channel",
        "contact_github": "https://github.com/username",
        "developer_name": "المطور الرئيسي",
        "developer_title": "AI SOLUTIONS ARCHITECT",
        "developer_image": "https://via.placeholder.com/200",
        "tutorials": [
            {
                "id": 1,
                "title": "شرح إعداد البوت",
                "description": "فيديو توضيحي لكيفية البدء واستخدام لوحة التحكم.",
                "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "view_count": 0
            }
        ]
    }
    data = load_json_file(SITE_SETTINGS_FILE, default_settings)
    
    def recursive_merge(target, source):
        is_updated = False
        for key, value in source.items():
            if key not in target:
                target[key] = value
                is_updated = True
            elif isinstance(value, dict) and isinstance(target.get(key), dict):
                if recursive_merge(target[key], value):
                    is_updated = True
        return is_updated

    if recursive_merge(data, default_settings):
        save_site_settings(data)
        
    return data

def save_site_settings(data: Dict):
    """Saves site settings."""
    save_json_file(SITE_SETTINGS_FILE, data)

print(f"✅ DataManager initialized. Data files expected in: {DATA_DIR}")
