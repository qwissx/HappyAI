import asyncio
from concurrent.futures import ThreadPoolExecutor

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from openai import AsyncOpenAI
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from amplitude import Amplitude

from settings import settings as st
from dependencies.files import create_file_store


""" Bot dependencies"""
storage = RedisStorage.from_url(st.redis_url)

bot = Bot(token=st.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)


"""OpenAI dependencies"""
vector_store_file = asyncio.run(create_file_store(openai_cli))

openai_cli = AsyncOpenAI(api_key=st.openai_api_key)

assistant = asyncio.run(openai_cli.beta.assistants.create(
    name="assistant",
    instructions=
        "You must give answers and analyze the text for values\
        Use your knowledge base to answer question about stress.\
        Isert the file name after the quoted phrase from this file.",
    model="gpt-4",
    tools=[{"type": "file_search"}],
))

asyncio.run(openai_cli.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store_file.id]}},
))


"""Amplitude dependencies"""
amp = Amplitude(st.amplitude_api_key)

executer = ThreadPoolExecutor()
