import asyncio
from pathlib import Path
from core.bot import bot
from core.config import config
from core.constants import Messages, Callbacks
from services.downloader import downloader
from utils.keyboards import keyboard_builder


user_sessions = {}


def handle_video_url(message, url):
    user_sessions[message.chat.id] = {"url": url, "type": "video"}
    
    bot.send_message(
        message.chat.id,
        "Select quality",
        reply_markup=keyboard_builder.video_quality_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith(Callbacks.VIDEO_PREFIX) or call.data.startswith(Callbacks.AUDIO_PREFIX))
def handle_quality_selection(call):
    chat_id = call.message.chat.id
    
    if chat_id not in user_sessions:
        bot.answer_callback_query(call.id, "Session expired")
        return
    
    action, quality = Callbacks.parse_callback(call.data)
    is_audio = action == Callbacks.AUDIO_PREFIX
    
    bot.edit_message_text(
        Messages.DOWNLOADING,
        chat_id,
        call.message.message_id
    )
    
    url = user_sessions[chat_id]["url"]
    
    try:
        result = asyncio.run(
            downloader.download(url, quality, is_audio)
        )
        
        if not result:
            bot.edit_message_text(Messages.ERROR, chat_id, call.message.message_id)
            return
        
        file_path = Path(result.get("file_path", ""))
        
        if not file_path.exists():
            bot.edit_message_text(Messages.ERROR, chat_id, call.message.message_id)
            return
        
        file_size_mb = downloader.get_file_size_mb(file_path)
        
        if file_size_mb > config.MAX_FILE_SIZE_MB:
            bot.edit_message_text(
                Messages.FILE_TOO_LARGE.format(size=config.MAX_FILE_SIZE_MB),
                chat_id,
                call.message.message_id
            )
            downloader.cleanup_file(file_path)
            return
        
        bot.edit_message_text(Messages.UPLOADING, chat_id, call.message.message_id)
        
        with open(file_path, 'rb') as file:
            if is_audio:
                bot.send_audio(chat_id, file)
            else:
                bot.send_video(chat_id, file)
        
        bot.edit_message_text(Messages.DONE, chat_id, call.message.message_id)
        
        downloader.cleanup_file(file_path)
        
    except Exception as e:
        print(f"Error: {e}")
        bot.edit_message_text(Messages.ERROR, chat_id, call.message.message_id)
    
    finally:
        if chat_id in user_sessions:
            del user_sessions[chat_id]
    
    bot.answer_callback_query(call.id)
