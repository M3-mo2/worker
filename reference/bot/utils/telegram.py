# bot_v2/bot/utils/telegram.py
# Contains Telegram-specific utility functions.

from telethon import events
from telethon.errors.rpcerrorlist import MessageNotModifiedError
from typing import Any, List, Optional

async def safe_edit_message(event: Any, text: str, buttons: Optional[List[List[Any]]] = None, parse_mode: str = 'md', link_preview: bool = None, entities: list = None):
    """
    Safely edits an existing message or sends a new one if editing fails.
    Handles MessageNotModifiedError gracefully.
    """
    try:
        # Check if the event is a CallbackQueryEvent or a NewMessageEvent
        if isinstance(event, events.CallbackQuery.Event):
            await event.edit(text, buttons=buttons, parse_mode=parse_mode, link_preview=link_preview, formatting_entities=entities)
        else: # Assuming it's a NewMessageEvent or similar with chat_id and id
            await event.client.edit_message(event.chat_id, event.id, text, buttons=buttons, parse_mode=parse_mode, link_preview=link_preview, formatting_entities=entities)
    except MessageNotModifiedError:
        pass # Ignore if the message is the same
    except Exception as e:
        print(f"Error in safe_edit_message: {e}. Falling back to sending new message.")
        # Fallback to sending new message if edit fails
        try:
            if isinstance(event, events.CallbackQuery.Event):
                await event.client.send_message(event.chat_id, text, buttons=buttons, parse_mode=parse_mode, link_preview=link_preview, formatting_entities=entities)
            else:
                await event.reply(text, buttons=buttons, parse_mode=parse_mode, link_preview=link_preview, formatting_entities=entities)
        except Exception as e2:
            print(f"Fallback send_message also failed: {e2}")

print("✅ Telegram utilities module initialized.")
