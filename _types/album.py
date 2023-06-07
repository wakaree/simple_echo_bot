
from typing import List, Optional, Dict, Type, Union, cast

from aiogram.types import (
    PhotoSize, Video, Audio,
    Document, Animation,
    InputMediaPhoto, InputMediaVideo,
    InputMediaAudio, InputMediaDocument
)
from pydantic import BaseModel

Media = Union[PhotoSize, Video, Audio, Document]
InputMedia = Union[
    InputMediaPhoto, InputMediaVideo,
    InputMediaAudio, InputMediaDocument
]


class Album(BaseModel):
    input_media: Dict[str, Type[InputMedia]] = {
        "photo": InputMediaPhoto,
        "video": InputMediaVideo,
        "audio": InputMediaAudio,
        "document": InputMediaDocument
    }

    photo: Optional[List[PhotoSize]] = None
    video: Optional[List[Video]] = None
    audio: Optional[List[Audio]] = None
    document: Optional[List[Document]] = None
    animation: Optional[List[Animation]] = None
    caption: Optional[str] = None

    @property
    def media_type(self) -> str:
        if self.photo:
            return "photo"
        if self.video:
            return "video"
        if self.audio:
            return "audio"
        if self.document:
            return "document"
        return "unknown"

    @property
    def media(self) -> Optional[List[Media]]:
        return getattr(self, self.media_type, None)

    @property
    def as_media_group(self) -> Optional[List[InputMedia]]:
        typ = self.media_type
        input_type = self.input_media.get(typ, None)

        if input_type is not None:
            media = cast(List[Media], self.media)
            group = [
                input_type(
                    type=typ, media=media[0].file_id,
                    caption=self.caption
                )
            ]

            for file in media[1:]:
                group.append(input_type(type=typ, media=file.file_id))

            return group
        return None
