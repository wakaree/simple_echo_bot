
from aiogram import Dispatcher

from .album import AlbumMiddleware
from .throttling import ThrottlingMiddleware


__all__ = [
    "AlbumMiddleware",
    "ThrottlingMiddleware",
    "setup"
]


def setup(dp: Dispatcher) -> None:
    for m in [
        AlbumMiddleware(),
        ThrottlingMiddleware()
    ]:
        dp.message.middleware(m)
