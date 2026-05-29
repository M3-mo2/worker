from core.bot import bot
from core.constants import Messages
from services.validator import validator
from handlers.video import handle_video_url
from handlers.playlist import handle_playlist_url


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_message(message):
    url = message.text.strip()
    is_valid, url_type = validator.validate(url)
    
    if not is_valid:
        bot.send_message(message.chat.id, Messages.INVALID_URL)
        return
    
    if url_type == "video":
        handle_video_url(message, url)
    elif url_type == "playlist":
        handle_playlist_url(message, url)
