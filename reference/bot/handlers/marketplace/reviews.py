# bot/handlers/marketplace/reviews.py
# Reviews and comments system

from telethon import events, Button
from bot.core import database
from bot.core.state import conversation_manager
from bot.services import marketplace_service
from bot.services.user_service import check_user_status

STATE_COMMENT_PRODUCT = "mp_comment_product"


def setup(client):
    client.add_event_handler(review_handler, events.CallbackQuery(pattern=rb"mp_review:"))
    client.add_event_handler(comments_handler, events.CallbackQuery(pattern=rb"mp_comments:.+"))
    client.add_event_handler(add_comment_start_handler, events.CallbackQuery(pattern=rb"mp_add_comment:"))
    client.add_event_handler(comment_text_handler, events.NewMessage())


async def review_handler(event):
    """Add or update review (Like/Dislike)."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse data: mp_review:product_id:rating
    data = event.data.decode().split(':')
    product_id = data[1]
    rating = int(data[2])  # 1 = dislike, 2 = like
    
    # Get product
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    # Check if user is owner
    if product['owner_id'] == sender_id:
        return await event.answer("❌ لا يمكنك تقييم منتجك الخاص", alert=True)
    
    # Add/update review
    await database.add_product_review(product_id, sender_id, rating)
    
    # Show success message
    rating_text = "👍 أعجبني" if rating == 2 else "👎 لم يعجبني"
    await event.answer(f"✅ تم تسجيل تقييمك: {rating_text}", alert=True)
    
    # Refresh product details
    await event.edit(
        await marketplace_service.format_product_details(product, sender_id),
        buttons=await get_product_buttons(product_id, sender_id),
        parse_mode='md'
    )


async def comments_handler(event):
    """Show product comments."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse data: mp_comments:product_id:page
    data = event.data.decode().split(':')
    product_id = data[1]
    page = int(data[2]) if len(data) > 2 else 0
    
    # Get product
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    # Get total comments count
    total_comments = await database.count_product_comments(product_id)
    
    # Pagination
    COMMENTS_PER_PAGE = 5
    offset = page * COMMENTS_PER_PAGE
    
    # Get comments for this page
    all_comments = await database.get_product_comments(product_id, limit=1000)
    comments = all_comments[offset:offset + COMMENTS_PER_PAGE]
    
    total_pages = (total_comments + COMMENTS_PER_PAGE - 1) // COMMENTS_PER_PAGE
    
    message = f"💬 **التعليقات** - {product['title']}\n\n"
    message += f"إجمالي التعليقات: {total_comments}\n"
    
    if page > 0:
        message += f"الصفحة {page + 1} من {total_pages}\n"
    
    message += "\n"
    
    if not comments:
        message += "لا توجد تعليقات بعد. كن أول من يعلق!"
    else:
        # Build message with entities for mentions
        from bot.core.client import client
        
        for comment in comments:
            user_id = comment['user_id']
            time_ago = marketplace_service.format_time_ago(comment['created_at'])
            
            # Get user info
            try:
                user = await client.get_entity(user_id)
                user_name = user.first_name or "مستخدم"
            except:
                user_name = "مستخدم"
            
            # Add to message with inline mention
            message += f"👤 [{user_name}](tg://user?id={user_id})\n"
            message += f"📅 {time_ago}\n"
            message += f"{comment['comment']}\n\n"
            message += "─────────────\n\n"
    
    buttons = []
    
    # Pagination buttons
    if total_pages > 1:
        nav_row = []
        if page > 0:
            nav_row.append(Button.inline("◀️", f"mp_comments:{product_id}:{page-1}".encode()))
        if page < total_pages - 1:
            nav_row.append(Button.inline("▶️", f"mp_comments:{product_id}:{page+1}".encode()))
        if nav_row:
            buttons.append(nav_row)
    
    buttons.append([Button.inline("✍️ كتابة تعليق جديد", f"mp_add_comment:{product_id}".encode())])
    buttons.append([Button.inline("🔙 رجوع للمنتج", f"mp_view:{product_id}".encode())])
    
    await event.edit(message, buttons=buttons, parse_mode='md', link_preview=False)


