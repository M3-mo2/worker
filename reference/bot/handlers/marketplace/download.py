# bot/handlers/marketplace/download.py
# Download and install products

import os
import tempfile
import zipfile
from telethon import events, Button
from bot.core import database
from bot.services import marketplace_service
from bot.services.user_service import check_user_status


def setup(client):
    client.add_event_handler(download_handler, events.CallbackQuery(pattern=b"mp_download:"))
    client.add_event_handler(download_confirm_handler, events.CallbackQuery(pattern=b"mp_dl_confirm:"))
    client.add_event_handler(my_downloads_handler, events.CallbackQuery(pattern=b"mp_my_downloads"))


async def download_handler(event):
    """Show download confirmation."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse product_id
    product_id = event.data.decode().split(':')[1]
    
    # Get product
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    # Check if already downloaded
    downloaded = await database.check_user_downloaded(sender_id, product_id)
    
    message = "📥 **تأكيد التحميل**\n\n"
    message += f"أنت على وشك تحميل:\n"
    message += f"📦 **{product['title']}** v{product['version']}\n\n"
    message += f"📁 **الملفات:** {product['file_count']} ملف\n"
    message += f"📦 **الحجم:** {product['total_size'] / 1024:.1f} KB\n\n"
    message += f"📂 **سيتم التثبيت في:**\n"
    message += f"`/{product['title'].lower().replace(' ', '_')}/`\n\n"
    
    if downloaded:
        message += "✅ **قمت بتحميل هذا المنتج من قبل**\n\n"
    
    message += "⚠️ **ملاحظة:** تأكد من مراجعة الكود قبل التشغيل!"
    
    buttons = [
        [Button.inline("✅ تحميل وتثبيت", f"mp_dl_confirm:{product_id}".encode())],
        [Button.inline("❌ إلغاء", f"mp_view:{product_id}".encode())]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def download_confirm_handler(event):
    """Confirm and download product."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse product_id
    product_id = event.data.decode().split(':')[1]
    
    # Check download limit (max 3 times per user)
    download_count = await database.get_user_download_count(sender_id, product_id)
    if download_count >= 3:
        return await event.answer("⚠️ وصلت للحد الأقصى (3 تحميلات) لهذا المنتج", alert=True)
    
    await event.edit("⏳ جاري التحميل...")
    
    # Get product
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    # Get source files
    source_dir = marketplace_service.get_product_files_dir(product_id)
    if not os.path.exists(source_dir):
        return await event.edit("❌ ملفات المنتج غير موجودة")
    
    # Check if has Python files or many files
    has_python = False
    file_count = 0
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_count += 1
            if file.endswith('.py'):
                has_python = True
                break
        if has_python:
            break
    
    # If Python or many files, send as zip
    if has_python or file_count > 5:
        try:
            import tempfile
            import zipfile
            from bot.core.client import client
            
            # Create temp zip
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp:
                zip_path = tmp.name
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)
            
            # Log download
            await database.log_product_download(product_id, sender_id, product['version'])
            await database.increment_product_downloads(product_id)
            
            # Send file
            caption = f"📦 **{product['title']}** v{product['version']}\n\n"
            caption += f"📁 {file_count} ملف\n"
            caption += f"📦 {product['total_size'] / 1024:.1f} KB\n\n"
            caption += "✅ تم إرسال الملفات مضغوطة\n"
            caption += "فك الضغط وارفعها للبوت"
            
            await client.send_file(
                sender_id,
                zip_path,
                caption=caption,
                parse_mode='md'
            )
            
            # Clean up
            os.unlink(zip_path)
            
            buttons = [
                [Button.inline("⭐ تقييم المنتج", f"mp_view:{product_id}".encode())],
                [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
            ]
            
            await event.edit("✅ تم إرسال الملفات بنجاح!", buttons=buttons)
            
        except Exception as e:
            await event.edit(f"❌ خطأ في الإرسال: {str(e)}")
    
    else:
        # Install normally for PHP
        success, message = await marketplace_service.download_product(sender_id, product_id)
        
        if success:
            final_message = "✅ **تم التحميل بنجاح**\n\n"
            final_message += f"📦 **{product['title']}** v{product['version']}\n\n"
            final_message += message + "\n\n"
            final_message += "🚀 **الخطوات التالية**\n"
            final_message += "1. افتح مجلد البوت من قائمة الملفات\n"
            final_message += "2. راجع الملفات وعدّل حسب احتياجاتك\n"
            final_message += "3. شغّل البوت\n\n"
            final_message += "💡 **نصيحة:** لا تنسَ تقييم المنتج بعد التجربة"
            
            buttons = [
                [Button.inline("⭐ تقييم المنتج الآن", f"mp_view:{product_id}".encode())],
                [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
            ]
            
            await event.edit(final_message, buttons=buttons, parse_mode='md')
        else:
            buttons = [
                [Button.inline("🔄 إعادة المحاولة", f"mp_download:{product_id}".encode())],
                [Button.inline("🔙 رجوع", f"mp_view:{product_id}".encode())]
            ]
            
            await event.edit(message, buttons=buttons, parse_mode='md')


async def my_downloads_handler(event):
    """Show user's download history."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse page: mp_my_downloads:page
    data = event.data.decode().split(':')
    page = int(data[1]) if len(data) > 1 else 0
    
    # Pagination
    DOWNLOADS_PER_PAGE = 8
    offset = page * DOWNLOADS_PER_PAGE
    
    # Get all downloads
    all_downloads = await database.get_user_downloads(sender_id, limit=1000)
    total = len(all_downloads)
    downloads = all_downloads[offset:offset + DOWNLOADS_PER_PAGE]
    
    total_pages = (total + DOWNLOADS_PER_PAGE - 1) // DOWNLOADS_PER_PAGE
    
    if not all_downloads:
        message = "📥 **تحميلاتي**\n\nلم تقم بتحميل أي منتجات بعد."
        buttons = [[Button.inline("🔙 رجوع", b"marketplace_home")]]
        return await event.edit(message, buttons=buttons, parse_mode='md')
    
    message = f"📥 **تحميلاتي** ({total} منتج)\n"
    
    if total_pages > 1:
        message += f"الصفحة {page + 1} من {total_pages}\n"
    
    message += "\n"
    
    buttons = []
    for dl in downloads:
        time_ago = marketplace_service.format_time_ago(dl['downloaded_at'])
        btn_text = f"📦 {dl['title']} - {time_ago}"
        btn_data = f"mp_view:{dl['product_id']}".encode()
        buttons.append([Button.inline(btn_text, btn_data)])
    
    # Pagination buttons
    if total_pages > 1:
        nav_row = []
        if page > 0:
            nav_row.append(Button.inline("◀️", f"mp_my_downloads:{page-1}".encode()))
        if page < total_pages - 1:
            nav_row.append(Button.inline("▶️", f"mp_my_downloads:{page+1}".encode()))
        if nav_row:
            buttons.append(nav_row)
    
    buttons.append([Button.inline("🔙 رجوع", b"marketplace_home")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


print("✅ Marketplace download handlers loaded.")
