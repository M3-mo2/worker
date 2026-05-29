# bot/services/marketplace_service.py
# Service layer for marketplace operations - Clean, reusable, and extensible

import os
import json
import time
import shutil
import zipfile
import hashlib
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from bot.core.config import settings
from bot.core import database

# Constants
MARKETPLACE_DIR = os.path.join(settings.PROJECT_ROOT, 'marketplace')
PRODUCTS_DIR = os.path.join(MARKETPLACE_DIR, 'products')
TEMP_DIR = os.path.join(MARKETPLACE_DIR, 'temp')
THUMBNAILS_DIR = os.path.join(MARKETPLACE_DIR, 'thumbnails')

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_TOTAL_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = [
    # Code files
    '.php', '.py', '.js', '.html', '.css', '.sql',
    # Data files
    '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.env',
    # Documentation
    '.txt', '.md', '.rst',
    # Config files (common patterns)
    '.example', '.sample', '.template', '.dist',
    # Archives
    '.zip'
]

# Dangerous PHP functions to check
DANGEROUS_FUNCTIONS = [
    'eval', 'exec', 'system', 'shell_exec', 'passthru', 
    'proc_open', 'popen', 'pcntl_exec', 'assert'
]


def generate_product_id() -> str:
    """Generates a unique product ID."""
    timestamp = int(time.time())
    random_part = hashlib.md5(os.urandom(16)).hexdigest()[:8]
    return f"mp_{timestamp}_{random_part}"


def get_product_dir(product_id: str) -> str:
    """Gets the directory path for a product."""
    return os.path.join(PRODUCTS_DIR, product_id)


def get_product_files_dir(product_id: str) -> str:
    """Gets the files directory for a product."""
    return os.path.join(get_product_dir(product_id), 'files')


def validate_file(file_path: str) -> Tuple[bool, str]:
    """
    Validates a file for security and size.
    Returns (is_valid, error_message)
    """
    # Check extension (handle double extensions like .env.example)
    filename = os.path.basename(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    
    # Check for common config file patterns
    config_patterns = ['.env', '.example', '.sample', '.template', '.dist', '.config']
    is_config_file = any(pattern in filename.lower() for pattern in config_patterns)
    
    # Allow config files and standard extensions
    if not (ext in ALLOWED_EXTENSIONS or is_config_file):
        return False, f"❌ نوع الملف غير مسموح: {ext}"
    
    # Check size
    if not os.path.exists(file_path):
        return False, "❌ الملف غير موجود"
    
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        return False, f"❌ حجم الملف كبير جداً ({file_size / 1024 / 1024:.1f} MB)"
    
    # Check PHP files for dangerous functions
    if ext == '.php':
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for func in DANGEROUS_FUNCTIONS:
                    if func in content:
                        return False, f"⚠️ الملف يحتوي على دالة خطرة: {func}"
        except Exception as e:
            return False, f"❌ فشل فحص الملف: {e}"
    
    return True, ""


def scan_directory(directory: str) -> Tuple[int, int, List[str]]:
    """
    Scans a directory and returns (file_count, total_size, file_list).
    """
    file_count = 0
    total_size = 0
    file_list = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, directory)
            file_list.append(rel_path)
            file_count += 1
            total_size += os.path.getsize(file_path)
    
    return file_count, total_size, file_list


async def create_product(
    owner_id: int,
    title: str,
    description: str,
    category: str,
    tags: List[str] = None,
    files_source: str = None
) -> Tuple[bool, str, Optional[str]]:
    """
    Creates a new marketplace product.
    Returns (success, message, product_id)
    """
    try:
        # Generate product ID
        product_id = generate_product_id()
        product_dir = get_product_dir(product_id)
        files_dir = get_product_files_dir(product_id)
        
        # Create directories
        os.makedirs(files_dir, exist_ok=True)
        
        # Copy files
        if files_source and os.path.exists(files_source):
            if os.path.isdir(files_source):
                shutil.copytree(files_source, files_dir, dirs_exist_ok=True)
            elif zipfile.is_zipfile(files_source):
                with zipfile.ZipFile(files_source, 'r') as zip_ref:
                    zip_ref.extractall(files_dir)
            else:
                return False, "❌ مصدر الملفات غير صالح", None
        
        # Scan files
        file_count, total_size, file_list = scan_directory(files_dir)
        
        if total_size > MAX_TOTAL_SIZE:
            shutil.rmtree(product_dir)
            return False, f"❌ الحجم الإجمالي كبير جداً ({total_size / 1024 / 1024:.1f} MB)", None
        
        # Validate all files
        for file_rel in file_list:
            file_path = os.path.join(files_dir, file_rel)
            is_valid, error = validate_file(file_path)
            if not is_valid:
                shutil.rmtree(product_dir)
                return False, error, None
        
        # Create metadata
        now = int(time.time())
        metadata = {
            'product_id': product_id,
            'owner_id': owner_id,
            'title': title,
            'description': description,
            'category': category,
            'tags': json.dumps(tags) if tags else None,
            'version': '1.0.0',
            'price': 0,
            'currency': 'USD',
            'is_free': True,
            'status': 'active',
            'created_at': now,
            'updated_at': now,
            'file_count': file_count,
            'total_size': total_size
        }
        
        # Save to database
        await database.create_marketplace_product(metadata)
        
        # Update category count
        await database.update_category_product_count(category)
        
        return True, "✅ تم رفع المنتج بنجاح!", product_id
        
    except Exception as e:
        # Cleanup on error
        if 'product_dir' in locals() and os.path.exists(product_dir):
            shutil.rmtree(product_dir)
        return False, f"❌ خطأ: {str(e)}", None


