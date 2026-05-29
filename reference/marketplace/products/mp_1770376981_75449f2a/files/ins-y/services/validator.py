import re
from typing import Tuple, Optional


class URLValidator:
    VIDEO_PATTERN = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    PLAYLIST_PATTERN = r'youtube\.com\/playlist\?list=([a-zA-Z0-9_-]+)'
    
    @classmethod
    def validate(cls, url: str) -> Tuple[bool, Optional[str]]:
        if cls.is_playlist(url):
            return True, "playlist"
        elif cls.is_video(url):
            return True, "video"
        return False, None
    
    @classmethod
    def is_video(cls, url: str) -> bool:
        return bool(re.search(cls.VIDEO_PATTERN, url))
    
    @classmethod
    def is_playlist(cls, url: str) -> bool:
        return bool(re.search(cls.PLAYLIST_PATTERN, url))
    
    @classmethod
    def extract_video_id(cls, url: str) -> Optional[str]:
        match = re.search(cls.VIDEO_PATTERN, url)
        return match.group(1) if match else None
    
    @classmethod
    def extract_playlist_id(cls, url: str) -> Optional[str]:
        match = re.search(cls.PLAYLIST_PATTERN, url)
        return match.group(1) if match else None


validator = URLValidator()
