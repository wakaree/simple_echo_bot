import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import handlers
import middlewares
from settings import Settings
from utils import logger


async def main() -> None:
    logger.setup()
    settings = Settings()  # type: ignore[call-arg]
    bot = Bot(settings.API_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)

    dp = Dispatcher(name=__name__)
    middlewares.setup(dp)
    handlers.setup(dp)

    await dp.start_polling(
        bot, allowed_updates=dp.resolve_used_update_types(),
        settings=settings
    )


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
