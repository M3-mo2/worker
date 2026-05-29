def format_duration(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_views(views: int) -> str:
    if views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M"
    elif views >= 1_000:
        return f"{views / 1_000:.1f}K"
    return str(views)


def format_file_size(size_bytes: int) -> str:
    size_mb = size_bytes / (1024 * 1024)
    if size_mb >= 1024:
        return f"{size_mb / 1024:.2f} GB"
    return f"{size_mb:.2f} MB"


def truncate_text(text: str, max_length: int = 50) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
