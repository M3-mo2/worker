# bot/handlers/admin/marketplace_users.py
# User management for marketplace admins

from telethon import events, Button
from bot.core import database
from bot.core.state import conversation_manager
from bot.handlers.admin.marketplace_admin import is_marketplace_admin, require_marketplace_admin
from bot.handlers.admin.marketplace_products import log_admin_action

STATE_ADMIN_MP_BAN_REASON = "admin_mp_ban_reason"

def setup(client):
    client.add_event_handler(users_list_handler, events.CallbackQuery(pattern=rb"admin_mp_users:.+"))
    client.add_event_handler(user_detail_handler, events.CallbackQuery(pattern=rb"admin_mp_user:\d+"))
    client.add_event_handler(ban_user_handler, events.CallbackQuery(pattern=rb"admin_mp_ban:\d+:.+"))
    client.add_event_handler(unban_user_handler, events.CallbackQuery(pattern=rb"admin_mp_unban:\d+"))
    client.add_event_handler(reset_warnings_handler, events.CallbackQuery(pattern=rb"admin_mp_reset_warn:\d+"))
    client.add_event_handler(ban_reason_handler, events.NewMessage())


async def users_list_handler(event):
    """List marketplace users with filters."""
    if not await require_marketplace_admin(event):
        return
    
    # Parse: admin_mp_users:filter:page
    data = event.data.decode().split(':')
    filter_type = data[1]
    page = int(data[2]) if len(data) > 2 else 0
    
    USERS_PER_PAGE = 6
    offset = page * USERS_PER_PAGE
    
    # Get users based on filter
    if filter_type == 'all':
        users, total = await get_all_marketplace_users(USERS_PER_PAGE, offset)
        title = "الكل"
    elif filter_type == 'active':
        users, total = await get_active_users(USERS_PER_PAGE, offset)
        title = "نشط"
    elif filter_type == 'banned':
        users, total = await get_banned_users(USERS_PER_PAGE, offset)
        title = "محظور"
    elif filter_type == 'warned':
        users, total = await get_warned_users(USERS_PER_PAGE, offset)
        title = "محذر"
    elif filter_type == 'top':
        users, total = await get_top_developers(USERS_PER_PAGE, offset)
        title = "الأفضل"
    else:
        users, total = await get_all_marketplace_users(USERS_PER_PAGE, offset)
        title = "الكل"
    
    total_pages = (total + USERS_PER_PAGE - 1) // USERS_PER_PAGE
    
    message = f"👥 **إدارة المستخدمين**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"الفلتر: {title} | الصفحة {page + 1} من {total_pages}\n\n"
    
    if not users:
        message += "لا يوجد مستخدمين."
    else:
        for i, user in enumerate(users, 1):
            # Get user name
            try:
                from bot.core.client import client
                user_entity = await client.get_entity(user['user_id'])
                user_name = user_entity.first_name or "مستخدم"
            except:
                user_name = "مستخدم"
            
            message += f"{i}️⃣ **{user_name}** (ID: {user['user_id']})\n"
            message += f"   📦 المنتجات: {user['product_count']}\n"
            message += f"   ⭐ التقييم: {user['avg_rating']:.1f}/5.0\n"
            message += f"   📥 التحميلات: {user['total_downloads']}\n"
            
            if user.get('warning_count', 0) > 0:
                message += f"   ⚠️ التحذيرات: {user['warning_count']}/3\n"
            
            if user.get('is_banned'):
                message += f"   🚫 محظور\n"
            
            message += "\n"
    
    # Filter buttons
    filter_buttons = []
    filters = [
        ('الكل', 'all'),
        ('نشط', 'active'),
        ('محظور', 'banned'),
        ('محذر', 'warned'),
        ('الأفضل', 'top')
    ]
    
    row = []
    for label, ftype in filters:
        if ftype == filter_type:
            row.append(Button.inline(f"● {label}", f"admin_mp_users:{ftype}:0".encode()))
        else:
            row.append(Button.inline(f"○ {label}", f"admin_mp_users:{ftype}:0".encode()))
        if len(row) == 3:
            filter_buttons.append(row)
            row = []
    if row:
        filter_buttons.append(row)
    
    # User buttons
    user_buttons = []
    for i, user in enumerate(users, 1):
        user_buttons.append([Button.inline(f"👤 #{i}", f"admin_mp_user:{user['user_id']}".encode())])
    
    # Navigation
    nav_row = []
    if page > 0:
        nav_row.append(Button.inline("◀️", f"admin_mp_users:{filter_type}:{page-1}".encode()))
    if page < total_pages - 1:
        nav_row.append(Button.inline("▶️", f"admin_mp_users:{filter_type}:{page+1}".encode()))
    
    buttons = filter_buttons + user_buttons
    if nav_row:
        buttons.append(nav_row)
    buttons.append([Button.inline("🔙 رجوع", b"admin_marketplace_home")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def user_detail_handler(event):
    """Show user details."""
    if not await require_marketplace_admin(event):
        return
    
    user_id = int(event.data.decode().split(':')[1])
    
    # Get user stats
    user_stats = await get_user_marketplace_stats(user_id)
    
    if not user_stats:
        return await event.answer("❌ المستخدم غير موجود", alert=True)
    
    # Get user name
    try:
        from bot.core.client import client
        user_entity = await client.get_entity(user_id)
        user_name = user_entity.first_name or "مستخدم"
    except:
        user_name = "مستخدم"
    
    message = f"👤 **ملف المستخدم**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"الاسم: [{user_name}](tg://user?id={user_id})\n"
    message += f"المعرف: {user_id}\n\n"
    
    message += f"📊 **الإحصائيات:**\n"
    message += f"• المنتجات: {user_stats['product_count']}\n"
    message += f"• التحميلات: {user_stats['total_downloads']}\n"
    message += f"• التقييم: {user_stats['avg_rating']:.1f}/5.0 ({user_stats['total_ratings']} تقييم)\n"
    message += f"• التعليقات: {user_stats['comment_count']}\n"
    message += f"• المراجعات: {user_stats['review_count']}\n\n"
    
    message += f"⚠️ **الحالة:**\n"
    message += f"• التحذيرات: {user_stats['warnings']}/3\n"
    
    if user_stats['is_banned']:
        import time
        days_left = (user_stats['banned_until'] - int(time.time())) // (24 * 60 * 60) + 1
        message += f"• الحظر: 🚫 محظور ({days_left} يوم متبقي)\n"
    else:
        message += f"• الحظر: ✅ غير محظور\n"
    
    message += "\n"
    
    if user_stats['recent_products']:
        message += f"📦 **آخر المنتجات:**\n"
        for product in user_stats['recent_products'][:3]:
            message += f"• {product['title']} ({product['downloads']} تحميل)\n"
        message += "\n"
    
    if user_stats['recent_comments']:
        message += f"💬 **آخر التعليقات:**\n"
        for comment in user_stats['recent_comments'][:2]:
            message += f"• \"{comment['text'][:30]}...\" على {comment['product_title']}\n"
    
    buttons = []
    
    if user_stats['is_banned']:
        buttons.append([Button.inline("✅ إلغاء الحظر", f"admin_mp_unban:{user_id}".encode())])
    else:
        buttons.append([
            Button.inline("🚫 حظر دائم", f"admin_mp_ban:{user_id}:permanent".encode()),
            Button.inline("⏰ حظر 3 أيام", f"admin_mp_ban:{user_id}:3d".encode())
        ])
        buttons.append([
            Button.inline("⏰ حظر 7 أيام", f"admin_mp_ban:{user_id}:7d".encode()),
            Button.inline("⏰ حظر 30 يوم", f"admin_mp_ban:{user_id}:30d".encode())
        ])
    
    if user_stats['warnings'] > 0:
        buttons.append([Button.inline("🔄 إعادة تعيين التحذيرات", f"admin_mp_reset_warn:{user_id}".encode())])
    
    buttons.append([
        Button.inline("📦 عرض المنتجات", f"admin_mp_user_products:{user_id}:0".encode()),
        Button.inline("💬 عرض التعليقات", f"admin_mp_user_comments:{user_id}:0".encode())
    ])
    
    buttons.append([Button.inline("🔙 رجوع", b"admin_mp_users:all:0")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def ban_user_handler(event):
    """Initiate user ban."""
    if not await require_marketplace_admin(event):
        return
    
    # Parse: admin_mp_ban:user_id:type
    data = event.data.decode().split(':')
    user_id = int(data[1])
    ban_type = data[2]
    
    # Get user name
    try:
        from bot.core.client import client
        user_entity = await client.get_entity(user_id)
        user_name = user_entity.first_name or "مستخدم"
    except:
        user_name = "مستخدم"
    
    ban_types = {
        'permanent': 'حظر دائم',
        '3d': 'حظر 3 أيام',
        '7d': 'حظر 7 أيام',
        '30d': 'حظر 30 يوم'
    }
    
    message = f"🚫 **حظر المستخدم**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"النوع: {ban_types.get(ban_type, ban_type)}\n"
    message += f"المستخدم: {user_name} ({user_id})\n\n"
    message += f"يرجى كتابة سبب الحظر:"
    
    # Set state
    conversation_manager.set_value(event.sender_id, STATE_ADMIN_MP_BAN_REASON, f"{user_id}:{ban_type}")
    
    buttons = [[Button.inline("🔙 إلغاء", f"admin_mp_user:{user_id}".encode())]]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def ban_reason_handler(event):
    """Handle ban reason input."""
    sender_id = event.sender_id
    
    if not is_marketplace_admin(sender_id):
        return
    
    ban_data = conversation_manager.get_value(sender_id, STATE_ADMIN_MP_BAN_REASON)
    if not ban_data:
        return
    
    reason = event.text.strip()
    
    if len(reason) < 5:
        return await event.reply("❌ السبب قصير جداً (5 أحرف على الأقل)")
    
    user_id, ban_type = ban_data.split(':')
    user_id = int(user_id)
    
    # Apply ban
    success = await apply_user_ban(user_id, ban_type, sender_id, reason)
    
    conversation_manager.clear_value(sender_id, STATE_ADMIN_MP_BAN_REASON)
    
    if success:
        # Notify user
        try:
            from bot.core.client import client
            ban_types = {
                'permanent': 'دائم',
                '3d': '3 أيام',
                '7d': '7 أيام',
                '30d': '30 يوم'
            }
            notify_msg = f"🚫 **تم حظرك من الماركت**\n\n"
            notify_msg += f"المدة: {ban_types.get(ban_type, ban_type)}\n"
            notify_msg += f"السبب: {reason}\n\n"
            notify_msg += f"إذا كان لديك استفسار، يرجى التواصل مع الإدارة."
            await client.send_message(user_id, notify_msg, parse_mode='md')
        except:
            pass
        
        await event.reply("✅ تم حظر المستخدم بنجاح وإرسال الإشعار")
    else:
        await event.reply("❌ حدث خطأ أثناء الحظر")


async def unban_user_handler(event):
    """Unban user."""
    if not await require_marketplace_admin(event):
        return
    
    user_id = int(event.data.decode().split(':')[1])
    
    success = await remove_user_ban(user_id, event.sender_id)
    
    if success:
        # Notify user
        try:
            from bot.core.client import client
            notify_msg = f"✅ **تم إلغاء حظرك من الماركت**\n\n"
            notify_msg += f"يمكنك الآن الوصول إلى الماركت مرة أخرى.\n"
            notify_msg += f"يرجى الالتزام بالقواعد."
            await client.send_message(user_id, notify_msg, parse_mode='md')
        except:
            pass
        
        await event.answer("✅ تم إلغاء حظر المستخدم", alert=True)
        
        # Log action
        await log_admin_action(event.sender_id, 'unban', 'user', str(user_id))
        
        # Refresh view
        await user_detail_handler(event)
    else:
        await event.answer("❌ حدث خطأ", alert=True)


async def reset_warnings_handler(event):
    """Reset user warnings."""
    if not await require_marketplace_admin(event):
        return
    
    user_id = int(event.data.decode().split(':')[1])
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        await db.execute('DELETE FROM marketplace_warnings WHERE user_id = ?', (user_id,))
        await db.commit()
    
    await event.answer("✅ تم إعادة تعيين التحذيرات", alert=True)
    
    # Log action
    await log_admin_action(event.sender_id, 'reset_warnings', 'user', str(user_id))
    
    # Refresh view
    await user_detail_handler(event)


# Helper functions

async def get_all_marketplace_users(limit: int, offset: int) -> tuple:
    """Get all marketplace users."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        # Get users with stats
        async with db.execute('''
            SELECT 
                p.owner_id as user_id,
                COUNT(DISTINCT p.product_id) as product_count,
                SUM(p.downloads) as total_downloads,
                AVG(CASE WHEN r.rating = 2 THEN 5.0 WHEN r.rating = 1 THEN 1.0 ELSE 3.0 END) as avg_rating,
                COALESCE(w.warning_count, 0) as warning_count
            FROM marketplace_products p
            LEFT JOIN marketplace_reviews r ON p.product_id = r.product_id
            LEFT JOIN marketplace_warnings w ON p.owner_id = w.user_id
            WHERE p.status = 'active'
            GROUP BY p.owner_id
            ORDER BY total_downloads DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset)) as cursor:
            users = [dict(row) async for row in cursor]
        
        # Get total count
        async with db.execute('''
            SELECT COUNT(DISTINCT owner_id) FROM marketplace_products WHERE status = 'active'
        ''') as cursor:
            result = await cursor.fetchone()
            total = result[0] if result else 0
        
        return users, total


async def get_active_users(limit: int, offset: int) -> tuple:
    """Get active users (not banned)."""
    import time
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        async with db.execute('''
            SELECT 
                p.owner_id as user_id,
                COUNT(DISTINCT p.product_id) as product_count,
                SUM(p.downloads) as total_downloads,
                AVG(CASE WHEN r.rating = 2 THEN 5.0 WHEN r.rating = 1 THEN 1.0 ELSE 3.0 END) as avg_rating,
                COALESCE(w.warning_count, 0) as warning_count
            FROM marketplace_products p
            LEFT JOIN marketplace_reviews r ON p.product_id = r.product_id
            LEFT JOIN marketplace_warnings w ON p.owner_id = w.user_id
            LEFT JOIN marketplace_bans b ON p.owner_id = b.user_id AND b.banned_until > ?
            WHERE p.status = 'active' AND b.user_id IS NULL
            GROUP BY p.owner_id
            ORDER BY total_downloads DESC
            LIMIT ? OFFSET ?
        ''', (int(time.time()), limit, offset)) as cursor:
            users = [dict(row) async for row in cursor]
        
        async with db.execute('''
            SELECT COUNT(DISTINCT p.owner_id)
            FROM marketplace_products p
            LEFT JOIN marketplace_bans b ON p.owner_id = b.user_id AND b.banned_until > ?
            WHERE p.status = 'active' AND b.user_id IS NULL
        ''', (int(time.time()),)) as cursor:
            result = await cursor.fetchone()
            total = result[0] if result else 0
        
        return users, total


async def get_banned_users(limit: int, offset: int) -> tuple:
    """Get banned users."""
    import time
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        async with db.execute('''
            SELECT 
                b.user_id,
                COUNT(DISTINCT p.product_id) as product_count,
                SUM(p.downloads) as total_downloads,
                0.0 as avg_rating,
                0 as warning_count,
                1 as is_banned
            FROM marketplace_bans b
            LEFT JOIN marketplace_products p ON b.user_id = p.owner_id
            WHERE b.banned_until > ?
            GROUP BY b.user_id
            LIMIT ? OFFSET ?
        ''', (int(time.time()), limit, offset)) as cursor:
            users = [dict(row) async for row in cursor]
        
        async with db.execute('''
            SELECT COUNT(*) FROM marketplace_bans WHERE banned_until > ?
        ''', (int(time.time()),)) as cursor:
            result = await cursor.fetchone()
            total = result[0] if result else 0
        
        return users, total


async def get_warned_users(limit: int, offset: int) -> tuple:
    """Get users with warnings."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        async with db.execute('''
            SELECT 
                w.user_id,
                COUNT(DISTINCT p.product_id) as product_count,
                SUM(p.downloads) as total_downloads,
                0.0 as avg_rating,
                w.warning_count
            FROM marketplace_warnings w
            LEFT JOIN marketplace_products p ON w.user_id = p.owner_id
            WHERE w.warning_count > 0
            GROUP BY w.user_id
            ORDER BY w.warning_count DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset)) as cursor:
            users = [dict(row) async for row in cursor]
        
        async with db.execute('''
            SELECT COUNT(*) FROM marketplace_warnings WHERE warning_count > 0
        ''') as cursor:
            result = await cursor.fetchone()
            total = result[0] if result else 0
        
        return users, total


async def get_top_developers(limit: int, offset: int) -> tuple:
    """Get top developers by downloads."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        async with db.execute('''
            SELECT 
                p.owner_id as user_id,
                COUNT(DISTINCT p.product_id) as product_count,
                SUM(p.downloads) as total_downloads,
                AVG(CASE WHEN r.rating = 2 THEN 5.0 WHEN r.rating = 1 THEN 1.0 ELSE 3.0 END) as avg_rating,
                COALESCE(w.warning_count, 0) as warning_count
            FROM marketplace_products p
            LEFT JOIN marketplace_reviews r ON p.product_id = r.product_id
            LEFT JOIN marketplace_warnings w ON p.owner_id = w.user_id
            WHERE p.status = 'active'
            GROUP BY p.owner_id
            ORDER BY total_downloads DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset)) as cursor:
            users = [dict(row) async for row in cursor]
        
        async with db.execute('''
            SELECT COUNT(DISTINCT owner_id) FROM marketplace_products WHERE status = 'active'
        ''') as cursor:
            result = await cursor.fetchone()
            total = result[0] if result else 0
        
        return users, total


async def get_user_marketplace_stats(user_id: int) -> dict:
    """Get detailed user stats."""
    import time
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        # Basic stats
        async with db.execute('''
            SELECT 
                COUNT(DISTINCT p.product_id) as product_count,
                SUM(p.downloads) as total_downloads,
                COUNT(DISTINCT c.comment_id) as comment_count,
                COUNT(DISTINCT r.product_id || r.user_id) as review_count
            FROM marketplace_products p
            LEFT JOIN marketplace_comments c ON p.owner_id = c.user_id
            LEFT JOIN marketplace_reviews r ON p.owner_id = r.user_id
            WHERE p.owner_id = ? AND p.status = 'active'
        ''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None
            stats = dict(row)
        
        # Average rating
        async with db.execute('''
            SELECT 
                AVG(CASE WHEN r.rating = 2 THEN 5.0 WHEN r.rating = 1 THEN 1.0 ELSE 3.0 END) as avg_rating,
                COUNT(*) as total_ratings
            FROM marketplace_reviews r
            INNER JOIN marketplace_products p ON r.product_id = p.product_id
            WHERE p.owner_id = ?
        ''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            stats['avg_rating'] = row[0] if row and row[0] else 0.0
            stats['total_ratings'] = row[1] if row else 0
        
        # Warnings
        async with db.execute('''
            SELECT warning_count FROM marketplace_warnings WHERE user_id = ?
        ''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            stats['warnings'] = row[0] if row else 0
        
        # Ban status
        async with db.execute('''
            SELECT banned_until FROM marketplace_bans WHERE user_id = ? AND banned_until > ?
        ''', (user_id, int(time.time()))) as cursor:
            row = await cursor.fetchone()
            stats['is_banned'] = row is not None
            stats['banned_until'] = row[0] if row else None
        
        # Recent products
        async with db.execute('''
            SELECT product_id, title, downloads
            FROM marketplace_products
            WHERE owner_id = ? AND status = 'active'
            ORDER BY created_at DESC
            LIMIT 3
        ''', (user_id,)) as cursor:
            stats['recent_products'] = [dict(row) async for row in cursor]
        
        # Recent comments
        async with db.execute('''
            SELECT c.comment as text, p.title as product_title
            FROM marketplace_comments c
            INNER JOIN marketplace_products p ON c.product_id = p.product_id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
            LIMIT 2
        ''', (user_id,)) as cursor:
            stats['recent_comments'] = [dict(row) async for row in cursor]
        
        return stats


async def apply_user_ban(user_id: int, ban_type: str, admin_id: int, reason: str) -> bool:
    """Apply ban to user."""
    import time
    
    try:
        # Calculate ban duration
        if ban_type == 'permanent':
            banned_until = int(time.time()) + (100 * 365 * 24 * 60 * 60)  # 100 years
            db_ban_type = 'permanent'
        elif ban_type == '3d':
            banned_until = int(time.time()) + (3 * 24 * 60 * 60)
            db_ban_type = 'comment_upload'
        elif ban_type == '7d':
            banned_until = int(time.time()) + (7 * 24 * 60 * 60)
            db_ban_type = 'comment_upload'
        elif ban_type == '30d':
            banned_until = int(time.time()) + (30 * 24 * 60 * 60)
            db_ban_type = 'comment_upload'
        else:
            return False
        
        async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
            await db.execute('''
                INSERT OR REPLACE INTO marketplace_bans 
                (user_id, ban_type, banned_until, reason, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, db_ban_type, banned_until, reason, int(time.time())))
            await db.commit()
        
        # Log action
        await log_admin_action(admin_id, f'ban_{ban_type}', 'user', str(user_id), reason)
        
        return True
    except Exception as e:
        print(f"Error banning user: {e}")
        return False


async def remove_user_ban(user_id: int, admin_id: int) -> bool:
    """Remove user ban."""
    try:
        async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
            await db.execute('DELETE FROM marketplace_bans WHERE user_id = ?', (user_id,))
            await db.commit()
        
        return True
    except Exception as e:
        print(f"Error unbanning user: {e}")
        return False


print("✅ Marketplace users admin loaded.")
