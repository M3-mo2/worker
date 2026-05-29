# bot/handlers/admin/marketplace_stats.py
# Statistics and analytics

from telethon import events, Button
from bot.core import database
from bot.handlers.admin.marketplace_admin import require_marketplace_admin

def setup(client):
    client.add_event_handler(stats_overview_handler, events.CallbackQuery(pattern=b"admin_mp_stats_overview"))
    client.add_event_handler(stats_top_handler, events.CallbackQuery(pattern=rb"admin_mp_stats_top:.+"))
    client.add_event_handler(stats_growth_handler, events.CallbackQuery(pattern=b"admin_mp_stats_growth"))


async def stats_overview_handler(event):
    """Show marketplace statistics overview."""
    if not await require_marketplace_admin(event):
        return
    
    stats = await get_marketplace_stats()
    
    message = f"📊 **إحصائيات الماركت**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    message += f"📈 **النمو:**\n"
    message += f"• اليوم: {stats['today_downloads']} تحميل، {stats['today_products']} منتجات جديدة\n"
    message += f"• هذا الأسبوع: {stats['week_downloads']} تحميل، {stats['week_products']} منتج\n"
    message += f"• هذا الشهر: {stats['month_downloads']} تحميل، {stats['month_products']} منتج\n\n"
    
    message += f"📦 **المنتجات:**\n"
    message += f"• الإجمالي: {stats['total_products']}\n"
    message += f"• النشط: {stats['active_products']}\n"
    message += f"• المميز: {stats['featured_products']}\n\n"
    
    message += f"👥 **المستخدمين:**\n"
    message += f"• الإجمالي: {stats['total_users']}\n"
    message += f"• المطورين: {stats['developers']}\n"
    message += f"• المحظورين: {stats['banned_users']}\n\n"
    
    message += f"⭐ **التقييمات:**\n"
    message += f"• المتوسط العام: {stats['avg_rating']:.1f}/5.0\n"
    message += f"• إجمالي التقييمات: {stats['total_ratings']}\n"
    message += f"• الإيجابية: {stats['positive_percent']:.0f}%\n\n"
    
    message += f"💬 **التفاعل:**\n"
    message += f"• التعليقات: {stats['total_comments']}\n"
    message += f"• المشاهدات: {stats['total_views']}\n"
    message += f"• التحميلات: {stats['total_downloads']}"
    
    buttons = [
        [Button.inline("🏆 الأفضل تحميلاً", b"admin_mp_stats_top:downloads"),
         Button.inline("⭐ الأعلى تقييماً", b"admin_mp_stats_top:ratings")],
        [Button.inline("👨‍💻 أفضل المطورين", b"admin_mp_stats_top:developers"),
         Button.inline("📈 النمو", b"admin_mp_stats_growth")],
        [Button.inline("🔙 رجوع", b"admin_marketplace_home")]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def stats_top_handler(event):
    """Show top products/developers."""
    if not await require_marketplace_admin(event):
        return
    
    # Parse: admin_mp_stats_top:type
    stat_type = event.data.decode().split(':')[1]
    
    if stat_type == 'downloads':
        items = await get_top_products_by_downloads(10)
        title = "🏆 الأفضل تحميلاً"
        format_func = lambda i, item: f"{i}. **{item['title']}**\n   📥 {item['downloads']} تحميل | ⭐ {item['rating']:.1f}/5.0"
    
    elif stat_type == 'ratings':
        items = await get_top_products_by_rating(10)
        title = "⭐ الأعلى تقييماً"
        format_func = lambda i, item: f"{i}. **{item['title']}**\n   ⭐ {item['rating']:.1f}/5.0 ({item['rating_count']} تقييم)"
    
    elif stat_type == 'developers':
        items = await get_top_developers_stats(10)
        title = "👨‍💻 أفضل المطورين"
        format_func = lambda i, item: f"{i}. [{item['name']}](tg://user?id={item['user_id']})\n   📦 {item['products']} منتج | 📥 {item['downloads']} تحميل"
    
    else:
        return await event.answer("❌ نوع غير صحيح", alert=True)
    
    message = f"{title}\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if not items:
        message += "لا توجد بيانات."
    else:
        medals = ["🥇", "🥈", "🥉"]
        for i, item in enumerate(items, 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            message += f"{medal} {format_func(i, item)}\n\n"
    
    buttons = [[Button.inline("🔙 رجوع", b"admin_mp_stats_overview")]]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def stats_growth_handler(event):
    """Show growth statistics."""
    if not await require_marketplace_admin(event):
        return
    
    growth = await get_growth_stats()
    
    message = f"📈 **إحصائيات النمو**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    message += f"📊 **اليوم:**\n"
    message += f"• المنتجات الجديدة: {growth['today_products']}\n"
    message += f"• التحميلات: {growth['today_downloads']}\n"
    message += f"• المستخدمين الجدد: {growth['today_users']}\n"
    message += f"• التعليقات: {growth['today_comments']}\n\n"
    
    message += f"📊 **هذا الأسبوع:**\n"
    message += f"• المنتجات الجديدة: {growth['week_products']}\n"
    message += f"• التحميلات: {growth['week_downloads']}\n"
    message += f"• المستخدمين الجدد: {growth['week_users']}\n"
    message += f"• التعليقات: {growth['week_comments']}\n\n"
    
    message += f"📊 **هذا الشهر:**\n"
    message += f"• المنتجات الجديدة: {growth['month_products']}\n"
    message += f"• التحميلات: {growth['month_downloads']}\n"
    message += f"• المستخدمين الجدد: {growth['month_users']}\n"
    message += f"• التعليقات: {growth['month_comments']}\n\n"
    
    # Calculate growth rate
    if growth['week_downloads'] > 0 and growth['prev_week_downloads'] > 0:
        growth_rate = ((growth['week_downloads'] - growth['prev_week_downloads']) / growth['prev_week_downloads']) * 100
        trend = "📈" if growth_rate > 0 else "📉"
        message += f"{trend} **معدل النمو الأسبوعي:** {growth_rate:+.1f}%"
    
    buttons = [[Button.inline("🔙 رجوع", b"admin_mp_stats_overview")]]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def get_marketplace_stats() -> dict:
    """Get comprehensive marketplace statistics."""
    import time
    
    today_start = int(time.time()) - (24 * 60 * 60)
    week_start = int(time.time()) - (7 * 24 * 60 * 60)
    month_start = int(time.time()) - (30 * 24 * 60 * 60)
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        stats = {}
        
        # Products
        async with db.execute('SELECT COUNT(*) FROM marketplace_products') as cursor:
            stats['total_products'] = (await cursor.fetchone())[0]
        
        async with db.execute("SELECT COUNT(*) FROM marketplace_products WHERE status = 'active'") as cursor:
            stats['active_products'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_featured') as cursor:
            stats['featured_products'] = (await cursor.fetchone())[0]
        
        # Growth
        async with db.execute('SELECT COUNT(*) FROM marketplace_products WHERE created_at > ?', (today_start,)) as cursor:
            stats['today_products'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_products WHERE created_at > ?', (week_start,)) as cursor:
            stats['week_products'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_products WHERE created_at > ?', (month_start,)) as cursor:
            stats['month_products'] = (await cursor.fetchone())[0]
        
        # Downloads
        async with db.execute('SELECT COUNT(*) FROM marketplace_downloads WHERE downloaded_at > ?', (today_start,)) as cursor:
            stats['today_downloads'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_downloads WHERE downloaded_at > ?', (week_start,)) as cursor:
            stats['week_downloads'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_downloads WHERE downloaded_at > ?', (month_start,)) as cursor:
            stats['month_downloads'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_downloads') as cursor:
            stats['total_downloads'] = (await cursor.fetchone())[0]
        
        # Users
        async with db.execute('SELECT COUNT(DISTINCT owner_id) FROM marketplace_products') as cursor:
            stats['total_users'] = (await cursor.fetchone())[0]
        
        async with db.execute("SELECT COUNT(DISTINCT owner_id) FROM marketplace_products WHERE status = 'active'") as cursor:
            stats['developers'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_bans WHERE banned_until > ?', (int(time.time()),)) as cursor:
            stats['banned_users'] = (await cursor.fetchone())[0]
        
        # Ratings
        async with db.execute('''
            SELECT 
                AVG(CASE WHEN rating = 2 THEN 5.0 WHEN rating = 1 THEN 1.0 ELSE 3.0 END) as avg,
                COUNT(*) as total,
                SUM(CASE WHEN rating = 2 THEN 1 ELSE 0 END) as positive
            FROM marketplace_reviews
        ''') as cursor:
            row = await cursor.fetchone()
            stats['avg_rating'] = row[0] if row[0] else 0.0
            stats['total_ratings'] = row[1]
            stats['positive_percent'] = (row[2] / row[1] * 100) if row[1] > 0 else 0
        
        # Comments & Views
        async with db.execute('SELECT COUNT(*) FROM marketplace_comments') as cursor:
            stats['total_comments'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT SUM(views) FROM marketplace_products') as cursor:
            stats['total_views'] = (await cursor.fetchone())[0] or 0
        
        return stats


async def get_top_products_by_downloads(limit: int) -> list:
    """Get top products by downloads."""
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
            WHERE p.status = 'active'
            GROUP BY p.product_id
            ORDER BY p.downloads DESC
            LIMIT ?
        ''', (limit,)) as cursor:
            return [dict(row) async for row in cursor]


async def get_top_products_by_rating(limit: int) -> list:
    """Get top products by rating."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        async with db.execute('''
            SELECT 
                p.product_id,
                p.title,
                AVG(CASE WHEN r.rating = 2 THEN 5.0 WHEN r.rating = 1 THEN 1.0 ELSE 3.0 END) as rating,
                COUNT(*) as rating_count
            FROM marketplace_products p
            INNER JOIN marketplace_reviews r ON p.product_id = r.product_id
            WHERE p.status = 'active'
            GROUP BY p.product_id
            HAVING rating_count >= 3
            ORDER BY rating DESC, rating_count DESC
            LIMIT ?
        ''', (limit,)) as cursor:
            return [dict(row) async for row in cursor]


async def get_top_developers_stats(limit: int) -> list:
    """Get top developers."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        async with db.execute('''
            SELECT 
                p.owner_id as user_id,
                COUNT(DISTINCT p.product_id) as products,
                SUM(p.downloads) as downloads
            FROM marketplace_products p
            WHERE p.status = 'active'
            GROUP BY p.owner_id
            ORDER BY downloads DESC
            LIMIT ?
        ''', (limit,)) as cursor:
            developers = []
            async for row in cursor:
                dev = dict(row)
                # Get name
                try:
                    from bot.core.client import client
                    user = await client.get_entity(dev['user_id'])
                    dev['name'] = user.first_name or "مطور"
                except:
                    dev['name'] = "مطور"
                developers.append(dev)
            return developers


async def get_growth_stats() -> dict:
    """Get growth statistics."""
    import time
    
    today_start = int(time.time()) - (24 * 60 * 60)
    week_start = int(time.time()) - (7 * 24 * 60 * 60)
    month_start = int(time.time()) - (30 * 24 * 60 * 60)
    prev_week_start = int(time.time()) - (14 * 24 * 60 * 60)
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        growth = {}
        
        # Today
        async with db.execute('SELECT COUNT(*) FROM marketplace_products WHERE created_at > ?', (today_start,)) as cursor:
            growth['today_products'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_downloads WHERE downloaded_at > ?', (today_start,)) as cursor:
            growth['today_downloads'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(DISTINCT owner_id) FROM marketplace_products WHERE created_at > ?', (today_start,)) as cursor:
            growth['today_users'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_comments WHERE created_at > ?', (today_start,)) as cursor:
            growth['today_comments'] = (await cursor.fetchone())[0]
        
        # Week
        async with db.execute('SELECT COUNT(*) FROM marketplace_products WHERE created_at > ?', (week_start,)) as cursor:
            growth['week_products'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_downloads WHERE downloaded_at > ?', (week_start,)) as cursor:
            growth['week_downloads'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(DISTINCT owner_id) FROM marketplace_products WHERE created_at > ?', (week_start,)) as cursor:
            growth['week_users'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_comments WHERE created_at > ?', (week_start,)) as cursor:
            growth['week_comments'] = (await cursor.fetchone())[0]
        
        # Month
        async with db.execute('SELECT COUNT(*) FROM marketplace_products WHERE created_at > ?', (month_start,)) as cursor:
            growth['month_products'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_downloads WHERE downloaded_at > ?', (month_start,)) as cursor:
            growth['month_downloads'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(DISTINCT owner_id) FROM marketplace_products WHERE created_at > ?', (month_start,)) as cursor:
            growth['month_users'] = (await cursor.fetchone())[0]
        
        async with db.execute('SELECT COUNT(*) FROM marketplace_comments WHERE created_at > ?', (month_start,)) as cursor:
            growth['month_comments'] = (await cursor.fetchone())[0]
        
        # Previous week (for growth rate)
        async with db.execute('SELECT COUNT(*) FROM marketplace_downloads WHERE downloaded_at BETWEEN ? AND ?', (prev_week_start, week_start)) as cursor:
            growth['prev_week_downloads'] = (await cursor.fetchone())[0]
        
        return growth


print("✅ Marketplace stats admin loaded.")
