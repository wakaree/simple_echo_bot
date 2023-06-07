from asyncio import sleep
from typing import (
    Any, Callable, Awaitable, MutableMapping,
    Tuple, Dict, Optional, cast
)

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from cachetools import TTLCache

from _types import Album, Media


class AlbumMiddleware(BaseMiddleware):
    DEFAULT_LATENCY = 0.1
    DEFAULT_TTL = 0.2

    def __init__(
        self,
        latency: float = DEFAULT_LATENCY,
        ttl: float = DEFAULT_TTL
    ) -> None:
        self.latency = latency
        self.cache: MutableMapping[
            str, Dict[str, Any]
        ] = TTLCache(maxsize=10_000, ttl=ttl)

    @staticmethod
    def get_content(message: Message) -> Optional[Tuple[Media, str]]:
        if message.photo:
            return message.photo[-1], "photo"
        if message.video:
            return message.video, "video"
        if message.audio:
            return message.audio, "audio"
        if message.document:
            return message.document, "document"
        return None

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        event = cast(Message, event)
        if event.media_group_id is not None:
            key = event.media_group_id
            media, content_type = cast(Tuple[Media, str], self.get_content(event))

            if key in self.cache:
                return self.cache[key][content_type].append(media)

            self.cache[key] = {content_type: [media], "caption": event.html_text}
            await sleep(self.latency)
            data["album"] = Album(**self.cache[key])

        return await handler(event, data)
