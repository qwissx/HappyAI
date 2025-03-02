import asyncio

from aiogram import Bot, Dispatcher
from openai import AsyncOpenAI
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from settings import settings as st


bot = Bot(token=st.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

openai_cli = AsyncOpenAI(api_key=st.openai_api_key)

assistant = asyncio.run(openai_cli.beta.assistants.create(
    name="assistant",
    instructions="You must give answers and analyze the text for values. Return information in json format {'response':response, 'value':value}",
    model="gpt-4",
))