async def download_product(
    user_id: int,
    product_id: str,
    install_to: str = None
) -> Tuple[bool, str]:
    """
    Downloads/installs a product for a user.
    Returns (success, message)
    """
    try:
        # Get product
        product = await database.get_marketplace_product(product_id)
        if not product:
            return False, "❌ المنتج غير موجود"
        
        if product['status'] != 'active':
            return False, "❌ المنتج غير متاح حالياً"
        
        # Get source files
        source_dir = get_product_files_dir(product_id)
        if not os.path.exists(source_dir):
            return False, "❌ ملفات المنتج غير موجودة"
        
        # Determine destination
        if not install_to:
            # Default: user_bots/{user_id}/{product_title_sanitized}/
            safe_title = "".join(c for c in product['title'] if c.isalnum() or c in (' ', '_', '-')).strip()
            safe_title = safe_title.replace(' ', '_').lower()
            install_to = os.path.join(settings.UPLOAD_DIR, str(user_id), safe_title)
        
        # Create destination
        os.makedirs(install_to, exist_ok=True)
        
        # Copy files
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            dest_item = os.path.join(install_to, item)
            
            if os.path.isdir(source_item):
                shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(source_item, dest_item)

        # Set permissions to 777 for all extracted files and folders
        try: os.chmod(str(install_to), 0o777)
        except: pass
        for root, dirs, files in os.walk(str(install_to)):
            for d in dirs:
                try: os.chmod(os.path.join(root, d), 0o777)
                except: pass
            for f in files:
                try: os.chmod(os.path.join(root, f), 0o777)
                except: pass
        
        # Log download
        await database.log_product_download(product_id, user_id, product['version'])
        await database.increment_product_downloads(product_id)
        
        # Return only folder name
        folder_name = os.path.basename(install_to)
        return True, f"✅ تم التثبيت في:\n`/{folder_name}/`"
        
    except Exception as e:
        return False, f"❌ خطأ في التحميل: {str(e)}"


async def delete_product(product_id: str, user_id: int) -> Tuple[bool, str]:
    """
    Deletes a product (only by owner).
    Returns (success, message)
    """
    try:
        # Get product
        product = await database.get_marketplace_product(product_id)
        if not product:
            return False, "❌ المنتج غير موجود"
        
        # Check ownership
        if product['owner_id'] != user_id:
            return False, "❌ ليس لديك صلاحية لحذف هذا المنتج"
        
        # Delete files
        product_dir = get_product_dir(product_id)
        if os.path.exists(product_dir):
            shutil.rmtree(product_dir)
        
        # Delete from database
        await database.delete_marketplace_product(product_id)
        
        # Update category count
        await database.update_category_product_count(product['category'])
        
        return True, "✅ تم حذف المنتج بنجاح"
        
    except Exception as e:
        return False, f"❌ خطأ في الحذف: {str(e)}"


async def format_product_card(product: dict, include_stats: bool = True) -> str:
    """Formats a product as a card for display."""
    # Get rating stats
    rating_stats = await database.get_product_rating_stats(product['product_id'])
    
    # Format rating
    rating_stars = "⭐" * int(rating_stats['rating'])
    if not rating_stars:
        rating_stars = "⚪ لا تقييمات"
    
    card = f"📦 **{product['title']}**\n"
    card += f"{rating_stars} {rating_stats['rating']}/5.0 ({rating_stats['total']} تقييم)\n"
    
    if include_stats:
        card += f"📥 {product['downloads']} تحميل\n"
    
    price_text = "مجاني" if product['is_free'] else f"${product['price']}"
    card += f"💰 {price_text}\n"
    
    return card


