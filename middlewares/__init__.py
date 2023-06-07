
from aiogram import Router

from .album import AlbumMiddleware
from .throttling import ThrottlingMiddleware

__all__ = [
    "AlbumMiddleware",
    "ThrottlingMiddleware",
    "setup"
]


def setup(router: Router) -> None:
    for m in [
        ThrottlingMiddleware(),
        AlbumMiddleware()
    ]:
        router.message.middleware(m)
