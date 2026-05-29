# bot_v2/bot/handlers/admin/settings.py
# Contains handlers for general bot settings, host settings (max files/folders), and AI usage limits.

from telethon import events
from telethon.tl.custom import Button
from typing import TYPE_CHECKING, Dict, Any, List
import os
import asyncio
from datetime import datetime

if TYPE_CHECKING:
    from telethon import TelegramClient

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings
from bot.core.data_manager import load_host_settings, save_host_settings, load_admin_settings, save_admin_settings, load_site_settings, save_site_settings
from bot.core.state import conversation_manager

# Local Imports from bot_v2 services
from bot.services.user_service import check_user_status

# Local Imports from bot_v2 utilities
from bot.utils.telegram import safe_edit_message
from bot.utils.backup import create_backup_zip

# Local Imports from bot_v2 handlers (for now, will be refactored later)


# --- UI Functions ---
def get_host_settings_buttons() -> List[List[Button]]:
    """Builds the buttons for the hosting settings panel."""
    host_settings = load_host_settings()
    admin_settings = load_admin_settings()

    php_status = "✅" if host_settings.get('allow_php', True) else "❌"
    json_status = "✅" if host_settings.get('allow_json', True) else "❌"
    txt_status = "✅" if host_settings.get('allow_txt', True) else "❌"
    
    bot_mode = host_settings.get('bot_mode', 'paid')
    bot_mode_text = "🆓 مجاني للجميع" if bot_mode == 'free' else "💰 الوضع المدفوع"

    ai_free_enabled = admin_settings.get('ai_free_enabled', True)
    ai_free_status = "✅ مفعل" if ai_free_enabled else "❌ معطل"

    buttons = [
        [Button.inline(f"وضع البوت: {bot_mode_text}", data="admin:toggle_bot_mode")],
        [Button.inline("📊 حدود الفئة المجانية (Free)", data="admin:tier_settings:free")],
        [Button.inline("💎 حدود الفئة المدفوعة (Pro)", data="admin:tier_settings:pro")],
        [Button.inline(f"استقبال PHP {php_status}", data="admin:toggle_php")],
        [Button.inline(f"استقبال JSON {json_status}", data="admin:toggle_json"),
         Button.inline(f"استقبال TXT {txt_status}", data="admin:toggle_txt")],
        
        [Button.inline(f"AI مجاني: {ai_free_status}", data="admin:toggle_ai_free")],
        [Button.inline(f"⚙️ حد AI المجاني (Bot) ({admin_settings.get('ai_free_fallback_limit', 5)})", data="admin:set_ai_free_fallback_limit")],
        [Button.inline(f"⚙️ حد AI المجاني (Agent) ({admin_settings.get('ai_agent_free_limit', 5)})", data="admin:set_ai_agent_free_limit")],
        [Button.inline(f"⚙️ حد AI المدفوع ({admin_settings.get('ai_pro_daily_limit', 5)})", data="admin:set_ai_pro_limit")],
        
        [Button.inline("🌐 إعدادات الموقع الإلكتروني", data="admin:site_settings_section")],
        [Button.inline("⬅️ رجوع", data='admin:main_menu')]
    ]
    return buttons

async def send_tier_settings_panel(event: events.CallbackQuery.Event, tier: str):
    """Sends the settings panel for a specific tier (free/pro)."""
    host_settings = load_host_settings()
    tiers = host_settings.get('tiers', {})
    t_data = tiers.get(tier, {})
    
    tier_name = "المجانية (Free)" if tier == "free" else "المدفوعة (Pro)"
    text = (
        f"**📊 إعدادات الفئة {tier_name}**\n\n"
        f"تحكم في قيود الاستهلاك لهذه الفئة."
    )
    
    buttons = [
        [Button.inline(f"💾 المساحة: {t_data.get('max_storage_mb', 0)} MB", data=f"admin:set_tier_limit:{tier}:max_storage_mb")],
        [Button.inline(f"📄 حد الملفات: {t_data.get('max_files', 0)}", data=f"admin:set_tier_limit:{tier}:max_files")],
        [Button.inline(f"📁 حد المجلدات: {t_data.get('max_folders', 0)}", data=f"admin:set_tier_limit:{tier}:max_folders")],
        [Button.inline(f"📦 ملفات الـ Zip: {t_data.get('max_zip_files', 0)}", data=f"admin:set_tier_limit:{tier}:max_zip_files")],
        [Button.inline("⬅️ رجوع", data="admin:host_settings_section")]
    ]
    await safe_edit_message(event, text, buttons=buttons)


