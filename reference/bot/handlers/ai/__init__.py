# bot_v2/bot/handlers/ai/__init__.py
# This __init__.py file is responsible for aggregating and setting up
# all AI-related handlers within the 'ai' sub-package.

from . import handlers
from . import keys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telethon import TelegramClient

def setup(client: "TelegramClient"):
    """
    Sets up all AI-related handlers and sub-handlers by calling their
    respective setup functions.
    """
    handlers.setup(client)
    keys.setup(client)
    print("✅ AI handlers package setup complete.")
