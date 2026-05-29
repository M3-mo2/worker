"""
bot/core/navigation.py
Centralized navigation manager that persists file paths/data using hashes in SQLite.
This ensures buttons remain valid even after bot restarts.
"""
import sqlite3
import hashlib
import os
import time
from bot.core.config import settings

# Path to the main database
DB_PATH = settings.DB_PATH

class NavigationManager:
    def __init__(self):
        print(f"🔌 NavigationManager initializing. DB: {DB_PATH}")
        self._ensure_table()

    def _get_conn(self):
        # check_same_thread=False allows using the connection across threads if needed,
        # though we create a new one here for safety in the simple wrapper.
        # Increased timeout to 10s to handle potential locks from aiosqlite
        return sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10.0)

    def _ensure_table(self):
        """Ensures the file_hashes table exists."""
        try:
            with self._get_conn() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS file_hashes (
                        hash TEXT PRIMARY KEY,
                        path TEXT NOT NULL,
                        created_at INTEGER
                    )
                """)
                conn.commit()
        except Exception as e:
            print(f"⚠️ Navigation DB Init Error: {e}")

    def get_hash(self, path: str) -> str:
        """
        Generates a persistent hash for a file path/data and saves it to DB.
        """
        if not path: return ""
        
        # Generate a short, consistent hash
        hash_key = hashlib.sha1(path.encode('utf-8')).hexdigest()[:12]
        
        # Save to DB (Insert or Ignore to avoid duplicates)
        try:
            with self._get_conn() as conn:
                conn.execute(
                    "INSERT OR IGNORE INTO file_hashes (hash, path, created_at) VALUES (?, ?, ?)",
                    (hash_key, path, int(time.time()))
                )
                conn.commit()
        except Exception as e:
            print(f"⚠️ Error saving navigation hash: {e}")
            
        return hash_key

    def resolve(self, hash_key: str) -> str:
        """
        Resolves a hash back to the original path/data.
        """
        try:
            with self._get_conn() as conn:
                cursor = conn.execute("SELECT path FROM file_hashes WHERE hash = ?", (hash_key,))
                row = cursor.fetchone()
                if row:
                    return row[0]
        except Exception as e:
            print(f"⚠️ Error resolving navigation hash: {e}")
        
        # Fallback: return the hash itself if resolution fails (legacy behavior)
        return hash_key

# Global Instance
nav = NavigationManager()

# --- Public Helpers ---

def create_nav_button_data(prefix: str, data: str) -> bytes:
    """Creates callback data bytes: 'prefix:hash'."""
    h = nav.get_hash(data)
    return f"{prefix}:{h}".encode()

def resolve_nav_data(data_str: str) -> str:
    """Resolves the hash part of a callback data string."""
    return nav.resolve(data_str)