async def send_host_settings_panel(event: events.CallbackQuery.Event):
    """Sends the hosting settings panel to the admin."""
    text = "**⚙️ إعدادات بوت الاستضافة**\n\nتحكم في القيود والخصائص للمستخدمين."
    buttons = get_host_settings_buttons()
    await safe_edit_message(event, text, buttons=buttons)


async def send_site_settings_panel(event: events.CallbackQuery.Event):
    """Sends the website settings panel to the admin."""
    site_settings = load_site_settings()
    
    status_icon = "✅" if site_settings.get('site_status') == 'active' else "❌"
    
    text = (
        "**🌐 إعدادات الموقع الإلكتروني**\n\n"
        f"🏠 **اسم الموقع:** `{site_settings.get('site_name')}`\n"
        f"📝 **الوصف:** `{site_settings.get('site_description')}`\n"
        f"🚦 **الحالة:** {status_icon}\n\n"
        "إليك الروابط المسجلة حالياً:\n"
        f"- **تليجرام:** `{site_settings.get('contact_telegram')}`\n"
        f"- **يوتيوب:** `{site_settings.get('contact_youtube')}`\n"
        f"- **جيت هب:** `{site_settings.get('contact_github')}`"
    )
    
    buttons = [
        [Button.inline(f"تغيير اسم الموقع ✏️", data="admin:set_site_field:site_name")],
        [Button.inline(f"تغيير الوصف ✏️", data="admin:set_site_field:site_description")],
        [Button.inline(f"تغيير الحالة ({status_icon})", data="admin:toggle_site_status")],
        [Button.inline("تعديل بيانات المطور 👨‍💻", data="admin:site_developer_menu")],
        [Button.inline("تعديل روابط التواصل 🔗", data="admin:site_contacts_menu")],
        [Button.inline("🎥 إدارة فيديوهات الشروحات", data="admin:tutorials_list")],
        [Button.inline("⬅️ رجوع", data="admin:main_menu")]
    ]
    await safe_edit_message(event, text, buttons=buttons)

async def send_site_developer_menu(event: events.CallbackQuery.Event):
    """Sub-menu for developer info."""
    site_settings = load_site_settings()
    text = (
        "**👨‍💻 تعديل بيانات المطور**\n\n"
        f"👤 **الاسم:** `{site_settings.get('developer_name')}`\n"
        f"🏷 **اللقب:** `{site_settings.get('developer_title')}`\n"
        f"🖼 **رابط الصورة:** `{site_settings.get('developer_image')}`"
    )
    buttons = [
        [Button.inline("تغيير الاسم ✏️", data="admin:set_site_field:developer_name")],
        [Button.inline("تغيير اللقب �", data="admin:set_site_field:developer_title")],
        [Button.inline("تغيير رابط الصورة �", data="admin:set_site_field:developer_image")],
        [Button.inline("⬅️ رجوع", data="admin:site_settings_section")]
    ]
    await safe_edit_message(event, text, buttons=buttons)

async def send_site_contacts_menu(event: events.CallbackQuery.Event):
    """Sub-menu for contact links."""
    text = "**🔗 تعديل روابط التواصل الاجتماعي للموقع**"
    buttons = [
        [Button.inline("رابط تليجرام ✈️", data="admin:set_site_field:contact_telegram")],
        [Button.inline("رابط يوتيوب 📺", data="admin:set_site_field:contact_youtube")],
        [Button.inline("رابط جيت هب 🐙", data="admin:set_site_field:contact_github")],
        [Button.inline("⬅️ رجوع", data="admin:site_settings_section")]
    ]
    await safe_edit_message(event, text, buttons=buttons)


# --- Callbacks ---

async def host_settings_menu_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    await send_host_settings_panel(event)


async def toggle_php_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    host_settings = load_host_settings()
    host_settings['allow_php'] = not host_settings.get('allow_php', True)
    save_host_settings(host_settings)
    await send_host_settings_panel(event)
    await event.answer("تم تحديث الإعداد.")

async def toggle_json_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    host_settings = load_host_settings()
    host_settings['allow_json'] = not host_settings.get('allow_json', True)
    save_host_settings(host_settings)
    await send_host_settings_panel(event)
    await event.answer("تم تحديث الإعداد.")

