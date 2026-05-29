# bot/tasks/top_developers_checker.py
# Background task to automatically grant PRO to top 3 marketplace developers

import asyncio
import time
from typing import List, Dict, Optional
from bot.core.client import client
from bot.core.database import DB_NAME
from bot.core.config import settings
from bot.services.billing_service import grant_top_developer_pro, revoke_top_developer_pro
from bot.services.ranking_engine import WEIGHTS, MIN_RATINGS_FOR_RANKING, DEFAULT_RATING_PERCENTAGE, DISLIKE_WEIGHT
import aiosqlite

# Constants
CHECK_INTERVAL = 6 * 60 * 60  # 6 hours
MIN_PRODUCTS = 1  # Minimum products to qualify (at least 1 product)
MIN_RATING = 0  # Minimum rating percentage (0% = no minimum)
WARNING_THRESHOLD = 50  # Downloads difference to send warning
# Helper for quiet logging unless in DEV_MODE
def log(msg):
    if getattr(settings, 'DEV_MODE', False):
        print(msg)

async def get_top_3_developers() -> List[Dict]:
    """Get current top 3 developers using marketplace ranking algorithm."""
    log(f"[TopDev] Checking with MIN_PRODUCTS={MIN_PRODUCTS}, MIN_RATING={MIN_RATING}")
    
    # Use balanced weights from ranking engine
    weights = WEIGHTS['balanced']
    
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        
        # Calculate quality score for each developer (sum of all their products)
        query = f'''
            SELECT 
                p.owner_id,
                COUNT(DISTINCT p.product_id) as products,
                SUM(p.downloads) as total_downloads,
                SUM(p.views) as total_views,
                SUM(
                    (p.downloads * {weights['downloads']}) +
                    (CASE 
                        WHEN (SELECT COUNT(*) FROM marketplace_reviews r WHERE r.product_id = p.product_id) >= {MIN_RATINGS_FOR_RANKING} THEN
                            ((SELECT CAST(COUNT(CASE WHEN rating = 2 THEN 1 END) AS FLOAT) FROM marketplace_reviews r WHERE r.product_id = p.product_id) / 
                             ((SELECT COUNT(CASE WHEN rating = 2 THEN 1 END) FROM marketplace_reviews r WHERE r.product_id = p.product_id) + 
                              ((SELECT COUNT(CASE WHEN rating = 1 THEN 1 END) FROM marketplace_reviews r WHERE r.product_id = p.product_id) * {DISLIKE_WEIGHT})) * 100 * {weights['rating']})
                        ELSE ({DEFAULT_RATING_PERCENTAGE} * {weights['rating']})
                    END) +
                    (p.views * {weights['views']}) +
                    ((SELECT COUNT(*) FROM marketplace_reviews r WHERE r.product_id = p.product_id AND r.comment IS NOT NULL) * {weights['comments']})
                ) as quality_score,
                COALESCE(
                    (
                        SELECT 
                            CASE 
                                WHEN COUNT(*) > 0 
                                THEN (SUM(CASE WHEN rating = 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*))
                                ELSE 0
                            END
                        FROM marketplace_reviews r
                        WHERE r.product_id IN (
                            SELECT product_id FROM marketplace_products WHERE owner_id = p.owner_id
                        )
                    ), 0
                ) as rating_percentage
            FROM marketplace_products p
            WHERE p.status = 'active'
            GROUP BY p.owner_id
            HAVING products >= ? AND rating_percentage >= ?
            ORDER BY quality_score DESC
            LIMIT 3
        '''
        
        async with db.execute(query, (MIN_PRODUCTS, MIN_RATING)) as cursor:
            developers = []
            async for row in cursor:
                dev = dict(row)
                log(f"[TopDev] Found: ID={dev['owner_id']}, products={dev['products']}, downloads={dev['total_downloads']}, quality_score={dev['quality_score']:.2f}")
                # Get developer name properly
                try:
                    user = await client.get_entity(int(dev['owner_id']))
                    dev['name'] = user.first_name or f"مطور #{dev['owner_id']}"
                    log(f"[TopDev] Name: {dev['name']}")
                except Exception as e:
                    log(f"[TopDev] Failed to get name for {dev['owner_id']}: {e}")
                    dev['name'] = f"مطور #{dev['owner_id']}"
                developers.append(dev)
            
            log(f"[TopDev] Total found: {len(developers)}")
            return developers


