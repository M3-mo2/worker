# bot/handlers/admin/marketplace_categories.py
# Category management

from telethon import events, Button
from bot.core import database
from bot.handlers.admin.marketplace_admin import require_marketplace_admin

def setup(client):
    client.add_event_handler(categories_list_handler, events.CallbackQuery(pattern=b"admin_mp_categories"))
    client.add_event_handler(category_detail_handler, events.CallbackQuery(pattern=rb"admin_mp_cat_detail:.+"))


async def categories_list_handler(event):
    """List all categories."""
    if not await require_marketplace_admin(event):
        return
    
    categories = await database.get_marketplace_categories()
    
    message = f"📂 **إدارة التصنيفات**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if not categories:
        message += "لا توجد تصنيفات."
    else:
        for i, cat in enumerate(categories, 1):
            message += f"{i}. {cat['icon']} **{cat['name_ar']}** ({cat['product_count']} منتج)\n"
    
    buttons = []
    for cat in categories:
        buttons.append([Button.inline(f"✏️ {cat['name_ar']}", f"admin_mp_cat_detail:{cat['category_id']}".encode())])
    
    buttons.append([Button.inline("🔙 رجوع", b"admin_marketplace_home")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def category_detail_handler(event):
    """Show category details."""
    if not await require_marketplace_admin(event):
        return
    
    category_id = event.data.decode().split(':')[1]
    
    category = await database.get_marketplace_category(category_id)
    if not category:
        return await event.answer("❌ التصنيف غير موجود", alert=True)
    
    message = f"📂 **تفاصيل التصنيف**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"الاسم بالعربية: {category['name_ar']}\n"
    message += f"الاسم بالإنجليزية: {category['name_en']}\n"
    message += f"الأيقونة: {category['icon']}\n"
    message += f"الوصف: {category['description'] or 'لا يوجد'}\n"
    message += f"الترتيب: {category['display_order']}\n\n"
    message += f"عدد المنتجات: {category['product_count']}"
    
    buttons = [
        [Button.inline("📦 عرض المنتجات", f"admin_mp_products:all:0".encode())],
        [Button.inline("🔙 رجوع", b"admin_mp_categories")]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


print("✅ Marketplace categories admin loaded.")