async def toggle_txt_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    host_settings = load_host_settings()
    host_settings['allow_txt'] = not host_settings.get('allow_txt', True)
    save_host_settings(host_settings)
    await send_host_settings_panel(event)
    await event.answer("تم تحديث الإعداد.")

async def toggle_bot_mode_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    
    host_settings = load_host_settings()
    current_mode = host_settings.get('bot_mode', 'paid')
    host_settings['bot_mode'] = 'free' if current_mode == 'paid' else 'paid'
    save_host_settings(host_settings)
    
    await send_host_settings_panel(event)
    mode_msg = "أصبح البوت الآن مجانياً للجميع (ما عدا حدود الرفع)." if host_settings['bot_mode'] == 'free' else "عاد البوت للوضع المدفوع."
    await event.answer(mode_msg, alert=True)

async def tier_settings_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    
    tier = event.data.decode().split(':')[-1]
    await send_tier_settings_panel(event, tier)

async def set_tier_limit_prompt(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
    
    data_parts = event.data.decode().split(':')
    tier = data_parts[2]
    limit_key = data_parts[3]
    
    conversation_manager.set_state(sender_id, f'awaiting_tier_limit:{tier}:{limit_key}', message_id=event.message_id)
    
    labels = {
        'max_storage_mb': 'المساحة التخزينية (MB)',
        'max_files': 'عدد الملفات الكلي',
        'max_folders': 'عدد المجلدات الكلي',
        'max_zip_files': 'عدد الملفات المسموحة داخل الـ Zip'
    }
    
    tier_name = "المجانية" if tier == "free" else "المدفوعة"
    label = labels.get(limit_key, limit_key)
    
    msg = f"**🔢 تحديد {label} للفئة {tier_name}:**\n\nأرسل الآن القيمة الجديدة (رقم)."
    await safe_edit_message(event, msg, buttons=[[Button.inline("إلغاء ❌", data=f"admin:tier_settings:{tier}")]])

async def backup_now_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) != 'sudo':
        return await event.answer("🚫 هذه الميزة مخصصة للمالك فقط.", alert=True)
    
    await event.answer("📦 جاري تحضير النسخة الاحتياطية...", alert=True)
    # Run in background
    asyncio.create_task(perform_manual_backup(event.client, sender_id))

async def toggle_daily_backup_callback(event: events.CallbackQuery.Event):
    sender_id = event.sender_id
    if check_user_status(sender_id) != 'sudo':
        return await event.answer("🚫 هذه الميزة مخصصة للمالك فقط.", alert=True)
        
    admin_settings = load_admin_settings()
    admin_settings['daily_backup'] = not admin_settings.get('daily_backup', False)
    save_admin_settings(admin_settings)
    
    from bot.handlers.admin.main import send_main_admin_panel
    await send_main_admin_panel(event, edit=True)
    await event.answer("تم تحديث إعدادات النسخ الاحتياطي.")

async def perform_manual_backup(client, recipient_id):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    root_dir = os.getcwd()
    folder_name = os.path.basename(root_dir)
    zip_filename = f"{folder_name}_manual_backup_{timestamp}.zip"
    zip_path = os.path.join(root_dir, zip_filename)
    
    try:
        await asyncio.to_thread(create_backup_zip, root_dir, zip_path)
        await client.send_file(
            recipient_id,
            zip_path,
            caption=f"📦 **نسخة احتياطية فورية**\n🗂 المجلد: `{folder_name}`\n📅 التاريخ: `{timestamp}`",
            force_document=True
        )
    except Exception as e:
        await client.send_message(recipient_id, f"❌ فشل النسخ الاحتياطي: {e}")
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

