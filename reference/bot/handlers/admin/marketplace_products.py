# bot/handlers/admin/marketplace_products.py
# Product management for admins

from telethon import events, Button
from bot.core import database
from bot.core.state import conversation_manager
from bot.handlers.admin.marketplace_admin import is_marketplace_admin, require_marketplace_admin

STATE_ADMIN_MP_DELETE_REASON = "admin_mp_delete_reason"

def setup(client):
    client.add_event_handler(products_list_handler, events.CallbackQuery(pattern=rb"admin_mp_products:.+"))
    client.add_event_handler(product_detail_handler, events.CallbackQuery(pattern=rb"admin_mp_product:.+"))
    client.add_event_handler(delete_product_handler, events.CallbackQuery(pattern=rb"admin_mp_delete:.+"))
    client.add_event_handler(feature_product_handler, events.CallbackQuery(pattern=rb"admin_mp_feature:.+"))
    client.add_event_handler(delete_reason_handler, events.NewMessage())


async def products_list_handler(event):
    """List products with filters."""
    if not await require_marketplace_admin(event):
        return
    
    # Parse: admin_mp_products:filter:page
    data = event.data.decode().split(':')
    filter_type = data[1]
    page = int(data[2]) if len(data) > 2 else 0
    
    PRODUCTS_PER_PAGE = 8
    offset = page * PRODUCTS_PER_PAGE
    
    # Get products based on filter
    if filter_type == 'all':
        products = await database.search_marketplace_products(limit=PRODUCTS_PER_PAGE, offset=offset, status='active')
        total = await database.count_marketplace_products(status='active')
        title = "جميع المنتجات"
    elif filter_type == 'featured':
        products = await get_featured_products(limit=PRODUCTS_PER_PAGE, offset=offset)
        total = await count_featured_products()
        title = "المنتجات المميزة"
    elif filter_type == 'reported':
        products = await get_reported_products(limit=PRODUCTS_PER_PAGE, offset=offset)
        total = await count_reported_products()
        title = "المنتجات المُبلغ عنها"
    elif filter_type == 'top':
        products = await database.search_marketplace_products(sort_by='downloads', limit=PRODUCTS_PER_PAGE, offset=offset, status='active')
        total = await database.count_marketplace_products(status='active')
        title = "الأكثر تحميلاً"
    else:
        products = await database.search_marketplace_products(limit=PRODUCTS_PER_PAGE, offset=offset, status='active')
        total = await database.count_marketplace_products(status='active')
        title = "جميع المنتجات"
    
    total_pages = (total + PRODUCTS_PER_PAGE - 1) // PRODUCTS_PER_PAGE
    
    message = f"📦 **إدارة المنتجات**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"الفلتر: {title} | الصفحة {page + 1} من {total_pages}\n\n"
    
    if not products:
        message += "لا توجد منتجات."
    else:
        for i, product in enumerate(products, 1):
            # Get developer name
            try:
                from bot.core.client import client
                owner = await client.get_entity(product['owner_id'])
                owner_name = owner.first_name or "مطور"
            except:
                owner_name = "مطور"
            
            # Get rating
            rating_stats = await database.get_product_rating_stats(product['product_id'])
            
            # Check if featured
            is_featured = await check_if_featured(product['product_id'])
            featured_mark = "⭐ " if is_featured else ""
            
            # Check reports
            report_count = await count_product_reports(product['product_id'])
            report_mark = f" 🚨 {report_count}" if report_count > 0 else ""
            
            message += f"{i}️⃣ {featured_mark}**{product['title']}** v{product['version']}\n"
            message += f"   👤 {owner_name}\n"
            message += f"   📥 {product['downloads']} | ⭐ {rating_stats['rating']}/5.0{report_mark}\n\n"
    
    # Filter buttons
    filter_buttons = []
    filters = [
        ('الكل', 'all'),
        ('مميز', 'featured'),
        ('مُبلغ عنه', 'reported'),
        ('الأفضل', 'top')
    ]
    
    row = []
    for label, ftype in filters:
        if ftype == filter_type:
            row.append(Button.inline(f"● {label}", f"admin_mp_products:{ftype}:0".encode()))
        else:
            row.append(Button.inline(f"○ {label}", f"admin_mp_products:{ftype}:0".encode()))
        if len(row) == 2:
            filter_buttons.append(row)
            row = []
    if row:
        filter_buttons.append(row)
    
    # Product buttons
    product_buttons = []
    for i, product in enumerate(products, 1):
        product_buttons.append([Button.inline(f"🔍 #{i}", f"admin_mp_product:{product['product_id']}".encode())])
    
    # Navigation
    nav_row = []
    if page > 0:
        nav_row.append(Button.inline("◀️", f"admin_mp_products:{filter_type}:{page-1}".encode()))
    if page < total_pages - 1:
        nav_row.append(Button.inline("▶️", f"admin_mp_products:{filter_type}:{page+1}".encode()))
    
    buttons = filter_buttons + product_buttons
    if nav_row:
        buttons.append(nav_row)
    buttons.append([Button.inline("🔙 رجوع", b"admin_marketplace_home")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def product_detail_handler(event):
    """Show product details for admin."""
    if not await require_marketplace_admin(event):
        return
    
    product_id = event.data.decode().split(':')[1]
    
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    # Get developer info
    try:
        from bot.core.client import client
        owner = await client.get_entity(product['owner_id'])
        owner_name = owner.first_name or "مطور"
    except:
        owner_name = "مطور"
    
    # Get stats
    rating_stats = await database.get_product_rating_stats(product_id)
    comment_count = await database.count_product_comments(product_id)
    
    # Get category
    category = await database.get_marketplace_category(product['category'])
    category_name = category['name_ar'] if category else product['category']
    
    # Check if featured
    is_featured = await check_if_featured(product_id)
    
    # Get reports
    report_count = await count_product_reports(product_id)
    
    message = f"🔍 **تفاصيل المنتج**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"📦 **{product['title']}** v{product['version']}\n"
    message += f"👤 المطور: [{owner_name}](tg://user?id={product['owner_id']})\n\n"
    
    message += f"📝 **الوصف:**\n{product['description']}\n\n"
    
    message += f"📂 التصنيف: {category_name}\n"
    message += f"📦 الحجم: {product['total_size'] / 1024:.1f} KB\n"
    message += f"📁 عدد الملفات: {product['file_count']} ملف\n\n"
    
    message += f"📊 **الإحصائيات:**\n"
    message += f"• التحميلات: {product['downloads']}\n"
    message += f"• المشاهدات: {product['views']}\n"
    message += f"• التقييم: ⭐ {rating_stats['rating']}/5.0 ({rating_stats['total']} تقييم)\n"
    message += f"• 👍 {rating_stats['likes']} | 👎 {rating_stats['dislikes']}\n"
    message += f"• التعليقات: {comment_count}\n\n"
    
    message += f"🚨 التقارير: {report_count}\n"
    message += f"⭐ الحالة: {'مميز' if is_featured else 'عادي'}\n"
    message += f"📅 تاريخ النشر: {product['created_at']}"
    
    feature_text = "إلغاء التمييز" if is_featured else "تمييز"
    
    buttons = [
        [Button.inline(f"⭐ {feature_text}", f"admin_mp_feature:{product_id}".encode()),
         Button.inline("🗑️ حذف", f"admin_mp_delete:{product_id}".encode())],
        [Button.inline("👤 ملف المطور", f"admin_mp_user:{product['owner_id']}".encode()),
         Button.inline("💬 التعليقات", f"mp_comments:{product_id}:0".encode())],
    ]
    
    if report_count > 0:
        buttons.append([Button.inline(f"🚨 عرض التقارير ({report_count})", f"admin_mp_product_reports:{product_id}:0".encode())])
    
    buttons.append([Button.inline("🔙 رجوع للقائمة", b"admin_mp_products:all:0")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def delete_product_handler(event):
    """Initiate product deletion."""
    if not await require_marketplace_admin(event):
        return
    
    product_id = event.data.decode().split(':')[1]
    
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    # Get stats
    comment_count = await database.count_product_comments(product_id)
    rating_count = (await database.get_product_rating_stats(product_id))['total']
    
    message = f"🗑️ **حذف المنتج**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"المنتج: **{product['title']}**\n\n"
    message += f"⚠️ **سيتم حذف:**\n"
    message += f"• المنتج وجميع ملفاته\n"
    message += f"• جميع التعليقات ({comment_count})\n"
    message += f"• جميع التقييمات ({rating_count})\n"
    message += f"• سجل التحميلات ({product['downloads']})\n\n"
    message += f"يرجى كتابة سبب الحذف:\n"
    message += f"(سيتم إرساله للمطور)"
    
    # Set state
    conversation_manager.set_value(event.sender_id, STATE_ADMIN_MP_DELETE_REASON, product_id)
    
    buttons = [[Button.inline("🔙 إلغاء", f"admin_mp_product:{product_id}".encode())]]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def delete_reason_handler(event):
    """Handle delete reason input."""
    sender_id = event.sender_id
    
    if not is_marketplace_admin(sender_id):
        return
    
    product_id = conversation_manager.get_value(sender_id, STATE_ADMIN_MP_DELETE_REASON)
    if not product_id:
        return
    
    reason = event.text.strip()
    
    if len(reason) < 5:
        return await event.reply("❌ السبب قصير جداً (5 أحرف على الأقل)")
    
    product = await database.get_marketplace_product(product_id)
    if not product:
        conversation_manager.clear_value(sender_id, STATE_ADMIN_MP_DELETE_REASON)
        return await event.reply("❌ المنتج غير موجود")
    
    # Delete product
    success = await delete_product_completely(product_id, sender_id, reason)
    
    conversation_manager.clear_value(sender_id, STATE_ADMIN_MP_DELETE_REASON)
    
    if success:
        # Notify developer
        try:
            from bot.core.client import client
            notify_msg = f"🗑️ **تم حذف منتجك**\n\n"
            notify_msg += f"المنتج: {product['title']}\n\n"
            notify_msg += f"السبب: {reason}\n\n"
            notify_msg += f"إذا كان لديك استفسار، يرجى التواصل مع الإدارة."
            await client.send_message(product['owner_id'], notify_msg, parse_mode='md')
        except:
            pass
        
        await event.reply("✅ تم حذف المنتج نهائياً وإرسال الإشعار للمطور")
    else:
        await event.reply("❌ حدث خطأ أثناء الحذف")


async def feature_product_handler(event):
    """Toggle product featured status."""
    if not await require_marketplace_admin(event):
        return
    
    product_id = event.data.decode().split(':')[1]
    
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    is_featured = await check_if_featured(product_id)
    
    if is_featured:
        # Unfeature
        await unfeature_product(product_id)
        await event.answer("✅ تم إلغاء تمييز المنتج", alert=True)
    else:
        # Feature
        await feature_product(product_id, event.sender_id)
        await event.answer("✅ تم تمييز المنتج", alert=True)
    
    # Log action
    await log_admin_action(
        event.sender_id,
        'feature' if not is_featured else 'unfeature',
        'product',
        product_id
    )
    
    # Refresh view
    await product_detail_handler(event)


# Helper functions

async def get_featured_products(limit: int, offset: int) -> list:
    """Get featured products."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        async with db.execute('''
            SELECT p.* FROM marketplace_products p
            INNER JOIN marketplace_featured f ON p.product_id = f.product_id
            WHERE p.status = 'active'
            ORDER BY f.priority DESC, f.featured_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset)) as cursor:
            return [dict(row) async for row in cursor]


async def count_featured_products() -> int:
    """Count featured products."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        async with db.execute('SELECT COUNT(*) FROM marketplace_featured') as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def get_reported_products(limit: int, offset: int) -> list:
    """Get products with reports."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        async with db.execute('''
            SELECT p.*, COUNT(r.id) as report_count
            FROM marketplace_products p
            INNER JOIN marketplace_reports r ON p.product_id = r.target_id
            WHERE r.target_type = 'product' AND r.status = 'pending' AND p.status = 'active'
            GROUP BY p.product_id
            ORDER BY report_count DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset)) as cursor:
            return [dict(row) async for row in cursor]


async def count_reported_products() -> int:
    """Count products with reports."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        async with db.execute('''
            SELECT COUNT(DISTINCT target_id) FROM marketplace_reports
            WHERE target_type = 'product' AND status = 'pending'
        ''') as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def check_if_featured(product_id: str) -> bool:
    """Check if product is featured."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        async with db.execute('SELECT 1 FROM marketplace_featured WHERE product_id = ?', (product_id,)) as cursor:
            return await cursor.fetchone() is not None


async def feature_product(product_id: str, admin_id: int):
    """Feature a product."""
    import time
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        await db.execute('''
            INSERT OR REPLACE INTO marketplace_featured (product_id, featured_at, featured_by, priority)
            VALUES (?, ?, ?, 0)
        ''', (product_id, int(time.time()), admin_id))
        await db.commit()


async def unfeature_product(product_id: str):
    """Unfeature a product."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        await db.execute('DELETE FROM marketplace_featured WHERE product_id = ?', (product_id,))
        await db.commit()


async def count_product_reports(product_id: str) -> int:
    """Count reports for a product."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        async with db.execute('''
            SELECT COUNT(*) FROM marketplace_reports
            WHERE target_type = 'product' AND target_id = ? AND status = 'pending'
        ''', (product_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0


async def delete_product_completely(product_id: str, admin_id: int, reason: str) -> bool:
    """Delete product and all related data."""
    import shutil
    import os
    from bot.services.marketplace_service import get_product_files_dir
    
    try:
        async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
            # Delete from database (CASCADE will handle related data)
            await db.execute('DELETE FROM marketplace_products WHERE product_id = ?', (product_id,))
            await db.commit()
        
        # Delete files
        product_dir = get_product_files_dir(product_id)
        if os.path.exists(product_dir):
            shutil.rmtree(product_dir)
        
        # Log action
        await log_admin_action(admin_id, 'delete', 'product', product_id, reason)
        
        return True
    except Exception as e:
        print(f"Error deleting product: {e}")
        return False


async def log_admin_action(admin_id: int, action_type: str, target_type: str, target_id: str, reason: str = None):
    """Log admin action."""
    import time
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        await db.execute('''
            INSERT INTO marketplace_admin_logs (admin_id, action_type, target_type, target_id, reason, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (admin_id, action_type, target_type, target_id, reason, int(time.time())))
        await db.commit()


print("✅ Marketplace products admin loaded.")