async def get_previous_top_3() -> List[Dict]:
    """Get previous top 3 from database."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        
        async with db.execute('''
            SELECT user_id, rank, downloads, products, rating_percentage, granted_at
            FROM top_developers
            WHERE is_active = 1
            ORDER BY rank ASC
        ''') as cursor:
            return [dict(row) async for row in cursor]


async def save_top_developers(developers: List[Dict]):
    """Save current top 3 to database."""
    now = int(time.time())
    
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        # Deactivate all previous
        await db.execute('UPDATE top_developers SET is_active = 0')
        
        # Insert/update current top 3
        for rank, dev in enumerate(developers, 1):
            await db.execute('''
                INSERT OR REPLACE INTO top_developers 
                (user_id, rank, downloads, products, rating_percentage, granted_at, is_active, last_checked)
                VALUES (?, ?, ?, ?, ?, ?, 1, ?)
            ''', (dev['owner_id'], rank, dev.get('total_downloads', 0), dev['products'], 
                  dev.get('rating_percentage', 0), now, now))
        
        await db.commit()


async def log_history(user_id: int, rank: int, downloads: int, products: int, 
                      rating: float, event_type: str):
    """Log event to history table."""
    now = int(time.time())
    
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        await db.execute('''
            INSERT INTO top_developers_history 
            (user_id, rank, downloads, products, rating_percentage, recorded_at, event_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, rank, downloads, products, rating, now, event_type))
        await db.commit()


async def send_promotion_message(user_id: int, rank: int, stats: Dict):
    """Send promotion message to new top 3 developer."""
    rank_emojis = {1: "🥇", 2: "🥈", 3: "🥉"}
    rank_emoji = rank_emojis.get(rank, "🏆")
    
    message = f"""
🎉 **مبروك! وصلت لـ Top 3!** 🎉

━━━━━━━━━━━━━━━━━━━━━━━

{rank_emoji} **ترتيبك الجديد:** #{rank}

🎁 **تم منحك PRO مجاني!**

📊 **إحصائياتك:**
• المنتجات: {stats['products']}
• التحميلات: {stats.get('total_downloads', 0):,}
• التقييم: {stats.get('rating_percentage', 0):.1f}%

✨ **مميزات PRO:**
• محرر الأكواد المتقدم
• سجلات الويبهوك
• تشغيل تجريبي
• أولوية في الدعم

💡 **حافظ على ترتيبك:**
• ارفع منتجات جديدة
• حسّن جودة منتجاتك
• تفاعل مع المستخدمين

👑 **أنت الآن من نخبة المطورين!**

⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll
"""
    
    from telethon.tl.custom import Button
    buttons = [
        [Button.inline("📦 منتجاتي", b"mp_my_products:0")],
        [Button.inline("🏆 أفضل المطورين", b"show_top_developers")]
    ]
    
    try:
        await client.send_message(user_id, message, buttons=buttons, parse_mode='md')
    except Exception as e:
        log(f"[TopDev] Failed to send promotion message to {user_id}: {e}")


async def send_demotion_message(user_id: int, old_rank: int, new_rank: Optional[int], stats: Dict):
    """Send demotion message to developer who left top 3."""
    rank_emojis = {1: "🥇", 2: "🥈", 3: "🥉"}
    old_emoji = rank_emojis.get(old_rank, "🏆")
    
    message = f"""
📉 **تحديث ترتيبك**

━━━━━━━━━━━━━━━━━━━━━━━

الترتيب السابق: #{old_rank} {old_emoji}
الترتيب الحالي: #{new_rank if new_rank else '4+'}

⚠️ **تم إيقاف PRO المجاني**

لقد خرجت من Top 3، لذلك تم تحويلك للباقة المجانية.

📊 **إحصائياتك الحالية:**
• المنتجات: {stats['products']}
• التحميلات: {stats.get('total_downloads', 0):,}
• التقييم: {stats.get('rating_percentage', 0):.1f}%

💪 **كيف تعود لـ Top 3؟**

1. **ارفع منتجات جديدة**
   منتجات أكثر = تحميلات أكثر

2. **حسّن منتجاتك الحالية**
   استمع لتعليقات المستخدمين

3. **روّج لمنتجاتك**
   شارك روابط منتجاتك

4. **حافظ على الجودة**
   منتجات عالية الجودة = تقييمات أفضل