# --- Conversation Handler for admin:settings (message inputs) ---
async def admin_settings_conversation_handler(event: events.NewMessage.Event):
    sender_id = event.sender_id
    state_data = conversation_manager.get_state(sender_id)
    state_status = state_data.get('status')
    message_id_to_edit = state_data.get('message_id')

    # A helper function to restore the panel after an action
    async def restore_panel(menu_function_to_call):
        if message_id_to_edit:
            try:
                mock_event = await event.client.get_messages(sender_id, ids=message_id_to_edit)
                if mock_event:
                    await menu_function_to_call(mock_event)
            except Exception as e:
                print(f"Error restoring panel: {e}")
                await event.reply("اكتمل الإجراء.")

    if state_status in ['awaiting_max_folders', 'awaiting_max_php', 'awaiting_ai_free_fallback_limit', 'awaiting_ai_agent_free_limit', 'awaiting_ai_pro_limit'] or state_status.startswith('awaiting_tier_limit:'):
        try:
            new_limit = int(event.text)
            if new_limit < 0:
                await event.reply("❌ لا يمكن أن يكون الحد عددًا سالبًا. يرجى إرسال رقم صحيح.")
                return

            if state_status.startswith('awaiting_tier_limit:'):
                _, tier, limit_key = state_status.split(':')
                host_settings = load_host_settings()
                if 'tiers' not in host_settings: host_settings['tiers'] = {}
                if tier not in host_settings['tiers']: host_settings['tiers'][tier] = {}
                
                host_settings['tiers'][tier][limit_key] = new_limit
                save_host_settings(host_settings)
                reply_text = f"✅ تم تحديث العتبة بنجاح."
                
                conversation_manager.delete_state(sender_id)
                await event.reply(reply_text)
                return await restore_panel(lambda e: send_tier_settings_panel(e, tier))

            elif state_status in ['awaiting_max_folders', 'awaiting_max_php']:
                host_settings = load_host_settings()
                if state_status == 'awaiting_max_folders':
                    host_settings['max_folders'] = new_limit
                    reply_text = f"✅ تم تحديث الحد الأقصى للمجلدات إلى **{new_limit}**."
                else: # awaiting_max_php
                    host_settings['max_php_files'] = new_limit
                    reply_text = f"✅ تم تحديث الحد الأقصى لملفات PHP إلى **{new_limit}**."
                save_host_settings(host_settings)
            else: # AI limits
                admin_settings = load_admin_settings()
                if state_status == 'awaiting_ai_free_fallback_limit':
                    admin_settings['ai_free_fallback_limit'] = new_limit
                    reply_text = f"✅ تم تحديث الحد اليومي لمفاتيح البوت (للمستخدم المجاني) إلى **{new_limit}**."
                elif state_status == 'awaiting_ai_agent_free_limit':
                    admin_settings['ai_agent_free_limit'] = new_limit
                    reply_text = f"✅ تم تحديث حد الـ Agent اليومي (للمستخدم المجاني) إلى **{new_limit}**."
                elif state_status == 'awaiting_ai_pro_limit':
                    admin_settings['ai_pro_daily_limit'] = new_limit
                    reply_text = f"✅ تم تحديث الحد اليومي لمفاتيح البوت (للمستخدم PRO) إلى **{new_limit}**."
                save_admin_settings(admin_settings)
            
            await event.reply(reply_text)

        except (ValueError, TypeError):
            await event.reply("❌ الإدخال غير صالح. يرجى إرسال رقم صحيح فقط.")
        
        conversation_manager.delete_state(sender_id)
        await restore_panel(send_host_settings_panel)

    elif state_status.startswith('awaiting_site_field:'):
        field = state_status.split(':')[-1]
        new_val = event.text.strip()
        
        site_settings = load_site_settings()
        site_settings[field] = new_val
        save_site_settings(site_settings)
        
        conversation_manager.delete_state(sender_id)
        await event.reply(f"✅ تم تحديث `{field}` بنجاح.")
        
        # Decide which panel to restore
        if field.startswith('contact_'):
            await restore_panel(send_site_contacts_menu)
        else:
            await restore_panel(send_site_settings_panel)

    elif state_status == 'awaiting_tutorial_title':
        title = event.text.strip()
        conversation_manager.set_state(sender_id, 'awaiting_tutorial_desc', message_id=message_id_to_edit, context={'title': title})
        await event.reply(f"✅ تم حفظ العنوان: `{title}`\n\n**📝 أرسل الآن وصفاً قصيراً للفيديو:**")

    elif state_status == 'awaiting_tutorial_desc':
        desc = event.text.strip()
        prev_data = state_data.get('context', {})
        conversation_manager.set_state(sender_id, 'awaiting_tutorial_url', message_id=message_id_to_edit, context={**prev_data, 'desc': desc})
        await event.reply(f"✅ تم حفظ الوصف.\n\n**🔗 أرسل الآن رابط الفيديو (YouTube):**")

    elif state_status == 'awaiting_tutorial_url':
        url = event.text.strip()
        state_data = conversation_manager.get_state(sender_id)
        message_id_to_edit = state_data.get('message_id')
        
        if 'youtube.com' not in url and 'youtu.be' not in url:
            return await event.reply("❌ عذراً، يجب إرسال رابط يوتيوب صحيح.")
            
        prev_data = state_data.get('context', {})
        site_settings = load_site_settings()
        tutorials = site_settings.get('tutorials', [])
        
        new_id = 1
        if tutorials:
            new_id = max(t.get('id', 0) for t in tutorials) + 1
            
        new_tut = {
            "id": new_id,
            "title": prev_data.get('title'),
            "description": prev_data.get('desc'),
            "video_url": url
        }
        
        tutorials.append(new_tut)
        site_settings['tutorials'] = tutorials
        save_site_settings(site_settings)
        
        conversation_manager.delete_state(sender_id)
        await event.reply("✅ تم إضافة الفيديو بنجاح إلى الموقع!")
        await restore_panel(send_tutorials_list)

    elif state_status.startswith('awaiting_edit_tut_field:'):
        parts = state_status.split(':')
        field = parts[1]
        tut_id = int(parts[2])
        new_value = event.text.strip()
        
        if field == 'video_url' and ('youtube.com' not in new_value and 'youtu.be' not in new_value):
            return await event.reply("❌ عذراً، يجب إرسال رابط يوتيوب صحيح.")
            
        site_settings = load_site_settings()
        tutorials = site_settings.get('tutorials', [])
        
        found = False
        for t in tutorials:
            if t.get('id') == tut_id:
                t[field] = new_value
                found = True
                break
                
        if not found:
            conversation_manager.delete_state(sender_id)
            return await event.reply("❌ لم يتم العثور على الفيديو.")
            
        site_settings['tutorials'] = tutorials
        save_site_settings(site_settings)
        
        conversation_manager.delete_state(sender_id)
        await event.reply(f"✅ تم تحديث `{field}` بنجاح.")
        await restore_panel(lambda e: manage_tutorial_menu(e, tut_id))

