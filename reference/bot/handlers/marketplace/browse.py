# bot/handlers/marketplace/browse.py
# Browse and view marketplace products

from telethon import events, Button
from bot.core import database
from bot.core.config import settings
from bot.services import marketplace_service
from bot.services.user_service import check_user_status

ITEMS_PER_PAGE = 6


def setup(client):
    client.add_event_handler(marketplace_home_handler, events.CallbackQuery(pattern=b"marketplace_home"))
    client.add_event_handler(marketplace_guide_pages_handler, events.CallbackQuery(pattern=b"mp_guide:\\d+"))
    client.add_event_handler(marketplace_guide_handler, events.CallbackQuery(pattern=b"mp_guide$"))
    client.add_event_handler(categories_handler, events.CallbackQuery(pattern=b"marketplace_categories"))
    client.add_event_handler(category_products_handler, events.CallbackQuery(pattern=b"mp_cat:"))
    client.add_event_handler(product_details_handler, events.CallbackQuery(pattern=b"mp_view:"))
    client.add_event_handler(browse_products_handler, events.CallbackQuery(pattern=b"mp_browse:"))


async def marketplace_home_handler(event):
    """Main marketplace home page."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Check marketplace ban
    from bot.services.profanity_filter import check_user_ban
    is_banned, ban_reason = await check_user_ban(sender_id, 'any')
    if is_banned:
        return await event.answer(ban_reason, alert=True)
    
    # Get stats
    stats = await database.get_marketplace_stats()
    
    message = f"🛒 **مرحباً بك في الماركت** {settings.MARKETPLACE_VERSION}\n\n"
    message += "اكتشف آلاف البوتات الجاهزة من المجتمع، أو شارك إبداعاتك مع الآخرين\n\n"
    message += "📊 **الإحصائيات**\n"
    message += f"• المنتجات: {stats['total_products']}\n"
    message += f"• التحميلات: {stats['total_downloads']}\n"
    message += f"• المطورين: {stats['total_developers']}\n\n"
    message += f"**⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll**"
    
    buttons = [
        [Button.inline("📖 شرح الماركت", b"mp_guide")],
        [Button.inline("🏆 أفضل مطورين", b"show_top_developers")],
        [Button.inline("📦 تصفح كل المنتجات", b"mp_browse:all:0")],
        [Button.inline("🔥 الأكثر تحميلاً", b"mp_browse:downloads:0"),
         Button.inline("⭐ الأعلى تقييماً", b"mp_browse:rating:0")],
        [Button.inline("🆕 الأحدث", b"mp_browse:newest:0"),
         Button.inline("📂 التصنيفات", b"marketplace_categories")],
        [Button.inline("📤 رفع منتج جديد", b"mp_upload_start")],
        [Button.inline("📦 منتجاتي", b"mp_my_products:0"),
         Button.inline("📥 تحميلاتي", b"mp_my_downloads:0")],
        [Button.inline("🔙 رجوع للقائمة الرئيسية", b"main_menu")]
    ]
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def marketplace_guide_handler(event):
    """Complete marketplace guide - Professional explanation."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Part 1: Introduction
    message = f"📖 **دليل الماركت الشامل** {settings.MARKETPLACE_VERSION}\n"
    message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    message += "**ما هو الماركت؟**\n"
    message += "الماركت هو منصة مجتمعية متكاملة تتيح لك تبادل البوتات والسكريبتات مع آلاف المطورين. "
    message += "سواء كنت تبحث عن حلول جاهزة لمشاريعك، أو ترغب في مشاركة إبداعاتك مع المجتمع، "
    message += "الماركت يوفر لك بيئة آمنة واحترافية لذلك.\n\n"
    
    message += f"**🎉 الإصدار الأول ({settings.MARKETPLACE_VERSION})**\n"
    message += "هذا هو الإصدار الأول من الماركت! نحن متحمسون لإطلاق هذه المنصة "
    message += "التي ستجمع المطورين والمبدعين في مكان واحد. نعمل باستمرار على تحسين "
    message += "التجربة وإضافة مميزات جديدة.\n\n"
    
    message += "**لماذا تستخدم الماركت؟**\n"
    message += "• وفّر ساعات من البرمجة باستخدام حلول جاهزة\n"
    message += "• تعلّم من كود المطورين الآخرين\n"
    message += "• شارك مشاريعك واحصل على تقييمات\n"
    message += "• اكتشف أفكار جديدة ومبتكرة\n"
    message += "• انضم لمجتمع نشط من المطورين\n\n"
    
    message += f"**⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll**"
    
    buttons = [
        [Button.inline("▶️ التالي: كيف تتصفح المنتجات", b"mp_guide:2")],
        [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
    ]
    
    try:
        await event.edit(message, buttons=buttons, parse_mode='md')
    except Exception:
        pass


async def marketplace_guide_pages_handler(event):
    """Handle guide pages navigation."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Get page number
    page = int(event.data.decode().split(':')[1])
    
    if page == 2:
        # Browsing guide
        message = "📖 **دليل الماركت - التصفح**\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        message += "**🔍 طرق التصفح المتاحة:**\n\n"
        
        message += "**1. تصفح كل المنتجات**\n"
        message += "يعرض جميع المنتجات مرتبة حسب الجودة الشاملة (Quality Score). "
        message += "هذا الترتيب يأخذ في الاعتبار التحميلات، التقييمات، المشاهدات، والتعليقات لضمان ظهور أفضل المنتجات أولاً.\n\n"
        
        message += "**2. الأكثر تحميلاً 🔥**\n"
        message += "المنتجات الأكثر شعبية بين المستخدمين. إذا كنت تبحث عن حلول مجربة وموثوقة، "
        message += "هذا القسم يعرض المنتجات التي حملها آلاف المستخدمين.\n\n"
        
        message += "**3. الأعلى تقييماً ⭐**\n"
        message += "المنتجات التي حصلت على أعلى نسبة إعجاب من المستخدمين. "
        message += "يتم احتساب التقييم بناءً على نسبة الإعجاب (👍) مقابل عدم الإعجاب (👎).\n\n"
        
        message += "**4. الأحدث 🆕**\n"
        message += "آخر المنتجات المضافة للماركت. اكتشف الإبداعات الجديدة والأفكار المبتكرة.\n\n"
        
        message += "**5. التصنيفات 📂**\n"
        message += "تصفح حسب نوع البوت: متاجر، ألعاب، أدوات، ترفيه، وغيرها. "
        message += "يسهل عليك إيجاد ما تبحث عنه بالضبط.\n\n"
        
        message += f"**⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll**"
        
        buttons = [
            [Button.inline("◀️ السابق", b"mp_guide"),
             Button.inline("▶️ التالي", b"mp_guide:3")],
            [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
        ]
        
    elif page == 3:
        # Download guide
        message = "📖 **دليل الماركت - التحميل**\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        message += "**📥 كيف تحمل منتج؟**\n\n"
        
        message += "**الخطوة 1: اختر المنتج**\n"
        message += "تصفح المنتجات واضغط على المنتج الذي يعجبك لعرض تفاصيله الكاملة.\n\n"
        
        message += "**الخطوة 2: راجع التفاصيل**\n"
        message += "ستجد معلومات شاملة عن المنتج:\n"
        message += "• الوصف والمميزات\n"
        message += "• عدد الملفات والحجم\n"
        message += "• التقييمات والتعليقات\n"
        message += "• إحصائيات التحميل\n"
        message += "• معلومات المطور\n\n"
        
        message += "**الخطوة 3: التحميل**\n"
        message += "اضغط على زر \"📥 تحميل الآن\" وسيتم:\n"
        message += "• نسخ جميع ملفات البوت إلى حسابك\n"
        message += "• إنشاء مجلد خاص بالمنتج\n"
        message += "• تسجيل التحميل في سجلك\n\n"
        
        message += "**الخطوة 4: التثبيت**\n"
        message += "بعد التحميل:\n"
        message += "1. افتح مجلد البوت من قائمة الملفات\n"
        message += "2. راجع الملفات وعدّل الإعدادات حسب احتياجك\n"
        message += "3. شغّل البوت واستمتع!\n\n"
        
        message += "**⚠️ نصائح أمان:**\n"
        message += "• راجع الكود دائماً قبل التشغيل\n"
        message += "• تحقق من التقييمات والتعليقات\n"
        message += "• لا تشارك معلومات حساسة\n\n"
        
        message += f"**⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll**"
        
        buttons = [
            [Button.inline("◀️ السابق", b"mp_guide:2"),
             Button.inline("▶️ التالي", b"mp_guide:4")],
            [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
        ]
        
    elif page == 4:
        # Upload guide
        message = "📖 **دليل الماركت - الرفع**\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        message += "**📤 كيف ترفع منتجك؟**\n\n"
        
        message += "**المتطلبات:**\n"
        message += "• بوت جاهز ومختبر\n"
        message += "• ملفات نظيفة وآمنة\n"
        message += "• وصف واضح ومفصل\n\n"
        
        message += "**خطوات الرفع:**\n\n"
        
        message += "**1. ابدأ عملية الرفع**\n"
        message += "اضغط على \"📤 رفع منتج جديد\" من الصفحة الرئيسية.\n\n"
        
        message += "**2. أدخل المعلومات الأساسية**\n"
        message += "• العنوان: اسم واضح وجذاب\n"
        message += "• الوصف: شرح مفصل للمميزات\n"
        message += "• التصنيف: اختر الفئة المناسبة\n\n"
        
        message += "**3. ارفع الملفات**\n"
        message += "يمكنك رفع:\n"
        message += "• ملف واحد (.php)\n"
        message += "• عدة ملفات منفصلة\n"
        message += "• ملف مضغوط (.zip)\n\n"
        
        message += "**4. المراجعة والنشر**\n"
        message += "راجع جميع المعلومات ثم اضغط \"✅ نشر المنتج\".\n\n"
        
        message += "**📊 بعد النشر:**\n"
        message += "• تابع إحصائيات منتجك\n"
        message += "• رد على التعليقات\n"
        message += "• حدّث المنتج عند الحاجة\n\n"
        
        message += f"**⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll**"
        
        buttons = [
            [Button.inline("◀️ السابق", b"mp_guide:3"),
             Button.inline("▶️ التالي", b"mp_guide:5")],
            [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
        ]
        
    elif page == 5:
        # Reviews and ratings
        message = "📖 **دليل الماركت - التقييمات**\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        message += "**⭐ نظام التقييمات**\n\n"
        
        message += "**كيف تقيّم منتج؟**\n"
        message += "بعد تحميل أي منتج، يمكنك تقييمه بطريقتين:\n\n"
        
        message += "**1. التقييم السريع**\n"
        message += "• 👍 أعجبني: إذا كان المنتج مفيد وجيد\n"
        message += "• 👎 لم يعجبني: إذا كان هناك مشاكل\n\n"
        
        message += "**2. كتابة تعليق**\n"
        message += "شارك تجربتك التفصيلية:\n"
        message += "• ما الذي أعجبك؟\n"
        message += "• هل واجهت مشاكل؟\n"
        message += "• اقتراحات للتحسين\n\n"
        
        message += "**💬 التعليقات:**\n"
        message += "• يمكنك كتابة حتى 3 تعليقات لكل منتج\n"
        message += "• الحد الأقصى: 500 حرف\n"
        message += "• كن محترماً وبناءً\n\n"
        
        message += "**🎯 أهمية التقييمات:**\n"
        message += "• تساعد المطورين على التحسين\n"
        message += "• تساعد المستخدمين على الاختيار\n"
        message += "• تحسن ترتيب المنتجات الجيدة\n\n"
        
        message += "**⚠️ قواعد التقييم:**\n"
        message += "• لا يمكنك تقييم منتجك الخاص\n"
        message += "• تقييم واحد لكل منتج\n"
        message += "• ممنوع الإساءة أو السب\n\n"
        
        message += f"**⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll**"
        
        buttons = [
            [Button.inline("◀️ السابق", b"mp_guide:4"),
             Button.inline("▶️ التالي", b"mp_guide:6")],
            [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
        ]
        
    elif page == 6:
        # Categories explanation
        message = "📖 **دليل الماركت - التصنيفات**\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        message += "**📂 التصنيفات المتاحة:**\n\n"
        
        message += "**🛒 متاجر (Stores)**\n"
        message += "بوتات المتاجر الإلكترونية، أنظمة الطلبات، إدارة المنتجات، "
        message += "سلة التسوق، والدفع الإلكتروني.\n\n"
        
        message += "**🎮 ألعاب (Games)**\n"
        message += "ألعاب تفاعلية، ألغاز، مسابقات، ألعاب جماعية، "
        message += "وأنظمة النقاط والمكافآت.\n\n"
        
        message += "**🔧 أدوات (Tools)**\n"
        message += "أدوات مساعدة، محولات، حاسبات، أدوات إدارة، "
        message += "وسكريبتات مفيدة للمطورين.\n\n"
        
        message += "**🎭 ترفيه (Entertainment)**\n"
        message += "بوتات الميمز، النكت، الصور، الموسيقى، "
        message += "والمحتوى الترفيهي.\n\n"
        
        message += "**📚 تعليمية (Educational)**\n"
        message += "بوتات تعليمية، دورات، اختبارات، قواميس، "
        message += "ومصادر تعليمية.\n\n"
        
        message += "**💼 أعمال (Business)**\n"
        message += "أنظمة CRM، إدارة المشاريع، الفواتير، "
        message += "وأدوات الإنتاجية.\n\n"
        
        message += "**📰 أخبار (News)**\n"
        message += "بوتات الأخبار، RSS feeds، تنبيهات، "
        message += "ومتابعة المواقع.\n\n"
        
        message += "**🎨 أخرى (Other)**\n"
        message += "أي منتجات لا تندرج تحت التصنيفات السابقة.\n\n"
        
        message += f"**⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll**"
        
        buttons = [
            [Button.inline("◀️ السابق", b"mp_guide:5"),
             Button.inline("▶️ التالي", b"mp_guide:7")],
            [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
        ]
        
    elif page == 7:
        # Security and rules
        message = "📖 **دليل الماركت - الأمان والقواعد**\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        message += "**🔒 الأمان أولاً**\n\n"
        
        message += "**للمستخدمين:**\n"
        message += "• راجع الكود دائماً قبل التشغيل\n"
        message += "• تحقق من التقييمات والتعليقات\n"
        message += "• لا تشغّل أكواد مشبوهة\n"
        message += "• احذر من الملفات الضارة\n"
        message += "• أبلغ عن أي محتوى مخالف\n\n"
        
        message += "**للمطورين:**\n"
        message += "• لا ترفع أكواد ضارة أو خبيثة\n"
        message += "• تأكد من نظافة الكود\n"
        message += "• اكتب وصف واضح وصادق\n"
        message += "• احترم حقوق الملكية\n"
        message += "• رد على التعليقات والاستفسارات\n\n"
        
        message += "**⚖️ القواعد العامة:**\n\n"
        
        message += "**ممنوع منعاً باتاً:**\n"
        message += "• رفع فيروسات أو برمجيات ضارة\n"
        message += "• سرقة أكواد الآخرين\n"
        message += "• الإساءة في التعليقات\n"
        message += "• التقييمات الوهمية\n"
        message += "• المحتوى المخالف للآداب\n\n"
        
        message += "**العقوبات:**\n"
        message += "• تحذير أول: تنبيه\n"
        message += "• تحذير ثاني: حظر مؤقت (24 ساعة)\n"
        message += "• تحذير ثالث: حظر مؤقت (7 أيام)\n"
        message += "• مخالفة خطيرة: حظر دائم\n\n"
        
        message += f"**⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll**"
        
        buttons = [
            [Button.inline("◀️ السابق", b"mp_guide:6"),
             Button.inline("▶️ التالي", b"mp_guide:8")],
            [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
        ]
        
    elif page == 8:
        # Tips and best practices
        message = "📖 **دليل الماركت - نصائح احترافية**\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        message += "**💡 نصائح للمستخدمين:**\n\n"
        
        message += "**1. اختر بحكمة**\n"
        message += "• راجع التقييمات والتعليقات\n"
        message += "• تحقق من عدد التحميلات\n"
        message += "• اقرأ الوصف بالكامل\n\n"
        
        message += "**2. اختبر قبل الاستخدام**\n"
        message += "• جرب البوت في بيئة آمنة\n"
        message += "• تأكد من عمل جميع المميزات\n"
        message += "• راجع الإعدادات\n\n"
        
        message += "**3. شارك تجربتك**\n"
        message += "• قيّم المنتجات التي تحملها\n"
        message += "• اكتب تعليقات مفيدة\n"
        message += "• ساعد المطورين على التحسين\n\n"
        
        message += "**💎 نصائح للمطورين:**\n\n"
        
        message += "**1. اهتم بالجودة**\n"
        message += "• اكتب كود نظيف ومنظم\n"
        message += "• أضف تعليقات توضيحية\n"
        message += "• اختبر جيداً قبل الرفع\n\n"
        
        message += "**2. الوصف مهم**\n"
        message += "• اشرح المميزات بوضوح\n"
        message += "• أضف أمثلة وصور\n"
        message += "• اذكر المتطلبات\n\n"
        
        message += "**3. تفاعل مع المجتمع**\n"
        message += "• رد على التعليقات\n"
        message += "• حدّث منتجاتك\n"
        message += "• اصلح الأخطاء بسرعة\n\n"
        
        message += "**🎯 كيف تحصل على تقييمات عالية؟**\n"
        message += "• جودة الكود\n"
        message += "• وضوح الوصف\n"
        message += "• سهولة الاستخدام\n"
        message += "• الدعم الفني\n"
        message += "• التحديثات المستمرة\n\n"
        
        message += f"**⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll**"
        
        buttons = [
            [Button.inline("◀️ السابق", b"mp_guide:7"),
             Button.inline("▶️ الخاتمة", b"mp_guide:9")],
            [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
        ]
        
    elif page == 9:
        # Final page
        message = "📖 **دليل الماركت - الخاتمة**\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        message += "**🎉 تهانينا!**\n\n"
        message += "أنت الآن جاهز لاستخدام الماركت بشكل احترافي. "
        message += "سواء كنت تبحث عن حلول جاهزة أو ترغب في مشاركة إبداعاتك، "
        message += "الماركت يوفر لك كل ما تحتاجه.\n\n"
        
        message += "**📊 إحصائيات الماركت:**\n"
        stats = await database.get_marketplace_stats()
        message += f"• {stats['total_products']} منتج متاح\n"
        message += f"• {stats['total_downloads']} عملية تحميل\n"
        message += f"• {stats['total_developers']} مطور نشط\n\n"
        
        message += f"**🎯 الإصدار الحالي: {settings.MARKETPLACE_VERSION}**\n"
        message += "هذا هو الإصدار الأول من الماركت! نحن نعمل باستمرار على:\n"
        message += "• إضافة مميزات جديدة\n"
        message += "• تحسين الأداء والأمان\n"
        message += "• الاستماع لاقتراحاتكم\n"
        message += "• بناء مجتمع أقوى\n\n"
        
        message += "**🚀 ابدأ الآن:**\n"
        message += "• تصفح المنتجات المتاحة\n"
        message += "• حمّل ما يناسبك\n"
        message += "• شارك منتجاتك\n"
        message += "• انضم للمجتمع\n\n"
        
        message += "**💬 هل تحتاج مساعدة؟**\n"
        message += "تواصل معنا:\n"
        message += "• @M3_mo2\n"
        message += "• @u_w_ll\n\n"
        
        message += f"**🌟 شكراً لاستخدامك الماركت {settings.MARKETPLACE_VERSION}!**\n\n"
        message += "نتمنى لك تجربة رائعة ومثمرة. "
        message += "معاً نبني مجتمع أقوى من المطورين والمبدعين.\n\n"
        
        message += f"**⬢ Build Market {settings.MARKETPLACE_VERSION} ⌁ @M3_mo2 & @u_w_ll**"
        
        buttons = [
            [Button.inline("◀️ السابق", b"mp_guide:8"),
             Button.inline("🔄 إعادة القراءة", b"mp_guide")],
            [Button.inline("🚀 ابدأ التصفح الآن", b"mp_browse:all:0")],
            [Button.inline("🔙 رجوع للماركت", b"marketplace_home")]
        ]
    
    else:
        # Default to first page
        return await marketplace_guide_handler(event)
    
    try:
        await event.edit(message, buttons=buttons, parse_mode='md')
    except Exception:
        pass


async def categories_handler(event):
    """Show all categories."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Check marketplace ban
    from bot.services.profanity_filter import check_user_ban
    is_banned, ban_reason = await check_user_ban(sender_id, 'any')
    if is_banned:
        return await event.answer(ban_reason, alert=True)
    
    categories = await database.get_marketplace_categories()
    
    message = "📂 **التصنيفات**\n\nاختر التصنيف المناسب لك:"
    
    # Create grid buttons (2 per row)
    buttons = []
    row = []
    for cat in categories:
        btn_text = f"{cat['icon']} {cat['name_ar']}\n({cat['product_count']} منتج)"
        btn_data = f"mp_cat:{cat['category_id']}:0".encode()
        row.append(Button.inline(btn_text, btn_data))
        
        if len(row) == 2:
            buttons.append(row)
            row = []
    
    if row:  # Add remaining button
        buttons.append(row)
    
    buttons.append([Button.inline("🔙 رجوع", b"marketplace_home")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def category_products_handler(event):
    """Show products in a category."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Check marketplace ban
    from bot.services.profanity_filter import check_user_ban
    is_banned, ban_reason = await check_user_ban(sender_id, 'any')
    if is_banned:
        return await event.answer(ban_reason, alert=True)
    
    # Parse data: mp_cat:category_id:page
    data = event.data.decode().split(':')
    category_id = data[1]
    page = int(data[2])
    
    # Get category
    category = await database.get_marketplace_category(category_id)
    if not category:
        return await event.answer("❌ التصنيف غير موجود", alert=True)
    
    # Get products
    offset = page * ITEMS_PER_PAGE
    products = await database.search_marketplace_products(
        category=category_id,
        sort_by='quality',
        limit=ITEMS_PER_PAGE,
        offset=offset
    )
    
    # Count total
    total = await database.count_marketplace_products(category=category_id)
    total_pages = (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    
    if not products:
        message = f"{category['icon']} **{category['name_ar']}**\n\n"
        message += "لا توجد منتجات في هذا التصنيف حالياً."
        buttons = [[Button.inline("🔙 رجوع", b"marketplace_categories")]]
        return await event.edit(message, buttons=buttons, parse_mode='md')
    
    message = f"{category['icon']} **{category['name_ar']}** ({total} منتج)\n\n"
    message += f"الصفحة {page + 1} من {total_pages}\n\n"
    
    # Product buttons
    buttons = []
    for product in products:
        card = await marketplace_service.format_product_card(product, include_stats=False)
        btn_data = f"mp_view:{product['product_id']}".encode()
        buttons.append([Button.inline(f"📦 {product['title']}", btn_data)])
    
    # Navigation buttons
    nav_row = []
    if page > 0:
        nav_row.append(Button.inline("⬅️ السابق", f"mp_cat:{category_id}:{page-1}".encode()))
    if page < total_pages - 1:
        nav_row.append(Button.inline("➡️ التالي", f"mp_cat:{category_id}:{page+1}".encode()))
    
    if nav_row:
        buttons.append(nav_row)
    
    buttons.append([Button.inline("🔙 رجوع", b"marketplace_categories")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def browse_products_handler(event):
    """Browse products with different sorting."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Check marketplace ban
    from bot.services.profanity_filter import check_user_ban
    is_banned, ban_reason = await check_user_ban(sender_id, 'any')
    if is_banned:
        return await event.answer(ban_reason, alert=True)
    
    # Parse data: mp_browse:sort_type:page
    data = event.data.decode().split(':')
    sort_type = data[1]
    page = int(data[2]) if len(data) > 2 else 0
    
    # Determine sort
    sort_map = {
        'all': ('quality', '📦 جميع المنتجات'),
        'downloads': ('downloads', '🔥 الأكثر تحميلاً'),
        'rating': ('rating', '⭐ الأعلى تقييماً'),
        'newest': ('newest', '🆕 الأحدث')
    }
    
    sort_by, title = sort_map.get(sort_type, ('quality', 'المنتجات'))
    
    # Get products
    offset = page * ITEMS_PER_PAGE
    products = await database.search_marketplace_products(
        sort_by=sort_by,
        limit=ITEMS_PER_PAGE,
        offset=offset
    )
    
    # Count total
    total = await database.count_marketplace_products()
    total_pages = (total + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    
    if not products:
        message = f"{title}\n\nلا توجد منتجات حالياً."
        buttons = [[Button.inline("🔙 رجوع", b"marketplace_home")]]
        return await event.edit(message, buttons=buttons, parse_mode='md')
    
    message = f"{title}\n\n"
    message += f"الصفحة {page + 1} من {total_pages}\n\n"
    
    # Product buttons
    buttons = []
    for product in products:
        btn_data = f"mp_view:{product['product_id']}".encode()
        buttons.append([Button.inline(f"📦 {product['title']}", btn_data)])
    
    # Navigation
    nav_row = []
    if page > 0:
        nav_row.append(Button.inline("⬅️ السابق", f"mp_browse:{sort_type}:{page-1}".encode()))
    if page < total_pages - 1:
        nav_row.append(Button.inline("➡️ التالي", f"mp_browse:{sort_type}:{page+1}".encode()))
    
    if nav_row:
        buttons.append(nav_row)
    
    buttons.append([Button.inline("🔙 رجوع", b"marketplace_home")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


async def product_details_handler(event):
    """Show full product details."""
    sender_id = event.sender_id
    
    if check_user_status(sender_id) == 'banned':
        return await event.answer("🚫 أنت محظور.", alert=True)
    
    # Check marketplace ban
    from bot.services.profanity_filter import check_user_ban
    is_banned, ban_reason = await check_user_ban(sender_id, 'any')
    if is_banned:
        return await event.answer(ban_reason, alert=True)
    
    # Parse data: mp_view:product_id
    product_id = event.data.decode().split(':')[1]
    
    # Get product
    product = await database.get_marketplace_product(product_id)
    if not product:
        return await event.answer("❌ المنتج غير موجود", alert=True)
    
    # Increment views (with 10-hour cooldown)
    await database.increment_product_views(product_id, sender_id)
    
    # Format details
    message = await marketplace_service.format_product_details(product, sender_id)
    
    # Get user's review
    user_review = await database.get_user_review(product_id, sender_id)
    
    # Buttons
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
    from urllib.parse import quote
    bot_username = (await event.client.get_me()).username
    product_url = f"https://t.me/{bot_username}?start=mp_{product_id}"
    share_text = f"شاهد هذا المنتج: {product['title']}"
    share_url = f"https://t.me/share/url?url={quote(product_url)}&text={quote(share_text)}"
    buttons.append([Button.url("📤 مشاركة المنتج", share_url)])
    
    # If owner, show manage button
    if product['owner_id'] == sender_id:
        buttons.append([Button.inline("⚙️ إدارة المنتج", f"mp_manage:{product_id}".encode())])
    
    buttons.append([Button.inline("🔙 رجوع", b"marketplace_home")])
    
    await event.edit(message, buttons=buttons, parse_mode='md')


print("✅ Marketplace browse handlers loaded.")
