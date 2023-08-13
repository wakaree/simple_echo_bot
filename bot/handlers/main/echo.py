from typing import Any

from aiogram import F, Router
from aiogram.methods import TelegramMethod
from aiogram.types import Message

from bot.types import Album

router = Router(name=__name__)


@router.message(F.media_group_id)
async def echo_album(message: Message, album: Album) -> TelegramMethod[Any]:
    return album.copy_to(chat_id=message.chat.id)


@router.message()
async def echo_message(message: Message) -> TelegramMethod[Any]:
    try:
        return message.send_copy(message.chat.id)
    except TypeError:
        return message.answer("Bro, I can't copy it.")
