from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# === Reply Keyboard (دائم في الأسفل) ===

def main_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🚀 نشر بوت"),
                KeyboardButton(text="📋 بوتاتي"),
            ],
            [
                KeyboardButton(text="❓ مساعدة"),
            ]
        ],
        resize_keyboard=True
    )


# === كيبوردات قائمة البوتات ===

def bots_list_keyboard(bots: list) -> InlineKeyboardMarkup:
    buttons = []
    for bot in bots:
        icon = "🟢" if bot["status"] == "running" else "🔴"
        name = bot["bot_username"] or f"Bot #{bot['id']}"
        buttons.append([InlineKeyboardButton(
            text=f"{icon} {name}",
            callback_data=f"manage:view:{bot['id']}"
        )])
    buttons.append([InlineKeyboardButton(
        text="➕ نشر بوت جديد",
        callback_data="deploy:new"
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === كيبوردات إدارة بوت واحد ===

def bot_actions_keyboard(bot_id: int, status: str) -> InlineKeyboardMarkup:
    buttons = []
    if status == "running":
        buttons.append(InlineKeyboardButton(text="⏸ إيقاف", callback_data=f"manage:stop:{bot_id}"))
    else:
        buttons.append(InlineKeyboardButton(text="▶ تشغيل", callback_data=f"manage:start:{bot_id}"))

    buttons.append(InlineKeyboardButton(text="🔄 إعادة تشغيل", callback_data=f"manage:restart:{bot_id}"))
    buttons.append(InlineKeyboardButton(text="🗑 حذف", callback_data=f"manage:delete:{bot_id}"))

    return InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [InlineKeyboardButton(text="🔙 رجوع", callback_data="manage:back")]
    ])


# === كيبوردات التأكيد ===

def confirm_keyboard(action: str, bot_id: int) -> InlineKeyboardMarkup:
    if action == "delete":
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🗑 احذف البوت", callback_data=f"manage:confirm:delete:{bot_id}"),
            InlineKeyboardButton(text="❌ لا خلاص", callback_data=f"manage:cancel:{bot_id}"),
        ]])
    elif action == "stop":
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="⏸ وقّف البوت", callback_data=f"manage:confirm:stop:{bot_id}"),
            InlineKeyboardButton(text="❌ لا خلاص", callback_data=f"manage:cancel:{bot_id}"),
        ]])
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ أيوه", callback_data=f"manage:confirm:{action}:{bot_id}"),
        InlineKeyboardButton(text="❌ لا", callback_data=f"manage:cancel:{bot_id}"),
    ]])


# === كيبورد رجوع ===

def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔙 رجوع", callback_data="manage:back")
    ]])


# === كيبورد نشر بوت ===

def deploy_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="❌ إلغاء", callback_data="deploy:cancel")
    ]])


# === كيبورد بعد النشر ===

def deploy_success_keyboard(bot_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 فتح البوت", url=bot_link)],
        [
            InlineKeyboardButton(text="📋 بوتاتي", callback_data="manage:list"),
            InlineKeyboardButton(text="🚀 نشر بوت تاني", callback_data="deploy:new"),
        ]
    ])


# === كيبورد بعد الإيقاف ===

def stop_done_keyboard(bot_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📋 بوتاتي", callback_data="manage:list"),
        InlineKeyboardButton(text="▶ شغّله تاني", callback_data=f"manage:start:{bot_id}"),
    ]])


# === كيبورد بعد الحذف ===

def delete_done_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📋 بوتاتي", callback_data="manage:list"),
        InlineKeyboardButton(text="🚀 نشر بوت جديد", callback_data="deploy:new"),
    ]])


# === كيبورد بعد الريستارت ===

def restart_done_keyboard(bot_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 فتح البوت", url=bot_link)],
        [InlineKeyboardButton(text="📋 بوتاتي", callback_data="manage:list")]
    ])


# === كيبورد إلغاء عام ===

def cancel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="❌ إلغاء", callback_data="deploy:cancel")
    ]])


# === كيبورد خطأ ===

def error_retry_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔄 جرب تاني", callback_data="deploy:new"),
        InlineKeyboardButton(text="📋 بوتاتي", callback_data="manage:list"),
    ]])
