import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode

import handlers
import middlewares
from settings import Settings
from utils import logger


async def main() -> None:
    logger.setup()
    settings = Settings()
    bot = Bot(settings.API_TOKEN, parse_mode=ParseMode.HTML)

    router = Router(name=__name__)
    middlewares.setup(router)
    handlers.setup(router)

    dp = Dispatcher(name=__name__)
    dp.include_router(router)

    await dp.start_polling(
        bot, allowed_updates=dp.resolve_used_update_types(),
        settings=settings
    )


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
