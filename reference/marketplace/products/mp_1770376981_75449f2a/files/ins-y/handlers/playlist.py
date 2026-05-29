import asyncio
from pathlib import Path
from core.bot import bot
from core.config import config
from core.constants import Messages, Callbacks
from services.downloader import downloader
from utils.keyboards import keyboard_builder


playlist_sessions = {}


def handle_playlist_url(message, url):
    playlist_sessions[message.chat.id] = {"url": url, "type": "playlist"}
    
    bot.send_message(
        message.chat.id,
        "Select format",
        reply_markup=keyboard_builder.playlist_options_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data in [Callbacks.PLAYLIST_ALL_VIDEO, Callbacks.PLAYLIST_ALL_AUDIO])
def handle_playlist_download_all(call):
    chat_id = call.message.chat.id
    
    if chat_id not in playlist_sessions:
        bot.answer_callback_query(call.id, "Session expired")
        return
    
    is_audio = call.data == Callbacks.PLAYLIST_ALL_AUDIO
    quality = "audio" if is_audio else "360p"
    
    bot.edit_message_text(
        Messages.PROCESSING,
        chat_id,
        call.message.message_id
    )
    
    url = playlist_sessions[chat_id]["url"]
    
    try:
        result = asyncio.run(
            downloader.download(url, quality, is_audio)
        )
        
        files = result.get("files", [])
        
        if not files:
            bot.edit_message_text(Messages.ERROR, chat_id, call.message.message_id)
            return
        
        total = len(files)
        
        if total > config.MAX_PLAYLIST_SIZE:
            bot.edit_message_text(
                Messages.PLAYLIST_TOO_LARGE.format(max=config.MAX_PLAYLIST_SIZE),
                chat_id,
                call.message.message_id
            )
            return
        
        bot.edit_message_text(
            f"Downloading {total} videos",
            chat_id,
            call.message.message_id
        )
        
        success_count = 0
        
        for idx, file_info in enumerate(files, 1):
            try:
                file_path = Path(file_info.get("path", ""))
                
                if not file_path.exists():
                    continue
                
                file_size_mb = downloader.get_file_size_mb(file_path)
                
                if file_size_mb > config.MAX_FILE_SIZE_MB:
                    downloader.cleanup_file(file_path)
                    continue
                
                bot.edit_message_text(
                    Messages.progress(idx, total),
                    chat_id,
                    call.message.message_id
                )
                
                with open(file_path, 'rb') as file:
                    if is_audio:
                        bot.send_audio(chat_id, file)
                    else:
                        bot.send_video(chat_id, file)
                
                success_count += 1
                downloader.cleanup_file(file_path)
                
            except Exception:
                continue
        
        bot.edit_message_text(
            f"Downloaded {success_count}/{total}",
            chat_id,
            call.message.message_id
        )
        
    except Exception:
        bot.edit_message_text(Messages.ERROR, chat_id, call.message.message_id)
    
    finally:
        if chat_id in playlist_sessions:
            del playlist_sessions[chat_id]
    
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == Callbacks.PLAYLIST_SELECT)
def handle_playlist_select(call):
    bot.answer_callback_query(call.id, "Coming soon")
    bot.edit_message_text(
        "Under development",
        call.message.chat.id,
        call.message.message_id
    )