async def format_product_details(product: dict, user_id: int = None) -> str:
    """Formats full product details."""
    # Get rating stats
    rating_stats = await database.get_product_rating_stats(product['product_id'])
    comment_count = await database.count_product_comments(product['product_id'])
    
    # Get category
    category = await database.get_marketplace_category(product['category'])
    category_name = category['name_ar'] if category else product['category']
    
    # Get developer info
    owner_id = product['owner_id']
    try:
        from bot.core.client import client
        owner = await client.get_entity(owner_id)
        owner_name = owner.first_name or "مطور"
    except:
        owner_name = "مطور"
    
    # Get developer stats (all products)
    developer_products = await database.get_user_products(owner_id)
    total_downloads = sum(p['downloads'] for p in developer_products)
    total_products = len(developer_products)
    
    # Calculate developer rating (average of all products)
    dev_ratings = []
    for p in developer_products:
        p_stats = await database.get_product_rating_stats(p['product_id'])
        if p_stats['total'] > 0:
            dev_ratings.append(p_stats['rating'])
    
    dev_rating = sum(dev_ratings) / len(dev_ratings) if dev_ratings else 0.0
    
    # Get top developers ranking
    all_developers = {}
    all_products = await database.search_marketplace_products(limit=1000, status='active')
    for p in all_products:
        dev_id = p['owner_id']
        if dev_id not in all_developers:
            all_developers[dev_id] = {'downloads': 0, 'products': 0}
        all_developers[dev_id]['downloads'] += p['downloads']
        all_developers[dev_id]['products'] += 1
    
    # Sort by downloads
    sorted_devs = sorted(all_developers.items(), key=lambda x: x[1]['downloads'], reverse=True)
    dev_rank = next((i+1 for i, (dev_id, _) in enumerate(sorted_devs) if dev_id == owner_id), None)
    
    # Format
    details = f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    details += f"📦 **{product['title']}**\n\n"
    details += f"📂 **التصنيف:** {category_name}\n"
    details += f"📝 **الوصف:**\n{product['description']}\n\n"
    
    details += f"📊 **الإحصائيات:**\n"
    details += f"• التحميلات: {product['downloads']}\n"
    details += f"• التقييم: ⭐ {rating_stats['rating']}/5.0 ({rating_stats['total']} تقييم)\n"
    details += f"• 👍 {rating_stats['likes']}  |  👎 {rating_stats['dislikes']}\n"
    details += f"• 💬 {comment_count} تعليق\n"
    details += f"• الإصدار: v{product['version']}\n"
    details += f"• الحجم: {product['total_size'] / 1024:.1f} KB\n\n"
    
    price_text = "مجاني" if product['is_free'] else f"${product['price']}"
    details += f"💰 **السعر:** {price_text}\n"
    
    # Check if user downloaded
    if user_id:
        downloaded = await database.check_user_downloaded(user_id, product['product_id'])
        if downloaded:
            details += "\n✅ **قمت بتحميل هذا المنتج من قبل**"
    
    # Developer info
    details += f"\n\n━━━━━━━━━━━━━━━━━━━━━━━\n"
    details += f"👨‍💻 **المطور:** [{owner_name}](tg://user?id={owner_id})\n"
    details += f"⭐ **تقييم المطور:** {dev_rating:.1f}/5.0\n"
    details += f"📦 **عدد المنتجات:** {total_products}\n"
    details += f"📥 **إجمالي التحميلات:** {total_downloads}\n"
    
    if dev_rank and dev_rank <= 5:
        rank_emoji = ["🥇", "🥈", "🥉", "🏅", "🏅"][dev_rank-1]
        details += f"{rank_emoji} **الترتيب:** #{dev_rank} من أفضل المطورين\n"
    
    return details


def format_time_ago(timestamp: int) -> str:
    """Formats timestamp as 'time ago'."""
    now = int(time.time())
    diff = now - timestamp
    
    if diff < 60:
        return "منذ لحظات"
    elif diff < 3600:
        minutes = diff // 60
        return f"منذ {minutes} دقيقة"
    elif diff < 86400:
        hours = diff // 3600
        return f"منذ {hours} ساعة"
    elif diff < 604800:
        days = diff // 86400
        return f"منذ {days} يوم"
    elif diff < 2592000:
        weeks = diff // 604800
        return f"منذ {weeks} أسبوع"
    else:
        months = diff // 2592000
        return f"منذ {months} شهر"


print("✅ Marketplace Service initialized.")
