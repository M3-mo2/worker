# bot/handlers/marketplace/manage.py
# Manage user's own products

from telethon import events, Button
from bot.core import database
from bot.services import marketplace_service
from bot.services.user_service import check_user_status


def setup(client):
    client.add_event_handler(my_products_handler, events.CallbackQuery(pattern=b"mp_my_products"))
    client.add_event_handler(manage_product_handler, events.CallbackQuery(pattern=b"mp_manage:"))
    client.add_event_handler(product_stats_handler, events.CallbackQuery(pattern=b"mp_stats:"))
    client.add_event_handler(delete_product_handler, events.CallbackQuery(pattern=b"mp_delete:"))
    client.add_event_handler(delete_confirm_handler, events.CallbackQuery(pattern=b"mp_del_confirm:"))


async def my_products_handler(event):
    """Show user's products."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse page: mp_my_products:page
    data = event.data.decode().split(':')
    page = int(data[1]) if len(data) > 1 else 0
    
    # Pagination
    PRODUCTS_PER_PAGE = 6
    offset = page * PRODUCTS_PER_PAGE
    
    # Get all products
    all_products = await database.get_user_products(sender_id)
    total = len(all_products)
    products = all_products[offset:offset + PRODUCTS_PER_PAGE]
    
    total_pages = (total + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE
    
    if not all_products:
        message = "📦 **منتجاتي**\n\nليس لديك أي منتجات منشورة بعد."
        buttons = [
            [Button.inline("📤 رفع منتج جديد", b"mp_upload_start")],
            [Button.inline("🔙 رجوع", b"marketplace_home")]
        ]
        return await event.edit(message, buttons=buttons, parse_mode='md')
    
    message = f"📦 **منتجاتي** ({total} منتج)\n"
    
    if total_pages > 1:
        message += f"الصفحة {page + 1} من {total_pages}\n"
    
    message += "\n"
    
    buttons = []
    for product in products:
        # Get stats
        rating_stats = await database.get_product_rating_stats(product['product_id'])
        comment_count = await database.count_product_comments(product['product_id'])
        
        # Compact button text
        btn_text = f"📦 {product['title'][:25]}"
        if len(product['title']) > 25:
            btn_text = f"📦 {product['title'][:22]}..."
        btn_text += f" | 📥 {product['downloads']} ⭐ {rating_stats['rating']}"
        
        btn_data = f"mp_manage:{product['product_id']}".encode()
        buttons.append([Button.inline(btn_text, btn_data)])
    
    # Pagination buttons
    if total_pages > 1:
        nav_row = []
        if page > 0:
            nav_row.append(Button.inline("◀️", f"mp_my_products:{page-1}".encode()))
        if page < total_pages - 1:
            nav_row.append(Button.inline("▶️", f"mp_my_products:{page+1}".encode()))
        if nav_row:
            buttons.append(nav_row)
    
    buttons.append([Button.inline("📤 رفع منتج جديد", b"mp_upload_start")])
    buttons.append([Button.inline("🔙 رجوع", b"marketplace_home")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def manage_product_handler(event):
    """Manage a specific product."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse product_id
    product_id = event.data.decode().split(':')[1]
    
    # Get product
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    # Check ownership
    if product['owner_id'] != sender_id:
        return await event.answer("❌ ليس لديك صلاحية لإدارة هذا المنتج", alert=True)
    
    # Get stats
    rating_stats = await database.get_product_rating_stats(product_id)
    comment_count = await database.count_product_comments(product_id)
    
    message = f"⚙️ **إدارة المنتج**\n\n"
    message += f"📦 **{product['title']}**\n\n"
    message += f"📊 **ملخص الإحصائيات:**\n"
    message += f"• المشاهدات: {product['views']}\n"
    message += f"• التحميلات: {product['downloads']}\n"
    message += f"• التقييم: ⭐ {rating_stats['rating']}/5.0\n"
    message += f"• التعليقات: {comment_count}\n"
    
    buttons = [
        [Button.inline("📊 إحصائيات مفصلة", f"mp_stats:{product_id}".encode())],
        [Button.inline("📦 عرض المنتج", f"mp_view:{product_id}".encode())],
        [Button.inline("💬 عرض التعليقات", f"mp_comments:{product_id}:0".encode())],
        [Button.inline("🗑️ حذف المنتج", f"mp_delete:{product_id}".encode())],
        [Button.inline("🔙 رجوع لمنتجاتي", b"mp_my_products")]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def product_stats_handler(event):
    """Show detailed product statistics."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse product_id
    product_id = event.data.decode().split(':')[1]
    
    # Get product
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    # Check ownership
    if product['owner_id'] != sender_id:
        return await event.answer("❌ ليس لديك صلاحية لعرض هذه الإحصائيات", alert=True)
    
    # Get stats
    rating_stats = await database.get_product_rating_stats(product_id)
    comment_count = await database.count_product_comments(product_id)
    
    message = f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    message += f"📊 **إحصائيات مفصلة**\n\n"
    message += f"📦 **{product['title']}**\n"
    message += f"🏷️ الإصدار: v{product['version']}\n\n"
    
    message += f"👁️ **المشاهدات**\n"
    message += f"• إجمالي المشاهدات: {product['views']}\n\n"
    
    message += f"📥 **التحميلات**\n"
    message += f"• إجمالي التحميلات: {product['downloads']}\n"
    if product['views'] > 0:
        conversion_rate = (product['downloads'] / product['views'] * 100)
        message += f"• معدل التحويل: {conversion_rate:.1f}%\n"
    message += "\n"
    
    message += f"⭐ **التقييمات**\n"
    message += f"• التقييم العام: {rating_stats['rating']}/5.0\n"
    message += f"• عدد التقييمات: {rating_stats['total']}\n"
    message += f"• 👍 إعجاب: {rating_stats['likes']}\n"
    message += f"• 👎 عدم إعجاب: {rating_stats['dislikes']}\n"
    if rating_stats['total'] > 0:
        like_rate = (rating_stats['likes'] / rating_stats['total'] * 100)
        message += f"• نسبة الإعجاب: {like_rate:.1f}%\n"
    message += "\n"
    
    message += f"💬 **التعليقات**\n"
    message += f"• عدد التعليقات: {comment_count}\n\n"
    
    message += f"📌 **الحالة:** {product['status']}\n"
    
    buttons = [
        [Button.inline("🔙 رجوع للإدارة", f"mp_manage:{product_id}".encode())]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def delete_product_handler(event):
    """Show delete confirmation."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse product_id
    product_id = event.data.decode().split(':')[1]
    
    # Get product
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    # Check ownership
    if product['owner_id'] != sender_id:
        return await event.answer("❌ ليس لديك صلاحية لحذف هذا المنتج", alert=True)
    
    message = "⚠️ **تأكيد الحذف**\n\n"
    message += f"هل أنت متأكد من حذف:\n"
    message += f"📦 **{product['title']}**\n\n"
    message += f"⚠️ **تحذير:** هذا الإجراء لا يمكن التراجع عنه!\n"
    message += f"سيتم حذف جميع الملفات والتقييمات والتعليقات."
    
    buttons = [
        [Button.inline("✅ نعم، احذف المنتج", f"mp_del_confirm:{product_id}".encode())],
        [Button.inline("❌ إلغاء", f"mp_manage:{product_id}".encode())]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def delete_confirm_handler(event):
    """Confirm and delete product."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse product_id
    product_id = event.data.decode().split(':')[1]
    
    await event.edit("⏳ جاري الحذف...")
    
    # Delete product
    success, message = await marketplace_service.delete_product(product_id, sender_id)
    
    buttons = [[Button.inline("🔙 رجوع لمنتجاتي", b"mp_my_products")]]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


print("✅ Marketplace manage handlers loaded.")
