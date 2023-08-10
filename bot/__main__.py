from aiogram import Bot
from aiogram.enums import ParseMode

from utils import logger
from .factory import make_dispatcher
from .settings import Settings


def main() -> None:
    logger.setup()

    dp = make_dispatcher()
    dp["settings"] = settings = Settings()

    bot = Bot(token=settings.API_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    return dp.run_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    main()
