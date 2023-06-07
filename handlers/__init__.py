
from aiogram import Router


def setup(router: Router) -> None:
    from . import main

    router.include_routers(
        main.router
    )
