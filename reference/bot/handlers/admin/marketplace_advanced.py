# bot/handlers/admin/marketplace_advanced.py
# Advanced features: Search, Logs, Settings

from telethon import events, Button
from bot.core import database
from bot.core.state import conversation_manager
from bot.handlers.admin.marketplace_admin import require_marketplace_admin

STATE_ADMIN_MP_SEARCH = "admin_mp_search"

def setup(client):
    client.add_event_handler(search_handler, events.CallbackQuery(pattern=b"admin_mp_search"))
    client.add_event_handler(search_input_handler, events.NewMessage())
    client.add_event_handler(logs_handler, events.CallbackQuery(pattern=rb"admin_mp_logs:\d+"))
    client.add_event_handler(settings_handler, events.CallbackQuery(pattern=b"admin_mp_settings"))
    client.add_event_handler(cleanup_handler, events.CallbackQuery(pattern=b"admin_mp_cleanup"))


async def search_handler(event):
    """Initiate search."""
    if not await require_marketplace_admin(event):
        return
    
    message = f"🔍 **بحث متقدم**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"يرجى كتابة:\n"
    message += f"• اسم المنتج للبحث عن منتجات\n"
    message += f"• معرف المستخدم للبحث عن مستخدم\n"
    message += f"• `product:اسم` للبحث في المنتجات فقط\n"
    message += f"• `user:معرف` للبحث في المستخدمين فقط"
    
    conversation_manager.set_value(event.sender_id, STATE_ADMIN_MP_SEARCH, "active")
    
    buttons = [[Button.inline("🔙 إلغاء", b"admin_marketplace_home")]]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def search_input_handler(event):
    """Handle search input."""
    sender_id = event.sender_id
    
    from bot.handlers.admin.marketplace_admin import is_marketplace_admin
    if not is_marketplace_admin(sender_id):
        return
    
    search_state = conversation_manager.get_value(sender_id, STATE_ADMIN_MP_SEARCH)
    if not search_state:
        return
    
    query = event.text.strip()
    
    if len(query) < 2:
        return await event.reply("❌ البحث قصير جداً (2 أحرف على الأقل)")
    
    conversation_manager.clear_value(sender_id, STATE_ADMIN_MP_SEARCH)
    
    # Parse search type
    if query.startswith('product:'):
        search_type = 'product'
        query = query.replace('product:', '').strip()
    elif query.startswith('user:'):
        search_type = 'user'
        query = query.replace('user:', '').strip()
    elif query.isdigit():
        search_type = 'user'
    else:
        search_type = 'product'
    
    # Perform search
    if search_type == 'product':
        results = await search_products(query)
        
        if not results:
            return await event.reply("❌ لم يتم العثور على منتجات")
        
        message = f"🔍 **نتائج البحث** ({len(results)} منتج)\n"
        message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        buttons = []
        for i, product in enumerate(results[:10], 1):
            message += f"{i}. **{product['title']}**\n"
            message += f"   📥 {product['downloads']} | ⭐ {product['rating']:.1f}/5.0\n\n"
            buttons.append([Button.inline(f"🔍 #{i}", f"admin_mp_product:{product['product_id']}".encode())])
        
        buttons.append([Button.inline("🔙 رجوع", b"admin_marketplace_home")])
        
        await event.reply(message, buttons=buttons, parse_mode='md')
    
    else:  # user
        try:
            user_id = int(query)
            from bot.handlers.admin.marketplace_users import get_user_marketplace_stats
            
            stats = await get_user_marketplace_stats(user_id)
            if not stats:
                return await event.reply("❌ المستخدم غير موجود في الماركت")
            
            buttons = [[Button.inline("👤 عرض الملف", f"admin_mp_user:{user_id}".encode())]]
            
            await event.reply(f"✅ تم العثور على المستخدم (ID: {user_id})", buttons=buttons)
        except:
            return await event.reply("❌ معرف المستخدم غير صحيح")


