from aiogram import Router

from . import echo

router = Router(name=__name__)
router.include_routers(echo.router)
