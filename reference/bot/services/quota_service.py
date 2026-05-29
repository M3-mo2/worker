# bot_v2/bot/services/quota_service.py
import os
from pathlib import Path
from typing import Dict, Any, Tuple
from bot.core.config import settings
from bot.core.data_manager import load_host_settings
from bot.services.user_service import get_user_data

def get_user_usage(user_id: int) -> Dict[str, Any]:
    """
    Calculates the total storage usage for a specific user.
    Returns: { 'total_bytes': int, 'file_count': int, 'folder_count': int }
    """
    user_root = Path(settings.USER_BOTS_DIR) / str(user_id)
    if not user_root.exists():
        return {'total_bytes': 0, 'file_count': 0, 'folder_count': 0}

    total_bytes = 0
    file_count = 0
    folder_count = 0

    for root, dirs, files in os.walk(user_root):
        folder_count += len(dirs)
        file_count += len(files)
        for f in files:
            fp = os.path.join(root, f)
            # skip if it's a symbolic link
            if not os.path.islink(fp):
                total_bytes += os.path.getsize(fp)

    return {
        'total_bytes': total_bytes,
        'file_count': file_count,
        'folder_count': folder_count
    }

def get_quota_limits(user_id: int) -> Dict[str, Any]:
    """
    Retrieves the quota limits for a user based on their tier.
    """
    host_settings = load_host_settings()
    user_data = get_user_data(user_id)
    plan = user_data.get('plan', 'free').lower()

    # Hardcoded default fallbacks for absolute safety
    tier_defaults = {
        'free': {
            'max_storage_mb': 50,
            'max_files': 30,
            'max_folders': 5,
            'max_zip_files': 50
        },
        'pro': {
            'max_storage_mb': 1000,
            'max_files': 500,
            'max_folders': 50,
            'max_zip_files': 1000
        }
    }

    tiers = host_settings.get('tiers', tier_defaults)
    
    # Get the specific tier data (e.g., 'free' or 'pro')
    selected_tier = tiers.get(plan, tiers.get('free', tier_defaults['free']))
    
    # Final Layer of Protection: Merge with hardcoded defaults to ensure no missing keys
    default_for_plan = tier_defaults.get(plan, tier_defaults['free'])
    
    for key, value in default_for_plan.items():
        if key not in selected_tier:
            selected_tier[key] = value
            
    return selected_tier

def can_add_files(user_id: int, new_files_count: int = 0, new_bytes: int = 0, new_folders: int = 0) -> Tuple[bool, str]:
    """
    Checks if adding the specified amount of data/files would exceed the user's quota.
    """
    usage = get_user_usage(user_id)
    limits = get_quota_limits(user_id)

    # Storage Check
    current_mb = usage['total_bytes'] / (1024 * 1024)
    new_mb = new_bytes / (1024 * 1024)
    if current_mb + new_mb > limits['max_storage_mb']:
        return False, f"⚠️ تجاوزت مساحة التخزين المسموحة ({limits['max_storage_mb']} MB)."

    # Files Check
    if usage['file_count'] + new_files_count > limits['max_files']:
        return False, f"⚠️ تجاوزت الحد الأقصى للملفات ({limits['max_files']} ملف)."

    # Folders Check
    if usage['folder_count'] + new_folders > limits['max_folders']:
        return False, f"⚠️ تجاوزت الحد الأقصى للمجلدات ({limits['max_folders']} مجلد)."

    return True, ""
