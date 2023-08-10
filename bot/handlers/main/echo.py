from typing import Any

from aiogram import Router, F
from aiogram.methods import TelegramMethod
from aiogram.types import Message

from bot.types import Album


router = Router(name=__name__)


@router.message(F.media_group_id)
async def echoAlbum(message: Message, album: Album) -> TelegramMethod[Any]:
    return message.answer_media_group(album.as_media_group)


@router.message()
async def echoMessage(message: Message) -> TelegramMethod[Any]:
    try:
        return message.send_copy(message.chat.id)
    except TypeError:
        return message.answer("Bro, I can't copy it.")
