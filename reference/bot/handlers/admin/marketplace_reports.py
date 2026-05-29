# bot/handlers/admin/marketplace_reports.py
# Abuse reports management

from telethon import events, Button
from bot.core import database
from bot.handlers.admin.marketplace_admin import require_marketplace_admin
from bot.handlers.admin.marketplace_products import log_admin_action

def setup(client):
    client.add_event_handler(reports_list_handler, events.CallbackQuery(pattern=rb"admin_mp_reports:.+"))
    client.add_event_handler(report_detail_handler, events.CallbackQuery(pattern=rb"admin_mp_report:\d+"))
    client.add_event_handler(resolve_report_handler, events.CallbackQuery(pattern=rb"admin_mp_resolve:\d+:.+"))


async def reports_list_handler(event):
    """List abuse reports."""
    if not await require_marketplace_admin(event):
        return
    
    # Parse: admin_mp_reports:status:page
    data = event.data.decode().split(':')
    status = data[1]
    page = int(data[2]) if len(data) > 2 else 0
    
    REPORTS_PER_PAGE = 8
    offset = page * REPORTS_PER_PAGE
    
    reports, total = await get_reports(status, REPORTS_PER_PAGE, offset)
    total_pages = (total + REPORTS_PER_PAGE - 1) // REPORTS_PER_PAGE
    
    status_names = {'pending': 'قيد المراجعة', 'resolved': 'محلولة', 'dismissed': 'مرفوضة'}
    
    message = f"🚨 **تقارير الإساءة**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"الحالة: {status_names.get(status, status)} | الصفحة {page + 1} من {total_pages}\n\n"
    
    if not reports:
        message += "لا توجد تقارير."
    else:
        for i, report in enumerate(reports, 1):
            message += f"{i}️⃣ **تقرير #{report['id']}**\n"
            message += f"   النوع: {report['target_type']}\n"
            message += f"   السبب: {report['reason'][:50]}...\n"
            message += f"   📅 {report['created_at']}\n\n"
    
    # Status filter buttons
    filter_buttons = [
        [
            Button.inline("● قيد المراجعة" if status == 'pending' else "○ قيد المراجعة", b"admin_mp_reports:pending:0"),
            Button.inline("● محلولة" if status == 'resolved' else "○ محلولة", b"admin_mp_reports:resolved:0")
        ],
        [Button.inline("● مرفوضة" if status == 'dismissed' else "○ مرفوضة", b"admin_mp_reports:dismissed:0")]
    ]
    
    # Report buttons
    report_buttons = []
    for i, report in enumerate(reports, 1):
        report_buttons.append([Button.inline(f"🔍 #{i}", f"admin_mp_report:{report['id']}".encode())])
    
    # Navigation
    nav_row = []
    if page > 0:
        nav_row.append(Button.inline("◀️", f"admin_mp_reports:{status}:{page-1}".encode()))
    if page < total_pages - 1:
        nav_row.append(Button.inline("▶️", f"admin_mp_reports:{status}:{page+1}".encode()))
    
    buttons = filter_buttons + report_buttons
    if nav_row:
        buttons.append(nav_row)
    buttons.append([Button.inline("🔙 رجوع", b"admin_marketplace_home")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def report_detail_handler(event):
    """Show report details."""
    if not await require_marketplace_admin(event):
        return
    
    report_id = int(event.data.decode().split(':')[1])
    
    report = await get_report_detail(report_id)
    if not report:
        return await event.answer("❌ التقرير غير موجود", alert=True)
    
    # Get reporter name
    try:
        from bot.core.client import client
        reporter = await client.get_entity(report['reporter_id'])
        reporter_name = reporter.first_name or "مستخدم"
    except:
        reporter_name = "مستخدم"
    
    message = f"🚨 **تفاصيل التقرير**\n"
    message += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"رقم التقرير: #{report['id']}\n"
    message += f"المُبلغ: [{reporter_name}](tg://user?id={report['reporter_id']})\n"
    message += f"النوع: {report['target_type']}\n"
    message += f"الهدف: {report['target_id']}\n\n"
    message += f"📝 **السبب:**\n{report['reason']}\n\n"
    message += f"📅 التاريخ: {report['created_at']}\n"
    message += f"📌 الحالة: {report['status']}"
    
    if report['status'] == 'pending':
        buttons = [
            [Button.inline("✅ حل (حذف الهدف)", f"admin_mp_resolve:{report_id}:delete".encode())],
            [Button.inline("⚠️ حل (تحذير)", f"admin_mp_resolve:{report_id}:warn".encode())],
            [Button.inline("❌ رفض التقرير", f"admin_mp_resolve:{report_id}:dismiss".encode())]
        ]
    else:
        buttons = []
    
    if report['target_type'] == 'product':
        buttons.append([Button.inline("📦 عرض المنتج", f"admin_mp_product:{report['target_id']}".encode())])
    elif report['target_type'] == 'user':
        buttons.append([Button.inline("👤 عرض المستخدم", f"admin_mp_user:{report['target_id']}".encode())])
    
    buttons.append([Button.inline("🔙 رجوع", b"admin_mp_reports:pending:0")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def resolve_report_handler(event):
    """Resolve abuse report."""
    if not await require_marketplace_admin(event):
        return
    
    # Parse: admin_mp_resolve:report_id:action
    data = event.data.decode().split(':')
    report_id = int(data[1])
    action = data[2]
    
    report = await get_report_detail(report_id)
    if not report:
        return await event.answer("❌ التقرير غير موجود", alert=True)
    
    success = False
    
    if action == 'delete':
        # Delete target
        if report['target_type'] == 'product':
            from bot.handlers.admin.marketplace_products import delete_product_completely
            success = await delete_product_completely(report['target_id'], event.sender_id, "تم الإبلاغ عنه")
        elif report['target_type'] == 'comment':
            success = await delete_comment(report['target_id'])
        
        if success:
            await mark_report_resolved(report_id, event.sender_id, 'resolved', 'تم حذف الهدف')
            await event.answer("✅ تم حل التقرير وحذف الهدف", alert=True)
    
    elif action == 'warn':
        # Warn user
        success = await warn_user_from_report(report, event.sender_id)
        if success:
            await mark_report_resolved(report_id, event.sender_id, 'resolved', 'تم تحذير المستخدم')
            await event.answer("✅ تم حل التقرير وتحذير المستخدم", alert=True)
    
    elif action == 'dismiss':
        # Dismiss report
        await mark_report_resolved(report_id, event.sender_id, 'dismissed', 'تقرير غير صحيح')
        await event.answer("✅ تم رفض التقرير", alert=True)
        success = True
    
    if success:
        # Notify reporter
        try:
            from bot.core.client import client
            notify_msg = f"📋 **تحديث على تقريرك**\n\n"
            notify_msg += f"تقرير #{report_id}\n"
            notify_msg += f"الحالة: تم المعالجة\n\n"
            notify_msg += f"شكراً لمساعدتك في تحسين المجتمع."
            await client.send_message(report['reporter_id'], notify_msg, parse_mode='md')
        except:
            pass
        
        await report_detail_handler(event)
    else:
        await event.answer("❌ حدث خطأ", alert=True)


async def get_reports(status: str, limit: int, offset: int) -> tuple:
    """Get reports by status."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        async with db.execute('''
            SELECT * FROM marketplace_reports
            WHERE status = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        ''', (status, limit, offset)) as cursor:
            reports = [dict(row) async for row in cursor]
        
        async with db.execute('''
            SELECT COUNT(*) FROM marketplace_reports WHERE status = ?
        ''', (status,)) as cursor:
            result = await cursor.fetchone()
            total = result[0] if result else 0
        
        return reports, total


async def get_report_detail(report_id: int) -> dict:
    """Get report details."""
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        async with db.execute('SELECT * FROM marketplace_reports WHERE id = ?', (report_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def mark_report_resolved(report_id: int, admin_id: int, status: str, notes: str):
    """Mark report as resolved."""
    import time
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        await db.execute('''
            UPDATE marketplace_reports
            SET status = ?, reviewed_by = ?, reviewed_at = ?, admin_notes = ?
            WHERE id = ?
        ''', (status, admin_id, int(time.time()), notes, report_id))
        await db.commit()
    
    await log_admin_action(admin_id, f'resolve_report_{status}', 'report', str(report_id), notes)


async def delete_comment(comment_id: str) -> bool:
    """Delete a comment."""
    try:
        async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
            await db.execute('DELETE FROM marketplace_comments WHERE id = ?', (comment_id,))
            await db.commit()
        return True
    except:
        return False


async def warn_user_from_report(report: dict, admin_id: int) -> bool:
    """Warn user based on report."""
    try:
        # Get user_id from target
        if report['target_type'] == 'product':
            product = await database.get_marketplace_product(report['target_id'])
            user_id = product['owner_id'] if product else None
        elif report['target_type'] == 'comment':
            async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
                async with db.execute('SELECT user_id FROM marketplace_comments WHERE id = ?', (report['target_id'],)) as cursor:
                    row = await cursor.fetchone()
                    user_id = row[0] if row else None
        else:
            user_id = int(report['target_id'])
        
        if not user_id:
            return False
        
        # Add warning
        from bot.services.profanity_filter import increment_user_warnings
        warnings = await increment_user_warnings(user_id)
        
        # Notify user
        try:
            from bot.core.client import client
            notify_msg = f"⚠️ **تحذير**\n\n"
            notify_msg += f"تم الإبلاغ عن محتوى لك.\n"
            notify_msg += f"السبب: {report['reason']}\n\n"
            notify_msg += f"التحذيرات: {warnings}/3\n\n"
            notify_msg += f"يرجى الالتزام بالقواعد."
            await client.send_message(user_id, notify_msg, parse_mode='md')
        except:
            pass
        
        return True
    except Exception as e:
        print(f"Error warning user: {e}")
        return False


print("✅ Marketplace reports admin loaded.")
