from typing import Any, Awaitable, Callable, Dict, MutableMapping, Optional

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, User
from cachetools import TTLCache

DEFAULT_RATE_LIMIT = 0.7
DEFAULT_KEY = "default"


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple throttling middleware using TTLCache
    This is just an example and does not need to be combined with AlbumMiddleware

    Usage example:
    router.message.middleware(ThrottlingMiddleware(spin=2.0))

    And then:
        @router.message(Command("dice"))
        @flags.throttling_key("spin")
        async def dice(message: Message) -> Any:
            pass
    """

    def __init__(
        self,
        *,
        default_key: Optional[str] = DEFAULT_KEY,
        default_ttl: float = 0.7,
        **ttl_map: float,
    ) -> None:
        """
        :param default_key: The cache key to be used by default.
        Set to None to disable throttling by default.
        :param default_ttl: The TTL in default cache
        :param ttl_map: Creates additional cache instances with different TTL
        """
        if default_key:
            ttl_map[default_key] = default_ttl

        self.default_key = default_key
        self.caches: Dict[str, MutableMapping[int, None]] = {}

        for name, ttl in ttl_map.items():
            self.caches[name] = TTLCache(maxsize=10_000, ttl=ttl)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user", None)

        if user is not None:
            throttling_key = get_flag(data, "throttling_key", default=self.default_key)
            if throttling_key and user.id in self.caches[throttling_key]:
                return None
            self.caches[throttling_key][user.id] = None

        return await handler(event, data)
