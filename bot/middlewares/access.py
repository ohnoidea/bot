from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Any, Dict, Callable, Awaitable

from config import admin_ids


class AdminMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user_id = data['event_from_user'].id
        if user_id not in admin_ids:
            return await data['bot'].send_message(user_id, 'The Force is weak with you')
        return await handler(event, data)


class AuthMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user_id = data['event_from_user'].id
        
        if not (await data['db_request'].known_user(user_id)):
            return await data['bot'].send_message(user_id, 'You are not one with the Force')
        return await handler(event, data)
