# لو حد عايز يعدل فرسايل البوت يعدل من هنا (خدو بالكو من الماركداون)
class Messages:
    WELCOME = """**YouTube Downloader**

Send video or playlist link

Features:
• Multiple quality options
• Audio extraction
• Playlist support"""

    INVALID_URL = "Invalid link"
    PROCESSING = "Processing"
    DOWNLOADING = "Downloading"
    UPLOADING = "Uploading"
    DONE = "Downloaded"
    ERROR = "Failed"
    FILE_TOO_LARGE = "File exceeds {size}MB limit"
    PLAYLIST_TOO_LARGE = "Playlist exceeds {max} videos"
    CANCELLED = "Cancelled"
    
    @staticmethod
    def progress(current, total):
        return f"Downloading {current}/{total}"
    
    @staticmethod
    def video_info(title, duration, views):
        return f"**{title}**\n\n`{duration}` • `{views} views`"

    @staticmethod
    def playlist_info(title, count):
        return f"**{title}**\n\n`{count} videos`"

class Callbacks:
    VIDEO_PREFIX = "vid"
    AUDIO_PREFIX = "aud"
    PLAYLIST_ALL_VIDEO = "pl_all_vid"
    PLAYLIST_ALL_AUDIO = "pl_all_aud"
    PLAYLIST_SELECT = "pl_select"
    CANCEL = "cancel"
    
    @staticmethod
    def video_quality(quality):
        return f"{Callbacks.VIDEO_PREFIX}:{quality}"
    
    @staticmethod
    def audio_quality():
        return f"{Callbacks.AUDIO_PREFIX}:audio"
    
    @staticmethod
    def parse_callback(data):
        parts = data.split(":")
        return parts[0], parts[1] if len(parts) > 1 else None