async def send_tutorials_list(event: events.CallbackQuery.Event):
    """Displays the list of tutorials from site_settings.json."""
    site_settings = load_site_settings()
    tutorials = site_settings.get('tutorials', [])
    
    text = (
        "**🎥 إدارة فيديوهات الشروحات**\n\n"
        "هذه الفيديوهات تظهر في صفحة 'شروحات' على الموقع الإلكتروني."
    )
    
    if not tutorials:
        text += "\n\n⚠️ لا توجد فيديوهات مضافة حالياً."
        buttons = [[Button.inline("➕ إضافة فيديو جديد", data="admin:add_tutorial_prompt")]]
    else:
        buttons = []
        for t in tutorials:
            buttons.append([Button.inline(f"🎬 {t.get('title')}", data=f"admin:manage_tutorial:{t.get('id')}")])
        buttons.append([Button.inline("➕ إضافة فيديو جديد", data="admin:add_tutorial_prompt")])
        
    buttons.append([Button.inline("⬅️ رجوع", data="admin:site_settings_section")])
    await safe_edit_message(event, text, buttons=buttons)

async def manage_tutorial_menu(event: events.CallbackQuery.Event, tut_id: int = None):
    """Shows the management menu for a specific tutorial."""
    try:
        if tut_id is None:
            tut_id = int(event.data.decode().split(':')[-1])
        site_settings = load_site_settings()
        tutorials = site_settings.get('tutorials', [])
        tutorial = next((t for t in tutorials if t.get('id') == tut_id), None)
        
        if not tutorial:
            return await event.answer("❌ لم يتم العثور على الفيديو.", alert=True)
            
        text = (
            f"**🎥 إدارة الفيديو: {tutorial.get('title')}**\n\n"
            f"📝 **الوصف**: {tutorial.get('description')}\n"
            f"🔗 **الرابط**: {tutorial.get('video_url')}\n"
            f"📊 **المشاهدات**: `{tutorial.get('view_count', 0)}`"
        )
        
        buttons = [
            [Button.inline("✏️ تعديل العنوان", data=f"admin:edit_tut_field:title:{tut_id}")],
            [Button.inline("📝 تعديل الوصف", data=f"admin:edit_tut_field:description:{tut_id}")],
            [Button.inline("🔗 تعديل الرابط", data=f"admin:edit_tut_field:video_url:{tut_id}")],
            [Button.inline("🗑 حذف الفيديو", data=f"admin:delete_tutorial:{tut_id}")],
            [Button.inline("⬅️ رجوع للقائمة", data="admin:tutorials_list")]
        ]
        await safe_edit_message(event, text, buttons=buttons)
    except Exception as e:
        await event.answer(f"❌ خطأ: {e}", alert=True)

