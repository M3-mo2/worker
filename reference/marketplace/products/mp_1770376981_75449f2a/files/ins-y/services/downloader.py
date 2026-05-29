import asyncio
from pathlib import Path
from typing import Dict, Any
from gold_dl import DownloadService
from core.config import config


class YouTubeDownloader:
    def __init__(self):
        self.download_dir = config.DOWNLOAD_DIR
    
    async def download(
        self,
        url: str,
        quality: str = "360p",
        is_audio: bool = False
    ) -> Dict[str, Any]:
        
        output_template = str(self.download_dir / "%(id)s.%(ext)s")
        
        service = DownloadService(
            url=url,
            path=output_template,
            quality="audio" if is_audio else quality,
            is_audio=is_audio,
            download_thumbnail=None,
            export_metadata=None
        )
        
        file_path = await service.download_async()
        
        if file_path and isinstance(file_path, str):
            return {
                'file_path': file_path,
                'title': '',
                'type': 'video'
            }
        
        return None
    
    def get_file_size_mb(self, file_path: Path) -> float:
        return file_path.stat().st_size / (1024 * 1024)
    
    def cleanup_file(self, file_path: Path):
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception:
            pass


downloader = YouTubeDownloader()
