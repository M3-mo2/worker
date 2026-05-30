import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return await handler(event, data)

        data["user_id"] = user_id
        return await handler(event, data)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user = event.from_user
            text = event.text or "[non-text]"
            logging.info(f"[MSG] {user.id} (@{user.username}): {text}")
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            logging.info(f"[CB] {user.id} (@{user.username}): {event.data}")

        return await handler(event, data)