async def edit_tutorial_field_prompt(event: events.CallbackQuery.Event):
    """Starts the conversation to edit a tutorial field."""
    parts = event.data.decode().split(':')
    field = parts[2]
    tut_id = int(parts[3])
    
    field_map = {
        'title': 'العنوان',
        'description': 'الوصف',
        'video_url': 'رابط الفيديو'
    }
    
    conversation_manager.set_state(event.sender_id, f'awaiting_edit_tut_field:{field}:{tut_id}', message_id=event.message_id)
    await safe_edit_message(event, f"**✏️ تعديل {field_map.get(field)} للفيديو:**\n\nأرسل القيمة الجديدة الآن.", buttons=[[Button.inline("إلغاء ❌", data=f"admin:manage_tutorial:{tut_id}")]])

async def add_tutorial_prompt(event: events.CallbackQuery.Event):
    """Starts the conversation to add a new tutorial."""
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
        
    conversation_manager.set_state(sender_id, 'awaiting_tutorial_title', message_id=event.message_id)
    await safe_edit_message(event, "**🎬 إضافة فيديو شرح جديد**\n\nأرسل الآن عنوان الفيديو:", buttons=[[Button.inline("إلغاء ❌", data="admin:tutorials_list")]])

async def delete_tutorial_callback(event: events.CallbackQuery.Event):
    """Deletes a tutorial by ID."""
    sender_id = event.sender_id
    if check_user_status(sender_id) not in ['sudo', 'admin']:
        return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
        
    try:
        tut_id = int(event.data.decode().split(':')[-1])
        site_settings = load_site_settings()
        tutorials = site_settings.get('tutorials', [])
        
        new_tutorials = [t for t in tutorials if t.get('id') != tut_id]
        if len(new_tutorials) == len(tutorials):
            return await event.answer("❌ لم يتم العثور على الفيديو.", alert=True)
            
        site_settings['tutorials'] = new_tutorials
        save_site_settings(site_settings)
        
        await event.answer("✅ تم حذف الفيديو بنجاح.")
        await send_tutorials_list(event)
    except Exception as e:
        await event.answer(f"❌ خطأ: {e}", alert=True)

