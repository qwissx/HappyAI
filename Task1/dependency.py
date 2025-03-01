from aiogram import Bot, Dispatcher
from openai import AsyncOpenAI
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from settings import settings as st


bot = Bot(token=st.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

openai_cli = AsyncOpenAI(api_key=st.openai_api_key)
