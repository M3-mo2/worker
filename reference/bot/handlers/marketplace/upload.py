# bot/handlers/marketplace/upload.py
# Upload new products to marketplace

import os
import tempfile
from telethon import events, Button
from bot.core import database
from bot.core.state import conversation_manager
from bot.services import marketplace_service
from bot.services.user_service import check_user_status, get_user_data

# Upload state keys
STATE_UPLOAD_STEP = "mp_upload_step"
STATE_UPLOAD_DATA = "mp_upload_data"
STATE_UPLOAD_TEMP = "mp_upload_temp"


def setup(client):
    client.add_event_handler(upload_start_handler, events.CallbackQuery(pattern=b"mp_upload_start"))
    client.add_event_handler(upload_category_handler, events.CallbackQuery(pattern=b"mp_upload_cat:"))
    client.add_event_handler(upload_confirm_handler, events.CallbackQuery(pattern=b"mp_upload_confirm"))
    client.add_event_handler(upload_cancel_handler, events.CallbackQuery(pattern=b"mp_upload_cancel"))
    client.add_event_handler(upload_text_handler, events.NewMessage())


async def upload_start_handler(event):
    """Start upload wizard - Step 1: Title."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Check user limits
    user_data = get_user_data(sender_id)
    user_plan = user_data.get('plan', 'free')
    
    user_products = await database.get_user_products(sender_id, status='active')
    max_products = 20 if user_plan == 'pro' else 3
    
    if len(user_products) >= max_products:
        return await event.answer(
            f"❌ وصلت للحد الأقصى ({max_products} منتجات)\n"
            f"احذف منتج قديم أو قم بالترقية لـ Pro",
            alert=True
        )
    
    # Initialize state
    conversation_manager.set_value(sender_id, STATE_UPLOAD_STEP, 1)
    conversation_manager.set_value(sender_id, STATE_UPLOAD_DATA, {})
    
    message = "📤 **رفع منتج جديد**\n\n"
    message += "الخطوة 1 من 4: المعلومات الأساسية\n\n"
    message += "أرسل **عنوان المنتج** (بالعربي أو الإنجليزي):"
    
    buttons = [[Button.inline("❌ إلغاء", b"mp_upload_cancel")]]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def upload_text_handler(event):
    """Handle text input during upload."""
    sender_id = event.sender_id
    
    # Check if in upload state
    state = conversation_manager.get_state(sender_id)
    step = state.get(STATE_UPLOAD_STEP)
    if not step:
        return  # Not in upload mode
    
    text = event.text.strip()
    upload_data = state.get(STATE_UPLOAD_DATA) or {}
    
    if step == 1:
        # Step 1: Title
        if len(text) < 3:
            return await event.reply("❌ العنوان قصير جداً (3 أحرف على الأقل)")
        if len(text) > 100:
            return await event.reply("❌ العنوان طويل جداً (100 حرف كحد أقصى)")
        
        upload_data['title'] = text
        conversation_manager.set_value(sender_id, STATE_UPLOAD_DATA, upload_data)
        conversation_manager.set_value(sender_id, STATE_UPLOAD_STEP, 2)
        
        message = "📝 **الوصف**\n\n"
        message += "الخطوة 2 من 4\n\n"
        message += "أرسل **وصف تفصيلي** للمنتج:"
        
        buttons = [[Button.inline("❌ إلغاء", b"mp_upload_cancel")]]
        await event.reply(message, buttons=buttons, parse_mode='md')
    
    elif step == 2:
        # Step 2: Description
        if len(text) < 10:
            return await event.reply("❌ الوصف قصير جداً (10 أحرف على الأقل)")
        if len(text) > 1000:
            return await event.reply("❌ الوصف طويل جداً (1000 حرف كحد أقصى)")
        
        upload_data['description'] = text
        conversation_manager.set_value(sender_id, STATE_UPLOAD_DATA, upload_data)
        conversation_manager.set_value(sender_id, STATE_UPLOAD_STEP, 3)
        
        # Show categories
        categories = await database.get_marketplace_categories()
        
        message = "📂 **التصنيف**\n\n"
        message += "الخطوة 3 من 4\n\n"
        message += "اختر التصنيف المناسب:"
        
        buttons = []
        row = []
        for cat in categories:
            btn_text = f"{cat['icon']} {cat['name_ar']}"
            btn_data = f"mp_upload_cat:{cat['category_id']}".encode()
            row.append(Button.inline(btn_text, btn_data))
            
            if len(row) == 2:
                buttons.append(row)
                row = []
        
        if row:
            buttons.append(row)
        
        buttons.append([Button.inline("❌ إلغاء", b"mp_upload_cancel")])
        
        await event.reply(message, buttons=buttons, parse_mode='md')
    
    elif step == 4:
        # Step 4: Waiting for files
        # Check if it's a file/document
        if event.file:
            await handle_file_upload(event, sender_id, upload_data)
        else:
            await event.reply("⚠️ يرجى إرسال ملف أو ملف ZIP")


async def upload_category_handler(event):
    """Handle category selection - Step 3."""
    sender_id = event.sender_id
    
    step = conversation_manager.get_value(sender_id, STATE_UPLOAD_STEP)
    if step != 3:
        return await event.answer("❌ خطأ في التسلسل", alert=True)
    
    # Parse category
    category_id = event.data.decode().split(':')[1]
    
    upload_data = conversation_manager.get_value(sender_id, STATE_UPLOAD_DATA)
    upload_data['category'] = category_id
    conversation_manager.set_value(sender_id, STATE_UPLOAD_DATA, upload_data)
    conversation_manager.set_value(sender_id, STATE_UPLOAD_STEP, 4)
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp(prefix='mp_upload_')
    conversation_manager.set_value(sender_id, STATE_UPLOAD_TEMP, temp_dir)
    
    message = "📁 **رفع الملفات**\n\n"
    message += "الخطوة 4 من 4\n\n"
    message += "أرسل ملفات البوت:\n"
    message += "• يمكنك إرسال ملف ZIP واحد\n"
    message += "• أو إرسال الملفات واحداً تلو الآخر\n"
    message += "• الحد الأقصى: 10 MB لكل ملف\n\n"
    message += "عند الانتهاء، اضغط \"✅ تم\""
    
    buttons = [
        [Button.inline("✅ تم - المراجعة والنشر", b"mp_upload_confirm")],
        [Button.inline("❌ إلغاء", b"mp_upload_cancel")]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def handle_file_upload(event, sender_id, upload_data):
    """Handle file upload during step 4."""
    temp_dir = conversation_manager.get_value(sender_id, STATE_UPLOAD_TEMP)
    if not temp_dir or not os.path.exists(temp_dir):
        return await event.reply("❌ خطأ: المجلد المؤقت غير موجود")
    
    try:
        # Download file
        file_name = event.file.name or f"file_{event.file.id}"
        
        # Check file size
        if event.file.size > 10 * 1024 * 1024:  # 10 MB
            return await event.reply(f"❌ الملف كبير جداً: {file_name}\n(الحد الأقصى: 10 MB)")
        
        file_path = os.path.join(temp_dir, file_name)
        
        await event.reply(f"⏳ جاري تحميل: {file_name}...")
        await event.download_media(file_path)
        
        # Extract if ZIP
        if file_name.endswith('.zip'):
            import zipfile
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                os.remove(file_path)
                await event.reply(f"✅ تم فك ضغط: {file_name}")
            except Exception as e:
                await event.reply(f"❌ فشل فك الضغط: {str(e)}")
        else:
            await event.reply(f"✅ تم تحميل: {file_name}")
        
    except Exception as e:
        await event.reply(f"❌ خطأ في التحميل: {str(e)}")


async def upload_confirm_handler(event):
    """Confirm and publish product."""
    sender_id = event.sender_id
    
    step = conversation_manager.get_value(sender_id, STATE_UPLOAD_STEP)
    if step != 4:
        return await event.answer("❌ خطأ في التسلسل", alert=True)
    
    upload_data = conversation_manager.get_value(sender_id, STATE_UPLOAD_DATA)
    temp_dir = conversation_manager.get_value(sender_id, STATE_UPLOAD_TEMP)
    
    if not temp_dir or not os.path.exists(temp_dir):
        return await event.answer("❌ لم يتم رفع أي ملفات", alert=True)
    
    # Check if files exist
    files = os.listdir(temp_dir)
    if not files:
        return await event.answer("❌ لم يتم رفع أي ملفات", alert=True)
    
    # Show confirmation
    category = await database.get_marketplace_category(upload_data['category'])
    
    message = "✅ **المراجعة النهائية**\n\n"
    message += f"📦 **العنوان:** {upload_data['title']}\n"
    message += f"📂 **التصنيف:** {category['name_ar']}\n"
    message += f"📝 **الوصف:** {upload_data['description'][:100]}...\n"
    message += f"📁 **الملفات:** {len(files)} ملف\n"
    message += f"💰 **السعر:** مجاني\n\n"
    message += "هل تريد نشر المنتج؟"
    
    buttons = [
        [Button.inline("✅ نشر الآن", b"mp_upload_publish")],
        [Button.inline("❌ إلغاء", b"mp_upload_cancel")]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def upload_cancel_handler(event):
    """Cancel upload process."""
    sender_id = event.sender_id
    
    # Cleanup temp directory
    temp_dir = conversation_manager.get_value(sender_id, STATE_UPLOAD_TEMP)
    if temp_dir and os.path.exists(temp_dir):
        import shutil
        shutil.rmtree(temp_dir)
    
    # Clear state
    conversation_manager.clear_value(sender_id, STATE_UPLOAD_STEP)
    conversation_manager.clear_value(sender_id, STATE_UPLOAD_DATA)
    conversation_manager.clear_value(sender_id, STATE_UPLOAD_TEMP)
    
    message = "❌ تم إلغاء عملية الرفع"
    buttons = [[Button.inline("🔙 رجوع للماركت", b"marketplace_home")]]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


# Register publish handler
async def upload_publish_handler(event):
    """Publish the product."""
    sender_id = event.sender_id
    
    upload_data = conversation_manager.get_value(sender_id, STATE_UPLOAD_DATA)
    temp_dir = conversation_manager.get_value(sender_id, STATE_UPLOAD_TEMP)
    
    if not upload_data or not temp_dir:
        return await event.answer("❌ خطأ في البيانات", alert=True)
    
    # Check profanity in title and description
    from bot.services.profanity_filter import check_profanity, check_user_ban
    
    is_banned, ban_reason = await check_user_ban(sender_id, 'upload')
    if is_banned:
        # Cleanup
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
        conversation_manager.clear_value(sender_id, STATE_UPLOAD_STEP)
        conversation_manager.clear_value(sender_id, STATE_UPLOAD_DATA)
        conversation_manager.clear_value(sender_id, STATE_UPLOAD_TEMP)
        return await event.edit(ban_reason)
    
    # Check title
    is_clean, reason, severity = await check_profanity(upload_data['title'], sender_id)
    if not is_clean:
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
        conversation_manager.clear_value(sender_id, STATE_UPLOAD_STEP)
        conversation_manager.clear_value(sender_id, STATE_UPLOAD_DATA)
        conversation_manager.clear_value(sender_id, STATE_UPLOAD_TEMP)
        return await event.edit(f"❌ اسم المنتج غير مقبول\n\n{reason}")
    
    # Check description
    is_clean, reason, severity = await check_profanity(upload_data['description'], sender_id)
    if not is_clean:
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)
        conversation_manager.clear_value(sender_id, STATE_UPLOAD_STEP)
        conversation_manager.clear_value(sender_id, STATE_UPLOAD_DATA)
        conversation_manager.clear_value(sender_id, STATE_UPLOAD_TEMP)
        return await event.edit(f"❌ وصف المنتج غير مقبول\n\n{reason}")
    
    await event.edit("⏳ جاري النشر...")
    
    # Create product
    success, message, product_id = await marketplace_service.create_product(
        owner_id=sender_id,
        title=upload_data['title'],
        description=upload_data['description'],
        category=upload_data['category'],
        files_source=temp_dir
    )
    
    # Cleanup
    if temp_dir and os.path.exists(temp_dir):
        import shutil
        shutil.rmtree(temp_dir)
    
    conversation_manager.clear_value(sender_id, STATE_UPLOAD_STEP)
    conversation_manager.clear_value(sender_id, STATE_UPLOAD_DATA)
    conversation_manager.clear_value(sender_id, STATE_UPLOAD_TEMP)
    
    if success:
        buttons = [[Button.inline("📦 عرض المنتج", f"mp_view:{product_id}".encode())]]
        await event.edit(message, buttons=buttons, parse_mode='md')
    else:
        buttons = [[Button.inline("🔙 رجوع", b"marketplace_home")]]
        await event.edit(message, buttons=buttons, parse_mode='md')


def setup_publish(client):
    """Setup publish handler separately."""
    client.add_event_handler(upload_publish_handler, events.CallbackQuery(pattern=b"mp_upload_publish"))


# Call setup_publish in setup
def setup(client):
    client.add_event_handler(upload_start_handler, events.CallbackQuery(pattern=b"mp_upload_start"))
    client.add_event_handler(upload_category_handler, events.CallbackQuery(pattern=b"mp_upload_cat:"))
    client.add_event_handler(upload_confirm_handler, events.CallbackQuery(pattern=b"mp_upload_confirm"))
    client.add_event_handler(upload_cancel_handler, events.CallbackQuery(pattern=b"mp_upload_cancel"))
    client.add_event_handler(upload_publish_handler, events.CallbackQuery(pattern=b"mp_upload_publish"))
    client.add_event_handler(upload_text_handler, events.NewMessage())
    print("✅ Marketplace upload handlers loaded.")
