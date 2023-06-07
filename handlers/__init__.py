
from aiogram import Dispatcher


def setup(dp: Dispatcher) -> None:
    from handlers import main

    dp.include_routers(
        main.router
    )
