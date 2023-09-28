from aiogram import Dispatcher

from .handlers import main
from .middlewares import AlbumMiddleware, ThrottlingMiddleware


def make_dispatcher() -> Dispatcher:
    dp = Dispatcher(name="__main__")

    dp.message.middleware(AlbumMiddleware())

    # This is just throttling usage example and does not need to be combined with AlbumMiddleware
    dp.message.middleware(ThrottlingMiddleware(foo=0.2, bar=0.5))

    dp.include_routers(main.router)

    return dp