async def logs_handler(event):
    """Show admin action logs."""
    if not await require_marketplace_admin(event):
        return
    
    # Parse: admin_mp_logs:page
    page = int(event.data.decode().split(':')[1])
    
    LOGS_PER_PAGE = 10
    offset = page * LOGS_PER_PAGE
    
    logs, total = await get_admin_logs(LOGS_PER_PAGE, offset)
    total_pages = (total + LOGS_PER_PAGE - 1) // LOGS_PER_PAGE
    
    message = f"📝 **سجل الإجراءات**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"الصفحة {page + 1} من {total_pages}\n\n"
    
    if not logs:
        message += "لا توجد سجلات."
    else:
        for log in logs:
            # Get admin name
            try:
                from bot.core.client import client
                admin = await client.get_entity(log['admin_id'])
                admin_name = admin.first_name or "إدمن"
            except:
                admin_name = "إدمن"
            
            action_names = {
                'delete': '🗑️ حذف',
                'feature': '⭐ تمييز',
                'unfeature': '⭐ إلغاء تمييز',
                'ban_permanent': '🚫 حظر دائم',
                'ban_3d': '🚫 حظر 3 أيام',
                'ban_7d': '🚫 حظر 7 أيام',
                'ban_30d': '🚫 حظر 30 يوم',
                'unban': '✅ إلغاء حظر',
                'reset_warnings': '🔄 إعادة تعيين تحذيرات',
                'resolve_report_resolved': '✅ حل تقرير',
                'resolve_report_dismissed': '❌ رفض تقرير'
            }
            
            action_text = action_names.get(log['action_type'], log['action_type'])
            
            message += f"• {action_text} {log['target_type']}\n"
            message += f"  بواسطة: {admin_name}\n"
            message += f"  📅 {log['created_at']}\n\n"
    
    # Navigation
    nav_row = []
    if page > 0:
        nav_row.append(Button.inline("◀️", f"admin_mp_logs:{page-1}".encode()))
    if page < total_pages - 1:
        nav_row.append(Button.inline("▶️", f"admin_mp_logs:{page+1}".encode()))
    
    buttons = []
    if nav_row:
        buttons.append(nav_row)
    buttons.append([Button.inline("🔙 رجوع", b"admin_marketplace_home")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def settings_handler(event):
    """Show marketplace settings."""
    if not await require_marketplace_admin(event):
        return
    
    # Get current settings
    stats = await get_system_health()
    
    message = f"⚙️ **إعدادات الماركت**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    message += f"📊 **صحة النظام:**\n"
    message += f"• حجم قاعدة البيانات: {stats['db_size']:.1f} MB\n"
    message += f"• حجم الملفات: {stats['files_size']:.1f} MB\n"
    message += f"• الحظر المنتهي: {stats['expired_bans']}\n"
    message += f"• التحذيرات القديمة: {stats['old_warnings']}\n\n"
    
    message += f"🔧 **الصيانة:**\n"
    message += f"• آخر تنظيف: {stats['last_cleanup']}\n"
    message += f"• الحالة: {'✅ جيد' if stats['health_status'] == 'good' else '⚠️ يحتاج صيانة'}"
    
    buttons = [
        [Button.inline("🧹 تنظيف النظام", b"admin_mp_cleanup")],
        [Button.inline("📊 تحديث الإحصائيات", b"admin_mp_stats_overview")],
        [Button.inline("🔙 رجوع", b"admin_marketplace_home")]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def cleanup_handler(event):
    """Perform system cleanup."""
    if not await require_marketplace_admin(event):
        return
    
    await event.answer("⏳ جاري التنظيف...", alert=True)
    
    # Cleanup operations
    cleaned = await perform_cleanup()
    
    message = f"🧹 **تنظيف النظام**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"✅ تم التنظيف بنجاح!\n\n"
    message += f"• الحظر المنتهي: {cleaned['expired_bans']} محذوف\n"
    message += f"• التحذيرات القديمة: {cleaned['old_warnings']} محذوف\n"
    message += f"• الملفات المؤقتة: {cleaned['temp_files']} محذوف\n"
    message += f"• المساحة المحررة: {cleaned['freed_space']:.1f} MB"
    
    buttons = [[Button.inline("🔙 رجوع", b"admin_mp_settings")]]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


# Helper functions

async def search_products(query: str) -> list:
    """Search products by title."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        async with db.execute('''
            SELECT 
                p.product_id,
                p.title,
                p.downloads,
                AVG(CASE WHEN r.rating = 2 THEN 5.0 WHEN r.rating = 1 THEN 1.0 ELSE 3.0 END) as rating
            FROM marketplace_products p
            LEFT JOIN marketplace_reviews r ON p.product_id = r.product_id
            WHERE p.title LIKE ? AND p.status = 'active'
            GROUP BY p.product_id
            ORDER BY p.downloads DESC
            LIMIT 20
        ''', (f'%{query}%',)) as cursor:
            return [dict(row) async for row in cursor]


async def get_admin_logs(limit: int, offset: int) -> tuple:
    """Get admin action logs."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        async with db.execute('''
            SELECT * FROM marketplace_admin_logs
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset)) as cursor:
            logs = [dict(row) async for row in cursor]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_admin_logs') as cursor:
            total = (await cursor.fetchone())[0]
        
        return logs, total


async def get_system_health() -> dict:
    """Get system health statistics."""
    import os
    import time
    from bot.services.marketplace_service import MARKETPLACE_DIR
    
    stats = {}
    
    # Database size
    db_path = database.DB_NAME
    if os.path.exists(db_path):
        stats['db_size'] = os.path.getsize(db_path) / (1024 * 1024)
    else:
        stats['db_size'] = 0
    
    # Files size
    if os.path.exists(MARKETPLACE_DIR):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(MARKETPLACE_DIR):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        stats['files_size'] = total_size / (1024 * 1024)
    else:
        stats['files_size'] = 0
    
    # Expired bans
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        async with db.execute('SELECT COUNT(*) FROM marketplace_bans WHERE banned_until <= ?', (int(time.time()),)) as cursor:
            stats['expired_bans'] = (await cursor.fetchone())[0]
        
        # Old warnings (more than 30 days)
        thirty_days_ago = int(time.time()) - (30 * 24 * 60 * 60)
        async with db.execute('SELECT COUNT(*) FROM marketplace_warnings WHERE last_warning_at < ?', (thirty_days_ago,)) as cursor:
            stats['old_warnings'] = (await cursor.fetchone())[0]
    
    stats['last_cleanup'] = 'لم يتم بعد'
    stats['health_status'] = 'good' if stats['expired_bans'] < 10 and stats['old_warnings'] < 20 else 'needs_maintenance'
    
    return stats


async def perform_cleanup() -> dict:
    """Perform system cleanup."""
    import time
    import os
    import shutil
    
    cleaned = {
        'expired_bans': 0,
        'old_warnings': 0,
        'temp_files': 0,
        'freed_space': 0
    }
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        # Delete expired bans
        async with db.execute('SELECT COUNT(*) FROM marketplace_bans WHERE banned_until <= ?', (int(time.time()),)) as cursor:
            cleaned['expired_bans'] = (await cursor.fetchone())[0]
        
        await db.execute('DELETE FROM marketplace_bans WHERE banned_until <= ?', (int(time.time()),))
        
        # Delete old warnings (more than 30 days)
        thirty_days_ago = int(time.time()) - (30 * 24 * 60 * 60)
        async with db.execute('SELECT COUNT(*) FROM marketplace_warnings WHERE last_warning_at < ?', (thirty_days_ago,)) as cursor:
            cleaned['old_warnings'] = (await cursor.fetchone())[0]
        
        await db.execute('DELETE FROM marketplace_warnings WHERE last_warning_at < ?', (thirty_days_ago,))
        
        await db.commit()
    
    # Clean temp files
    from bot.services.marketplace_service import MARKETPLACE_DIR
    temp_dir = os.path.join(MARKETPLACE_DIR, 'temp')
    if os.path.exists(temp_dir):
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            try:
                if os.path.isdir(item_path):
                    size = sum(os.path.getsize(os.path.join(dirpath, filename))
                              for dirpath, dirnames, filenames in os.walk(item_path)
                              for filename in filenames)
                    shutil.rmtree(item_path)
                    cleaned['freed_space'] += size / (1024 * 1024)
                    cleaned['temp_files'] += 1
            except:
                pass
    
    return cleaned


print("✅ Marketplace advanced features loaded.")
