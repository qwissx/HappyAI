import asyncio
import logging
import sys

from aiogram import F
from aiogram.filters import CommandStart

from handlers.start import start_handler
from handlers.voice import voice_handler
from handlers.default import default_handler
from handlers.images import analyze_image_handler

from dependency import dp, bot


dp.message(F.voice)(voice_handler)
dp.message(lambda message: message.photo is not None)(analyze_image_handler)
dp.message(CommandStart)(start_handler)
dp.message(lambda message: message is not None)(default_handler)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())