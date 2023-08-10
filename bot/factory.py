from aiogram import Dispatcher

from .handlers import main
from .middlewares import AlbumMiddleware, ThrottlingMiddleware


def make_dispatcher() -> Dispatcher:
    dp = Dispatcher(name="__main__")

    dp.message.middleware(AlbumMiddleware())
    dp.message.middleware(ThrottlingMiddleware())

    dp.include_routers(main.router)

    return dp
