# bot_v2/bot/core/client.py
# Initializes and exports a single instance of TelegramClient.

from telethon import TelegramClient
from bot.core.config import settings

import secrets

# A unique session name for the new bot_v2 project
# Default base session name — can be rotated if conflict detected.
SESSION_NAME = 'bot'


def _create_client(session_name: str):
    """Create a TelegramClient instance for the given session name."""
    return TelegramClient(
        session_name,
        settings.telegram.API_ID,
        settings.telegram.API_HASH
    )

# Global client instance (created lazily at import time)
client = _create_client(SESSION_NAME)
print(f"✅ TelegramClient initialized with API_ID: {settings.telegram.API_ID} (Session: {SESSION_NAME})")


def reset_client(new_suffix: str = None):
    """Rotate the global client to a new session name to avoid conflicts.

    If new_suffix is provided it will be appended to the base session name,
    otherwise a short random hex is used. This function reassigns the module-level
    `client` variable so other modules importing `bot.core.client` can access
    the new instance as `bot.core.client.client`.
    """
    global client
    suffix = new_suffix or secrets.token_hex(6)
    new_name = f"{SESSION_NAME}_{suffix}"
    client = _create_client(new_name)
    print(f"🔁 TelegramClient session rotated -> {new_name}")
    return new_name
