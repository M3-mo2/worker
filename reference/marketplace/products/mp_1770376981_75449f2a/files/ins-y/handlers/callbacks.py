from core.bot import bot
from core.constants import Callbacks, Messages
from handlers.video import user_sessions
from handlers.playlist import playlist_sessions

@bot.callback_query_handler(func=lambda call: call.data == Callbacks.CANCEL)
def handle_cancel(call):
    chat_id = call.message.chat.id
    
    if chat_id in user_sessions:
        del user_sessions[chat_id]
    
    if chat_id in playlist_sessions:
        del playlist_sessions[chat_id]
    
    bot.edit_message_text(
        Messages.CANCELLED,
        chat_id,
        call.message.message_id
    )
    
    bot.answer_callback_query(call.id)
