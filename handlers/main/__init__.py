
from aiogram import Router

from . import echo

__all__ = [
    "echo", "router"
]


router = Router(name=__name__)
router.include_router(
    echo.router
)
