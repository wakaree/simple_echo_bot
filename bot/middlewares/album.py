from __future__ import annotations

from asyncio import sleep
from typing import Any, Awaitable, Callable, Dict, MutableMapping, Optional, Tuple, cast

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from cachetools import TTLCache

from ..types import Album, Media

DEFAULT_LATENCY = 0.2
DEFAULT_TTL = 0.3


class AlbumMiddleware(BaseMiddleware):
    def __init__(
        self,
        album_key: str = "album",
        latency: float = DEFAULT_LATENCY,
        ttl: float = DEFAULT_TTL,
    ) -> None:
        self.album_key = album_key
        self.latency = latency
        self.cache: MutableMapping[str, Dict[str, Any]] = TTLCache(maxsize=10_000, ttl=ttl)

    @classmethod
    def webhook_mode(cls, album_key: str = "album") -> AlbumMiddleware:
        """
        Set up the middleware to be used with webhooks.
        In fact, in most cases, simply increasing the delay is sufficient.

        If during testing some elements of the media group are lost, just increase delay even more.
        """
        return cls(album_key=album_key, latency=1, ttl=2)

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
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.media_group_id is not None:
            key = event.media_group_id
            media, content_type = cast(Tuple[Media, str], self.get_content(event))

            if key in self.cache:
                if content_type not in self.cache[key]:
                    self.cache[key][content_type] = [media]
                    return None

                self.cache[key]["messages"].append(event)
                self.cache[key][content_type].append(media)
                return None

            self.cache[key] = {
                content_type: [media],
                "messages": [event],
                "caption": event.html_text,
            }

            await sleep(self.latency)
            data[self.album_key] = Album.model_validate(
                self.cache[key], context={"bot": data["bot"]}
            )

        return await handler(event, data)
