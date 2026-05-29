import time
from pathlib import Path
from threading import Thread
from core.config import config


class FileCleaner:
    def __init__(self):
        self.download_dir = config.DOWNLOAD_DIR
        self.temp_dir = config.TEMP_DIR
        self.cleanup_interval = config.CLEANUP_INTERVAL
        self.running = False
        
    def start(self):
        self.running = True
        thread = Thread(target=self._cleanup_loop, daemon=True)
        thread.start()
        
    def stop(self):
        self.running = False
        
    def _cleanup_loop(self):
        while self.running:
            self._cleanup_old_files()
            time.sleep(self.cleanup_interval)
            
    def _cleanup_old_files(self):
        current_time = time.time()
        max_age = 3600
        
        for directory in [self.download_dir, self.temp_dir]:
            for file_path in directory.glob("*"):
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > max_age:
                        try:
                            file_path.unlink()
                        except Exception:
                            pass


cleaner = FileCleaner()
