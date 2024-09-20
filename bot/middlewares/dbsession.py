from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from psycopg_pool import AsyncConnectionPool
from typing import Any, Dict, Callable, Awaitable

from utils.dbconnect import Request


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, connection_pool: AsyncConnectionPool):
        super().__init__()
        self.connection_pool = connection_pool
    
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with self.connection_pool.connection() as conn:
            data['db_request'] = Request(conn)
            return await handler(event, data)
