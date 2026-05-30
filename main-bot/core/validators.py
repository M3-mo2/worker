from aiogram.types import Document
from config import MAX_FILE_SIZE


def validate_php_file(document: Document) -> str | None:
    if not document.file_name or not document.file_name.endswith(".php"):
        return f"❌ الملف لازم يكون بصيغة `.php`\n\nانت رفعت: `{document.file_name}`"
    if document.file_size and document.file_size > MAX_FILE_SIZE:
        size_mb = round(document.file_size / (1024 * 1024), 1)
        return f"❌ الملف كبير جداً\n\nالحد الأقصى 10MB وحجم الملف `{size_mb}`MB"
    if document.file_size == 0:
        return "❌ الملف فاضي\n\nارفع ملف فيه كود البوت بتاعك."
    return None


def validate_bot_token(token: str) -> str | None:
    token = token.strip()
    if ":" not in token:
        return "❌ التوكن مش صحيح\n\nالتوكن بتاخده من @BotFather لما تعمل بوت جديد أو تكتب `/newbot`"
    parts = token.split(":")
    if len(parts) != 2 or not parts[0].isdigit():
        return "❌ التوكن مش صحيح\n\nالتوكن بتاخده من @BotFather لما تعمل بوت جديد أو تكتب `/newbot`"
    return None
