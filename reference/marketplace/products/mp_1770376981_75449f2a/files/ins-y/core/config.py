# لو مش فاهم متلعبش فالملف دا (:
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 50))
    MAX_PLAYLIST_SIZE = int(os.getenv("MAX_PLAYLIST_SIZE", 20))
    DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", 300))
    CLEANUP_INTERVAL = int(os.getenv("CLEANUP_INTERVAL", 3600))
    
    DOWNLOAD_DIR = BASE_DIR / "downloads"
    TEMP_DIR = BASE_DIR / "temp"
    
    QUALITIES = {
        "360p": "360p",
        "720p": "720p",
        "1080p": "1080p",
        "audio": "audio"
    }
    
    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN not found in environment")
        
        cls.DOWNLOAD_DIR.mkdir(exist_ok=True)
        cls.TEMP_DIR.mkdir(exist_ok=True)
        
        return True

config = Config()