💡 **نصيحة:** المنافسة مستمرة، لا تستسلم!

⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll
"""
    
    from telethon.tl.custom import Button
    buttons = [
        [Button.inline("📤 رفع منتج جديد", b"mp_upload_start")],
        [Button.inline("🏆 أفضل المطورين", b"show_top_developers")],
        [Button.inline("💎 شراء PRO", b"billing_menu")]
    ]
    
    try:
        await client.send_message(user_id, message, buttons=buttons, parse_mode='md')
    except Exception as e:
        log(f"[TopDev] Failed to send demotion message to {user_id}: {e}")


async def send_rank_change_message(user_id: int, old_rank: int, new_rank: int, stats: Dict):
    """Send rank change message to developer still in top 3."""
    rank_emojis = {1: "🥇", 2: "🥈", 3: "🥉"}
    old_emoji = rank_emojis.get(old_rank, "🏆")
    new_emoji = rank_emojis.get(new_rank, "🏆")
    
    if new_rank < old_rank:
        emoji = "📈"
        text = "تحسن ترتيبك!"
        motivation = "💪 استمر في التحسين للوصول للمركز الأول!" if new_rank > 1 else "👑 أنت في المركز الأول! حافظ عليه!"
    else:
        emoji = "📉"
        text = "انخفض ترتيبك"
        motivation = "💪 اعمل أكثر للعودة لترتيبك السابق!"
    
    message = f"""
{emoji} **{text}**

━━━━━━━━━━━━━━━━━━━━━━━

{old_emoji} الترتيب السابق: #{old_rank}
{new_emoji} الترتيب الحالي: #{new_rank}

✅ **لا تزال في Top 3!**
PRO الخاص بك لا يزال نشطاً.

📊 **إحصائياتك:**
• المنتجات: {stats['products']}
• التحميلات: {stats.get('total_downloads', 0):,}
• التقييم: {stats.get('rating_percentage', 0):.1f}%

{motivation}

⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll
"""
    
    from telethon.tl.custom import Button
    buttons = [[Button.inline("🏆 أفضل المطورين", b"show_top_developers")]]
    
    try:
        await client.send_message(user_id, message, buttons=buttons, parse_mode='md')
    except Exception as e:
        log(f"[TopDev] Failed to send rank change message to {user_id}: {e}")


async def update_top_developers(current: List[Dict], previous: List[Dict]):
    """Compare and update top developers, send notifications."""
    log(f"[TopDev] Checking top developers...")
    
    # Format current and previous for logging
    current_str = ', '.join([f"{d['owner_id']}({d.get('total_downloads', 0)})" for d in current])
    previous_str = ', '.join([f"{d['user_id']}({d.get('downloads', 0)})" for d in previous])
    log(f"[TopDev] Current: [{current_str}]")
    log(f"[TopDev] Previous: [{previous_str}]")
    
    # Create maps for easy lookup
    current_map = {dev['owner_id']: (i+1, dev) for i, dev in enumerate(current)}
    previous_map = {dev['user_id']: (dev['rank'], dev) for dev in previous}
    
    # Check for promotions (new to top 3)
    for user_id, (rank, stats) in current_map.items():
        if user_id not in previous_map:
            # New developer in top 3
            log(f"[TopDev] 🎉 Promoting user {user_id} to rank {rank}")
            grant_top_developer_pro(str(user_id), rank)
            await send_promotion_message(user_id, rank, stats)
            await log_history(user_id, rank, stats.get('total_downloads', 0), stats['products'], 
                            stats['rating_percentage'], 'promoted')
    
    # Check for demotions (left top 3)
    for user_id, (old_rank, old_stats) in previous_map.items():
        if user_id not in current_map:
            # Developer left top 3
            log(f"[TopDev] 📉 Demoting user {user_id} from rank {old_rank}")
            revoke_top_developer_pro(str(user_id))
            
            # Get current stats
            current_stats = await get_developer_stats(user_id)
            await send_demotion_message(user_id, old_rank, None, current_stats)
            await log_history(user_id, old_rank, current_stats.get('total_downloads', 0), 
                            current_stats['products'], current_stats['rating_percentage'], 'demoted')
    
    # Check for rank changes (still in top 3)
    for user_id, (new_rank, stats) in current_map.items():
        if user_id in previous_map:
            old_rank = previous_map[user_id][0]
            if old_rank != new_rank:
                # Rank changed
                log(f"[TopDev] 📊 User {user_id} rank changed: {old_rank} -> {new_rank}")
                grant_top_developer_pro(str(user_id), new_rank)  # Update rank
                await send_rank_change_message(user_id, old_rank, new_rank, stats)
                await log_history(user_id, new_rank, stats.get('total_downloads', 0), stats['products'], 
                                stats['rating_percentage'], 'rank_changed')
            else:
                # No rank change - check if they have PRO
                from bot.core.data_manager import load_all_users
                all_users = load_all_users()
                user_data = all_users.get(str(user_id), {})
                
                has_pro = user_data.get('plan') == 'pro'
                is_top_dev_pro = user_data.get('plan_source') == 'top_developer'
                
                if not has_pro or not is_top_dev_pro:
                    # They're in top 3 but don't have PRO! Grant it now
                    log(f"[TopDev] 🎁 User {user_id} is rank {new_rank} but missing PRO - granting now")
                    grant_top_developer_pro(str(user_id), new_rank)
                    await send_promotion_message(user_id, new_rank, stats)
                    await log_history(user_id, new_rank, stats.get('total_downloads', 0), stats['products'], 
                                    stats['rating_percentage'], 'promoted')
                else:
                    # All good, just refresh
                    log(f"[TopDev] ✅ User {user_id} still at rank {new_rank}")
                    grant_top_developer_pro(str(user_id), new_rank)  # Refresh PRO
    
    # Save current top 3
    await save_top_developers(current)
    log(f"[TopDev] ✅ Check complete. Top 3: {[dev['owner_id'] for dev in current]}")


async def get_developer_stats(user_id: int) -> Dict:
    """Get current stats for a developer."""
    async with aiosqlite.connect(DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        
        async with db.execute('''
            SELECT 
                COUNT(DISTINCT product_id) as products,
                SUM(downloads) as downloads,
                (
                    SELECT 
                        CASE 
                            WHEN COUNT(*) > 0 
                            THEN (SUM(CASE WHEN rating = 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*))
                            ELSE 50
                        END
                    FROM marketplace_reviews r
                    WHERE r.product_id IN (
                        SELECT product_id FROM marketplace_products WHERE owner_id = ?
                    )
                ) as rating_percentage
            FROM marketplace_products
            WHERE owner_id = ? AND status = 'active'
        ''', (user_id, user_id)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else {'products': 0, 'downloads': 0, 'rating_percentage': 0}


async def top_developers_checker_task():
    """Main background task - runs every 6 hours."""
    log("✅ Top Developers Checker task started")
    
    # Wait for bot to fully start
    await asyncio.sleep(60)
    
    # Run immediately on first start
    log("[TopDev] Running initial check...")
    try:
        current = await get_top_3_developers()
        previous = await get_previous_top_3()
        await update_top_developers(current, previous)
    except Exception as e:
        log(f"[TopDev] Error in initial check: {e}")
        import traceback
        if getattr(settings, 'DEV_MODE', False):
            traceback.print_exc()
    
    # Then run every 6 hours
    while True:
        await asyncio.sleep(CHECK_INTERVAL)
        
        try:
            current = await get_top_3_developers()
            previous = await get_previous_top_3()
            await update_top_developers(current, previous)
        except Exception as e:
            log(f"[TopDev] Error in checker task: {e}")
            import traceback
            if getattr(settings, 'DEV_MODE', False):
                traceback.print_exc()


# Smart trigger - runs on every download
_last_check_time = 0
_check_lock = asyncio.Lock()

async def trigger_top_developers_check():
    """
    Smart trigger that checks top developers when downloads happen.
    Prevents spam by limiting checks to once per minute.
    """
    global _last_check_time
    
    import time
    current_time = time.time()
    
    # Rate limit: max once per minute
    if current_time - _last_check_time < 60:
        return
    
    # Use lock to prevent concurrent checks
    if _check_lock.locked():
        return
    
    async with _check_lock:
        _last_check_time = current_time
        
        try:
            log("[TopDev] 🔔 Triggered check from download event")
            current = await get_top_3_developers()
            previous = await get_previous_top_3()
            await update_top_developers(current, previous)
        except Exception as e:
            log(f"[TopDev] Error in triggered check: {e}")


print("✅ Top Developers Checker module loaded")
