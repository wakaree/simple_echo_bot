from aiogram import Router, F
from aiogram.methods import CopyMessage, SendMediaGroup
from aiogram.types import Message, ContentType

from _types import Album

router = Router(name=__name__)


@router.message(F.media_group_id)
async def echoAlbum(message: Message, album: Album) -> SendMediaGroup:
    return message.answer_media_group(album.as_media_group)


@router.message(
    F.content_type.in_([
        ContentType.TEXT,
        ContentType.VIDEO,
        ContentType.ANIMATION,
        ContentType.STICKER,
        ContentType.POLL,
        ContentType.PHOTO,
        ContentType.AUDIO,
        ContentType.VOICE,
        ContentType.LOCATION,
        ContentType.CONTACT,
        ContentType.VIDEO_NOTE,
        ContentType.HAS_MEDIA_SPOILER,
    ])
)
async def echoMessage(message: Message) -> CopyMessage:
    return message.copy_to(message.chat.id)
