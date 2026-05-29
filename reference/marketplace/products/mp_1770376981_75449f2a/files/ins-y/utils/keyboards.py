from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.constants import Callbacks

# ايش الملل ذا
class KeyboardBuilder:
    @staticmethod
    def video_quality_keyboard():
        markup = InlineKeyboardMarkup(row_width=3)
        
        buttons = [
            InlineKeyboardButton("360p", callback_data=Callbacks.video_quality("360p")),
            InlineKeyboardButton("720p", callback_data=Callbacks.video_quality("720p")),
            InlineKeyboardButton("1080p", callback_data=Callbacks.video_quality("1080p")),
            InlineKeyboardButton("Audio", callback_data=Callbacks.audio_quality()),
        ]
        
        markup.add(*buttons[:3])
        markup.add(buttons[3])
        
        return markup
    
    @staticmethod
    def playlist_options_keyboard():
        markup = InlineKeyboardMarkup(row_width=2)
        
        markup.add(
            InlineKeyboardButton("Video", callback_data=Callbacks.PLAYLIST_ALL_VIDEO),
            InlineKeyboardButton("Audio", callback_data=Callbacks.PLAYLIST_ALL_AUDIO),
        )
        
        return markup
    
    @staticmethod
    def cancel_keyboard():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Cancel", callback_data=Callbacks.CANCEL))
        return markup


keyboard_builder = KeyboardBuilder()