async def add_comment_start_handler(event):
    """Start adding a comment."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Parse product_id
    product_id = event.data.decode().split(':')[1]
    
    # Set state
    conversation_manager.set_value(sender_id, STATE_COMMENT_PRODUCT, product_id)
    
    message = "💬 **كتابة تعليق**\n\n"
    message += "شارك تجربتك مع المنتج:\n"
    message += "(الحد الأقصى: 500 حرف)\n\n"
    message += "أرسل تعليقك الآن:"
    
    buttons = [[Button.inline("❌ إلغاء", f"mp_comments:{product_id}:0".encode())]]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def comment_text_handler(event):
    """Handle comment text input."""
    sender_id = event.sender_id
    
    # Check if in comment state
    product_id = conversation_manager.get_value(sender_id, STATE_COMMENT_PRODUCT)
    if not product_id:
        return  # Not in comment mode
    
    text = event.text.strip()
    
    # Validate length
    if len(text) < 3:
        return await event.reply("❌ التعليق قصير جداً (3 أحرف على الأقل)")
    if len(text) > 500:
        return await event.reply("❌ التعليق طويل جداً (500 حرف كحد أقصى)")
    
    # Check profanity
    from bot.services.profanity_filter import check_profanity, check_user_ban
    
    is_banned, ban_reason = await check_user_ban(sender_id, 'comment')
    if is_banned:
        conversation_manager.clear_value(sender_id, STATE_COMMENT_PRODUCT)
        return await event.reply(ban_reason)
    
    is_clean, reason, severity = await check_profanity(text, sender_id)
    if not is_clean:
        if severity == 3:  # Critical - permanent ban
            conversation_manager.clear_value(sender_id, STATE_COMMENT_PRODUCT)
        return await event.reply(reason)
    
    # Check user's comment count on this product
    all_comments = await database.get_product_comments(product_id, limit=1000)
    user_comments = [c for c in all_comments if c['user_id'] == sender_id]
    
    if len(user_comments) >= 3:
        conversation_manager.clear_value(sender_id, STATE_COMMENT_PRODUCT)
        return await event.reply("❌ وصلت للحد الأقصى (3 تعليقات لكل منتج)")
    
    # Add comment
    await database.add_product_comment(product_id, sender_id, text)
    
    # Clear state
    conversation_manager.clear_value(sender_id, STATE_COMMENT_PRODUCT)
    
    # Show success
    message = "✅ **تم إضافة تعليقك بنجاح**\n\nشكراً لمشاركتك 🙏"
    buttons = [[Button.inline("💬 عرض التعليقات", f"mp_comments:{product_id}:0".encode())]]
    
    await event.reply(message, buttons=buttons, parse_mode='md')


async def get_product_buttons(product_id: str, user_id: int):
    """Helper to get product detail buttons."""
    from urllib.parse import quote
    from bot.core.client import client
    
    product = await database.get_marketplace_product(product_id)
    user_review = await database.get_user_review(product_id, user_id)
    
    buttons = [
        [Button.inline("📥 تحميل الآن", f"mp_download:{product_id}".encode())],
    ]
    
    # Review buttons
    if user_review:
        if user_review['rating'] == 2:
            buttons.append([Button.inline("👍 أعجبني ✓", f"mp_review:{product_id}:2".encode())])
        else:
            buttons.append([Button.inline("👍 أعجبني", f"mp_review:{product_id}:2".encode())])
        
        if user_review['rating'] == 1:
            buttons.append([Button.inline("👎 لم يعجبني ✓", f"mp_review:{product_id}:1".encode())])
        else:
            buttons.append([Button.inline("👎 لم يعجبني", f"mp_review:{product_id}:1".encode())])
    else:
        buttons.append([
            Button.inline("👍 أعجبني", f"mp_review:{product_id}:2".encode()),
            Button.inline("👎 لم يعجبني", f"mp_review:{product_id}:1".encode())
        ])
    
    comment_count = await database.count_product_comments(product_id)
    buttons.append([Button.inline(f"💬 التعليقات ({comment_count})", f"mp_comments:{product_id}:0".encode())])
    
    # Share button
    bot_username = (await client.get_me()).username
    product_url = f"https://t.me/{bot_username}?start=mp_{product_id}"
    share_text = f"شاهد هذا المنتج: {product['title']}"
    share_url = f"https://t.me/share/url?url={quote(product_url)}&text={quote(share_text)}"
    buttons.append([Button.url("📤 مشاركة المنتج", share_url)])
    
    if product['owner_id'] == user_id:
        buttons.append([Button.inline("⚙️ إدارة المنتج", f"mp_manage:{product_id}".encode())])
    
    buttons.append([Button.inline("🔙 رجوع", b"marketplace_home")])
    
    return buttons


print("✅ Marketplace reviews handlers loaded.")
