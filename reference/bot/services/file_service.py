# bot_v2/bot/services/file_service.py
# Centralized service for managing user's file system, paths, and current working directories.

import os
from typing import Dict, Optional

from bot.core.config import settings

# --- File System Management Globals and Helpers ---
# Corresponds to BOTS_DIR in main.py, but now relative to the project root or specified in config
USER_BOTS_ROOT_DIR = os.path.abspath(settings.UPLOAD_DIR) # Use setting from config

# Global dict {user_id: path} for user's current working directory.
# This state is managed centrally by this service.
user_current_working_directory: Dict[int, str] = {} 

def get_user_root(user_id: int) -> str:
    """Returns the root directory for a given user."""
    path = os.path.join(USER_BOTS_ROOT_DIR, str(user_id))
    os.makedirs(path, exist_ok=True)
    return path

def get_current_path(user_id: int) -> str:
    """Gets the user's current working directory, defaulting to their root."""
    return user_current_working_directory.get(user_id, get_user_root(user_id))

def set_current_path(user_id: int, path: str) -> Optional[str]:
    """Sets the user's current working directory, ensuring it's within their root.
    Returns the new path if successful, None otherwise.
    """
    root = get_user_root(user_id)
    # Handle '..' for navigating up
    if path == "..":
        new_path = os.path.abspath(os.path.join(get_current_path(user_id), path))
    else:
        new_path = os.path.abspath(os.path.join(get_current_path(user_id), path))
    
    # Security check: ensure new_path is within the user's root
    if os.path.commonpath([root, new_path]) == root and os.path.isdir(new_path):
        user_current_working_directory[user_id] = new_path
        return new_path
    return None # Return None if path is invalid or outside root

print("✅ File Service initialized.")
