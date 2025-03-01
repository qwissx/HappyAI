import asyncio
import logging
import sys

from aiogram.filters import CommandStart

from handlers.start import start_handler
from handlers.voice import voice_handler

from dependency import dp, bot


dp.message(lambda message: message.voice is not None)(voice_handler)
dp.message(CommandStart)(start_handler)

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())