def setup(client_instance: "TelegramClient"):
    """Registers all admin settings handlers with the TelegramClient."""
    # Callbacks for menu navigation
    client_instance.on(events.CallbackQuery(pattern=b'admin:host_settings_section'))(host_settings_menu_callback)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:tier_settings:(free|pro)'))(tier_settings_callback)

    # Callbacks for toggles
    client_instance.on(events.CallbackQuery(pattern=rb'admin:toggle_php'))(toggle_php_callback)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:toggle_json'))(toggle_json_callback)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:toggle_txt'))(toggle_txt_callback)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:toggle_bot_mode'))(toggle_bot_mode_callback)
    # Re-register toggle_ai_free if it was accidentally removed during refactor
    async def toggle_ai_free_callback(event: events.CallbackQuery.Event):
        sender_id = event.sender_id
        if check_user_status(sender_id) not in ['sudo', 'admin']:
            return await event.answer("🚫 ليس لديك صلاحية الوصول لهذه الميزة.", alert=True)
        admin_settings = load_admin_settings()
        admin_settings['ai_free_enabled'] = not admin_settings.get('ai_free_enabled', True) 
        save_admin_settings(admin_settings)
        await send_host_settings_panel(event)
        await event.answer("تم تحديث إعدادات الـ AI.")
    client_instance.on(events.CallbackQuery(pattern=rb'admin:toggle_ai_free'))(toggle_ai_free_callback)

    # Callbacks for prompts
    client_instance.on(events.CallbackQuery(pattern=rb'admin:set_tier_limit:(free|pro):(\w+)'))(set_tier_limit_prompt)
    
    async def set_ai_free_fallback_limit_prompt(event: events.CallbackQuery.Event):
        conversation_manager.set_state(event.sender_id, 'awaiting_ai_free_fallback_limit', message_id=event.message_id)
        await safe_edit_message(event, "**⚙️ تحديد حد AI المجاني (في البوت)**", buttons=[[Button.inline("إلغاء ❌", data="admin:host_settings_section")]])
    client_instance.on(events.CallbackQuery(pattern=b'admin:set_ai_free_fallback_limit'))(set_ai_free_fallback_limit_prompt)

    async def set_ai_agent_free_limit_prompt(event: events.CallbackQuery.Event):
        conversation_manager.set_state(event.sender_id, 'awaiting_ai_agent_free_limit', message_id=event.message_id)
        await safe_edit_message(event, "**⚙️ تحديد حد الـ Agent المجاني (في الموقع)**", buttons=[[Button.inline("إلغاء ❌", data="admin:host_settings_section")]])
    client_instance.on(events.CallbackQuery(pattern=b'admin:set_ai_agent_free_limit'))(set_ai_agent_free_limit_prompt)

    async def set_ai_pro_limit_prompt(event: events.CallbackQuery.Event):
        conversation_manager.set_state(event.sender_id, 'awaiting_ai_pro_limit', message_id=event.message_id)
        await safe_edit_message(event, "**⚙️ تحديد حد AI المدفوع**", buttons=[[Button.inline("إلغاء ❌", data="admin:host_settings_section")]])
    client_instance.on(events.CallbackQuery(pattern=b'admin:set_ai_pro_limit'))(set_ai_pro_limit_prompt)

    client_instance.on(events.CallbackQuery(pattern=b'admin:backup_now'))(backup_now_callback)
    client_instance.on(events.CallbackQuery(pattern=b'admin:toggle_daily_backup'))(toggle_daily_backup_callback)

    # Site Settings Callbacks
    client_instance.on(events.CallbackQuery(pattern=b'admin:site_settings_section'))(send_site_settings_panel)
    client_instance.on(events.CallbackQuery(pattern=b'admin:site_contacts_menu'))(send_site_contacts_menu)
    client_instance.on(events.CallbackQuery(pattern=b'admin:site_developer_menu'))(send_site_developer_menu)
    
    async def toggle_site_status_callback(event: events.CallbackQuery.Event):
        site_settings = load_site_settings()
        site_settings['site_status'] = 'maintenance' if site_settings.get('site_status') == 'active' else 'active'
        save_site_settings(site_settings)
        await send_site_settings_panel(event)
    client_instance.on(events.CallbackQuery(pattern=b'admin:toggle_site_status'))(toggle_site_status_callback)

    async def set_site_field_prompt(event: events.CallbackQuery.Event):
        field = event.data.decode().split(':')[-1]
        conversation_manager.set_state(event.sender_id, f'awaiting_site_field:{field}', message_id=event.message_id)
        await safe_edit_message(event, f"**✏️ إدخال قيمة جديدة لـ `{field}`:**\n\nأرسل القيمة الآن.", buttons=[[Button.inline("إلغاء ❌", data="admin:site_settings_section")]])
    client_instance.on(events.CallbackQuery(pattern=rb'admin:set_site_field:(\w+)'))(set_site_field_prompt)

    # Tutorial Callbacks
    client_instance.on(events.CallbackQuery(pattern=b'admin:tutorials_list'))(send_tutorials_list)
    client_instance.on(events.CallbackQuery(pattern=b'admin:add_tutorial_prompt'))(add_tutorial_prompt)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:delete_tutorial:(\d+)'))(delete_tutorial_callback)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:manage_tutorial:(\d+)'))(manage_tutorial_menu)
    client_instance.on(events.CallbackQuery(pattern=rb'admin:edit_tut_field:(\w+):(\d+)'))(edit_tutorial_field_prompt)

    # NewMessage handler for conversations
    client_instance.on(events.NewMessage(func=lambda e: e.is_private and conversation_manager.has_state(e.sender_id) and (conversation_manager.get_status(e.sender_id) in ['awaiting_max_folders', 'awaiting_max_php', 'awaiting_ai_free_fallback_limit', 'awaiting_ai_agent_free_limit', 'awaiting_ai_pro_limit', 'awaiting_tutorial_title', 'awaiting_tutorial_desc', 'awaiting_tutorial_url'] or conversation_manager.get_status(e.sender_id).startswith('awaiting_tier_limit:') or conversation_manager.get_status(e.sender_id).startswith('awaiting_site_field:') or conversation_manager.get_status(e.sender_id).startswith('awaiting_edit_tut_field:'))))(admin_settings_conversation_handler)
    print("✅ Admin Settings handlers registered.")
