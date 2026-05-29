# bot/handlers/admin/marketplace_admin.py
# Main marketplace admin panel

from telethon import events, Button
from bot.core import database
from bot.core.config import settings

def is_marketplace_admin(user_id: int) -> bool:
    """Check if user is marketplace admin."""
    return user_id in settings.telegram.SUDO_USERS


async def require_marketplace_admin(event):
    """Check admin permission."""
    if not is_marketplace_admin(event.sender_id):
        return await event.answer("🚫 غير مصرح لك بالوصول", alert=True)
    return True


def setup(client):
    client.add_event_handler(marketplace_admin_home_handler, events.CallbackQuery(pattern=b"admin_marketplace_home"))


async def marketplace_admin_home_handler(event):
    """Main marketplace admin dashboard."""
    if not await require_marketplace_admin(event):
        return
    
    # Get overview stats
    stats = await get_admin_overview_stats()
    
    message = "🛒 **إدارة الماركت**\n"
    message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    message += "📊 **الإحصائيات السريعة:**\n"
    message += f"• المنتجات: {stats['total_products']} منتج نشط\n"
    message += f"• المستخدمين: {stats['total_users']} ({stats['banned_users']} محظورين)\n"
    message += f"• التحميلات اليوم: {stats['downloads_today']}\n"
    message += f"• التقييم العام: {stats['avg_rating']:.1f}/5.0\n\n"
    
    if stats['alerts']:
        message += "⚠️ **يحتاج انتباه:**\n"
        for alert in stats['alerts']:
            message += f"• {alert}\n"
        message += "\n"
    
    if stats['top_today']:
        message += "🔥 **الأكثر نشاطاً اليوم:**\n"
        for i, product in enumerate(stats['top_today'][:2], 1):
            message += f"{i}. {product['title']} ({product['downloads_today']} تحميل)\n"
        message += "\n"
    
    message += f"🕐 آخر تحديث: منذ {stats['last_update']}"
    
    buttons = [
        [Button.inline("📦 إدارة المنتجات", b"admin_mp_products:all:0"),
         Button.inline("👥 إدارة المستخدمين", b"admin_mp_users:all:0")],
        [Button.inline("📊 الإحصائيات", b"admin_mp_stats_overview"),
         Button.inline("📂 التصنيفات", b"admin_mp_categories")],
        [Button.inline("🚨 تقارير الإساءة", b"admin_mp_reports:pending:0"),
         Button.inline("🔍 بحث متقدم", b"admin_mp_search")],
        [Button.inline("📝 سجل الإجراءات", b"admin_mp_logs:0"),
         Button.inline("⚙️ الإعدادات", b"admin_mp_settings")],
        [Button.inline("🔙 رجوع للوحة الإدارة", b"admin_panel")]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def get_admin_overview_stats() -> dict:
    """Get overview statistics for admin dashboard."""
    import time
    
    # Get basic counts
    total_products = await database.count_marketplace_products(status='active')
    
    # Get user counts
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        # Total marketplace users (users who have products)
        async with db.execute('SELECT COUNT(DISTINCT owner_id) FROM marketplace_products') as cursor:
            result = await cursor.fetchone()
            total_users = result[0] if result else 0
        
        # Banned users
        async with db.execute('''
            SELECT COUNT(*) FROM marketplace_bans 
            WHERE banned_until > ?
        ''', (int(time.time()),)) as cursor:
            result = await cursor.fetchone()
            banned_users = result[0] if result else 0
        
        # Downloads today
        today_start = int(time.time()) - (24 * 60 * 60)
        async with db.execute('''
            SELECT COUNT(*) FROM marketplace_downloads 
            WHERE downloaded_at > ?
        ''', (today_start,)) as cursor:
            result = await cursor.fetchone()
            downloads_today = result[0] if result else 0
        
        # Average rating
        async with db.execute('''
            SELECT AVG(CASE WHEN rating = 2 THEN 5.0 WHEN rating = 1 THEN 1.0 ELSE 3.0 END) 
            FROM marketplace_reviews
        ''') as cursor:
            result = await cursor.fetchone()
            avg_rating = result[0] if result and result[0] else 0.0
        
        # Alerts
        alerts = []
        
        # Pending reports
        async with db.execute('''
            SELECT COUNT(*) FROM marketplace_reports WHERE status = 'pending'
        ''') as cursor:
            result = await cursor.fetchone()
            pending_reports = result[0] if result else 0
            if pending_reports > 0:
                alerts.append(f"{pending_reports} تقارير إساءة جديدة")
        
        # Users with 3 warnings
        async with db.execute('''
            SELECT COUNT(*) FROM marketplace_warnings WHERE warning_count >= 3
        ''') as cursor:
            result = await cursor.fetchone()
            warned_users = result[0] if result else 0
            if warned_users > 0:
                alerts.append(f"{warned_users} مستخدمين تجاوزوا التحذيرات")
        
        # Top products today
        async with db.execute('''
            SELECT p.product_id, p.title, COUNT(d.id) as downloads_today
            FROM marketplace_products p
            LEFT JOIN marketplace_downloads d ON p.product_id = d.product_id 
                AND d.downloaded_at > ?
            WHERE p.status = 'active'
            GROUP BY p.product_id
            ORDER BY downloads_today DESC
            LIMIT 2
        ''', (today_start,)) as cursor:
            top_today = []
            async for row in cursor:
                top_today.append({
                    'product_id': row[0],
                    'title': row[1],
                    'downloads_today': row[2]
                })
    
    return {
        'total_products': total_products,
        'total_users': total_users,
        'banned_users': banned_users,
        'downloads_today': downloads_today,
        'avg_rating': avg_rating,
        'alerts': alerts,
        'top_today': top_today,
        'last_update': 'دقائق'
    }


print("✅ Marketplace admin panel loaded.")
