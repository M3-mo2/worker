# bot/handlers/top_developers.py
# Handler for top developers leaderboard

from telethon import events, Button
from bot.core import database
from bot.services.user_service import check_user_status
from bot.core.client import client

async def show_top_developers_handler(event):
    """Show top developers leaderboard."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Get top 10 developers
    top_devs = await get_top_developers_leaderboard(10)
    
    message = "🏆 **أفضل المطورين**\n\n"
    message += "أفضل 3 مطورين يحصلون على 👑 **PRO مجاني**!\n\n"
    message += "📊 **الترتيب حسب:** التحميلات + التقييمات + المشاهدات\n\n"
    
    if not top_devs:
        message += "لا يوجد مطورين بعد. كن أول من يرفع منتج!"
    else:
        for i, dev in enumerate(top_devs, 1):
            rank_emoji = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
            pro_badge = " 👑" if i <= 3 else ""
            
            message += f"{rank_emoji} [{dev['name']}](tg://user?id={dev['owner_id']}){pro_badge}\n"
            message += f"   📦 {dev['products']} منتج | "
            message += f"📥 {dev['downloads']:,} تحميل\n\n"
    
    # Show user's rank if not in top 10
    user_rank = await get_user_rank(sender_id)
    if user_rank and user_rank > 10:
        user_stats = await get_user_marketplace_stats(sender_id)
        message += f"━━━━━━━━━━━━━━━━\n"
        message += f"📍 **ترتيبك:** #{user_rank}\n"
        message += f"📦 {user_stats['products']} منتج | "
        message += f"📥 {user_stats['downloads']:,} تحميل\n\n"
        
        # Calculate gap to top 3
        if user_rank > 3:
            gap = await get_gap_to_rank(sender_id, 3)
            if gap:
                message += f"💡 **للوصول لـ Top 3:** تحتاج ~{gap:,} تحميل إضافي\n"
    
    message += f"\n**⬢ Build Market v1.0 ⌁ @M3_mo2 & @u_w_ll**"
    
    buttons = [
        [Button.inline("🔄 تحديث", b"show_top_developers")],
        [Button.inline("📤 رفع منتج", b"mp_upload_start")],
        [Button.inline("🔙 رجوع", b"marketplace_home")]
    ]
    
    try:
        await event.edit(message, buttons=buttons, parse_mode='md')
    except:
        await event.respond(message, buttons=buttons, parse_mode='md')


async def get_top_developers_leaderboard(limit: int) -> list:
    """Get top developers for leaderboard using same algorithm as PRO granting."""
    import aiosqlite
    from bot.services.ranking_engine import WEIGHTS, MIN_RATINGS_FOR_RANKING, DEFAULT_RATING_PERCENTAGE, DISLIKE_WEIGHT
    
    # Use same weights as top_developers_checker
    weights = WEIGHTS['balanced']
    
    async with aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        
        # Use SAME query as get_top_3_developers() for consistency
        query = f'''
            SELECT 
                p.owner_id,
                COUNT(DISTINCT p.product_id) as products,
                SUM(p.downloads) as downloads,
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
                ) as quality_score
            FROM marketplace_products p
            WHERE p.status = 'active'
            GROUP BY p.owner_id
            ORDER BY quality_score DESC
            LIMIT ?
        '''
        
        async with db.execute(query, (limit,)) as cursor:
            developers = []
            async for row in cursor:
                dev = dict(row)
                # Get name properly
                try:
                    user = await client.get_entity(int(dev['owner_id']))
                    dev['name'] = user.first_name or f"مطور #{dev['owner_id']}"
                except Exception as e:
                    print(f"Failed to get name for {dev['owner_id']}: {e}")
                    dev['name'] = f"مطور #{dev['owner_id']}"
                developers.append(dev)
            return developers


async def get_user_rank(user_id: int) -> int:
    """Get user's rank in leaderboard using same algorithm."""
    import aiosqlite
    from bot.services.ranking_engine import WEIGHTS, MIN_RATINGS_FOR_RANKING, DEFAULT_RATING_PERCENTAGE, DISLIKE_WEIGHT
    
    weights = WEIGHTS['balanced']
    
    async with aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        # Use same quality_score calculation
        query = f'''
            WITH ranked_developers AS (
                SELECT 
                    owner_id,
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
                    ROW_NUMBER() OVER (ORDER BY SUM(
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
                    ) DESC) as rank
                FROM marketplace_products p
                WHERE status = 'active'
                GROUP BY owner_id
            )
            SELECT rank FROM ranked_developers WHERE owner_id = ?
        '''
        async with db.execute(query, (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None


async def get_user_marketplace_stats(user_id: int) -> dict:
    """Get user's marketplace statistics."""
    import aiosqlite
    
    async with aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = aiosqlite.Row
        
        async with db.execute('''
            SELECT 
                COUNT(DISTINCT product_id) as products,
                SUM(downloads) as downloads
            FROM marketplace_products
            WHERE owner_id = ? AND status = 'active'
        ''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else {'products': 0, 'downloads': 0}


async def get_gap_to_rank(user_id: int, target_rank: int) -> int:
    """Calculate quality score gap to reach target rank."""
    import aiosqlite
    from bot.services.ranking_engine import WEIGHTS, MIN_RATINGS_FOR_RANKING, DEFAULT_RATING_PERCENTAGE, DISLIKE_WEIGHT
    
    weights = WEIGHTS['balanced']
    
    async with aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        # Calculate quality score for each developer
        score_query = f'''
            SELECT 
                owner_id,
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
                ) as quality_score
            FROM marketplace_products p
            WHERE status = 'active'
            GROUP BY owner_id
            ORDER BY quality_score DESC
        '''
        
        # Get target rank score
        async with db.execute(f"{score_query} LIMIT 1 OFFSET ?", (target_rank - 1,)) as cursor:
            target_row = await cursor.fetchone()
            target_score = target_row[1] if target_row else 0
        
        # Get user score
        async with db.execute(f'''
            SELECT SUM(
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
            ) as quality_score
            FROM marketplace_products p
            WHERE owner_id = ? AND status = 'active'
        ''', (user_id,)) as cursor:
            user_row = await cursor.fetchone()
            user_score = user_row[0] if user_row and user_row[0] else 0
        
        gap = target_score - user_score
        # Convert score gap to approximate downloads needed
        downloads_gap = int(gap / weights['downloads']) if weights['downloads'] > 0 else 0
        return downloads_gap if downloads_gap > 0 else 0


def setup(client_instance):
    """Register top developers handlers."""
    client_instance.on(events.CallbackQuery(pattern=b"show_top_developers"))(show_top_developers_handler)
    print("✅ Top Developers handlers registered.")
