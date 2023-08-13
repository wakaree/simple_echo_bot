from typing import Any, Awaitable, Callable, Dict, MutableMapping, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

DEFAULT_RATE_LIMIT = 0.7


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple throttling middleware using TTLCache
    This is just an example and does not need to be combined with AlbumMiddleware
    """

    def __init__(self, rate_limit: float = DEFAULT_RATE_LIMIT) -> None:
        self.cache: MutableMapping[int, None] = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user", None)

        if user is not None:
            if user.id in self.cache:
                return None
            self.cache[user.id] = None
        return await handler(event, data)
