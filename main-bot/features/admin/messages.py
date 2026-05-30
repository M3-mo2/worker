NO_WORKERS = (
    "مفيش Workers مسجلين لسه.\n"
    "\n"
    "أضف Worker الأول:"
)

WORKERS_LIST = "⚙️ الـ Workers ({count})\n"

WORKER_DETAILS = (
    "🖥 Worker #{id}\n"
    "\n"
    "🔗 الرابط: {url}\n"
    "📊 الحالة: {status}\n"
    "🤖 عدد البوتات: {bots_count}\n"
    "🕐 آخر فحص: {last_check}"
)

ADD_WORKER_ASK_URL = (
    "➕ إضافة Worker جديد\n"
    "\n"
    "ابعت رابط الـ Worker:\n"
    "مثال: `https://worker-1.up.railway.app`"
)

ADD_WORKER_ASK_SECRET = (
    "✅ الرابط: {url}\n"
    "\n"
    "🔑 ابعت الـ INTERNAL_SECRET بتاع الـ Worker:"
)

ADD_WORKER_SUCCESS = (
    "✅ تم إضافة الـ Worker!\n"
    "\n"
    "🔗 الرابط: {url}\n"
    "📊 الحالة: نشط"
)

ADD_WORKER_EXISTS = (
    "⚠️ الـ Worker ده مسجل بالفعل\n"
    "\n"
    "🔗 الرابط: {url}"
)

DELETE_WORKER_CONFIRM = (
    "⚠️ حذف Worker #{id}\n"
    "\n"
    "🔗 الرابط: {url}\n"
    "🤖 عدد البوتات عليه: {bots_count}\n"
    "\n"
    "لو حذفته، البوتات عليه مش هتشتغل."
)

DELETE_WORKER_DONE = "🗑 تم حذف Worker #{id}"

DELETE_WORKER_HAS_BOTS = (
    "❌ مش ممكن تحذف الـ Worker ده\n"
    "\n"
    "عليه {count} بوت شغال. نقّل البوتات الأول."
)

MAINTENANCE_ON = "🔧 Worker #{id} دلوقتي في وضع الصيانة"
MAINTENANCE_OFF = "✅ Worker #{id} رجع يشتغل تاني"

STATUS_ACTIVE = "🟢 نشط"
STATUS_MAINTENANCE = "🔧 صيانة"
STATUS_DEAD = "🔴 ميت"

HEALTH_CHECK_RUNNING = "🔍 جاري فحص الـ Workers..."
HEALTH_CHECK_DONE = (
    "✅ تم فحص الـ Workers\n"
    "\n"
    "{results}"
)
