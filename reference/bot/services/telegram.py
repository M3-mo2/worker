# bot_v2/bot/services/telegram.py
# Encapsulates direct interactions with the Telegram Bot API.

import httpx
from typing import Optional, Dict, Any

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError, PeerIdInvalidError

# Local Imports from bot_v2 core
from bot.core.client import client
from bot.core.config import settings


async def set_webhook_for_token(token: str, secret_token: Optional[str] = None) -> Optional[str]:
    """
    Sets a Telegram webhook for a given bot token using httpx.
    Returns the response text from Telegram or None on failure.
    """
    # Use the dedicated WEBHOOK_BASE_URL to avoid unintended path prefixes
    webhook_url = f"{settings.web.WEBHOOK_BASE_URL.rstrip('/')}/webhook?tk={token}"
    api_url = f"https://api.telegram.org/bot{token}/setWebhook"
    params = {'url': webhook_url}
    if secret_token:
        params['secret_token'] = secret_token

    print(f"[TelegramService] Setting webhook via httpx:\n{api_url}\n")
    try:
        async with httpx.AsyncClient() as http_client:
            resp = await http_client.get(api_url, params=params, timeout=10)
        print("[TelegramService] RESULT:", resp.text)
        resp.raise_for_status()
        return resp.text
    except httpx.HTTPStatusError as e:
        print(f"[TelegramService] ERROR setting webhook for {token[:8]}: HTTP {e.response.status_code} - {e.response.text}")
        return e.response.text
    except Exception as e:
        print(f"[TelegramService] ERROR setting webhook for {token[:8]}: {e}")
        return None

async def delete_webhook_for_token(token: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
    """
    Deletes a Telegram webhook for a given bot token using httpx.
    Returns the JSON response from Telegram or None on failure.
    """
    api_url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    try:
        async with httpx.AsyncClient() as http_client:
            resp = await http_client.post(api_url, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        print(f"[TelegramService] ERROR deleting webhook for {token[:8]}: HTTP {e.response.status_code} - {e.response.text}")
        try:
            return e.response.json()
        except Exception:
            return {"error": e.response.text}
    except Exception as e:
        print(f"[TelegramService] ERROR deleting webhook for {token[:8]}: {e}")
        return None

async def get_user_info(user_identifier: Any) -> Optional[Dict[str, Any]]:
    """
    Retrieves user information from Telegram using client.get_entity and GetFullUserRequest.
    Can accept user ID (int), username (str), or forwarded message (event object).
    Returns a dictionary with user data (id, first_name, username) or None if not found.
    """
    if isinstance(user_identifier, str) and user_identifier.isdigit():
        user_identifier = int(user_identifier)
    elif isinstance(user_identifier, str) and user_identifier.startswith('@'):
        user_identifier = user_identifier[1:] # Remove '@' for get_entity

    try:
        # Use GetFullUserRequest for more reliable user fetching
        user = await client(GetFullUserRequest(user_identifier))
        user_entity = user.users[0] # The actual User object is within the users list
        
        return {
            "id": user_entity.id,
            "first_name": user_entity.first_name,
            "username": user_entity.username or "N/A" # Default to "N/A" if username is None
        }
    except (UserNotParticipantError, PeerIdInvalidError, ValueError, IndexError) as e:
        print(f"[TelegramService] Could not find user '{user_identifier}': {e}")
        return None
    except Exception as e:
        print(f"[TelegramService] Unexpected error getting user info for '{user_identifier}': {e}")
        return None

async def get_chat_entity(chat_identifier: Any) -> Optional[Any]:
    """
    Retrieves chat entity (channel or group) information from Telegram.
    Can accept chat ID (int), username (str), or event object.
    Returns the Telethon entity object or None if not found.
    """
    try:
        if isinstance(chat_identifier, str) and chat_identifier.startswith('@'):
            chat_identifier = chat_identifier[1:] # Remove '@' for get_entity
        entity = await client.get_entity(chat_identifier)
        return entity
    except Exception as e:
        print(f"[TelegramService] Could not find chat entity '{chat_identifier}': {e}")
        return None

async def export_chat_invite_link(chat_id: int) -> Optional[str]:
    """
    Exports an invite link for a given chat ID.
    Returns the invite link (str) or None on failure.
    """
    try:
        invite_link_result = await client(ExportChatInviteRequest(chat_id))
        return invite_link_result.link
    except Exception as e:
        print(f"[TelegramService] Could not export invite link for chat {chat_id}: {e}")
        return None

async def send_message_to_admin(admin_id: int, text: str, parse_mode: str = 'md') -> bool:
    """Send message to admin using Bot API directly, avoiding Telethon entity issues.
    
    Falls back to HTTP Bot API if Telethon fails with entity resolution error.
    Returns True if sent successfully, False otherwise.
    """
    # Try Telethon first
    try:
        await client.send_message(admin_id, text, parse_mode=parse_mode)
        return True
    except ValueError:
        pass
    except Exception:
        return False

    # Fallback: Bot API (doesn't need access_hash)
    # Convert Telethon parse_mode to Bot API format
    bot_parse_mode = parse_mode
    if parse_mode == 'md':
        bot_parse_mode = 'Markdown'

    url = f"https://api.telegram.org/bot{settings.telegram.BOT_TOKEN}/sendMessage"
    payload = {"chat_id": admin_id, "text": text, "parse_mode": bot_parse_mode}
    try:
        async with httpx.AsyncClient() as http_client:
            resp = await http_client.post(url, json=payload, timeout=10)
            return resp.json().get("ok", False)
    except Exception:
        return False

print("✅ Telegram Service module initialized.")