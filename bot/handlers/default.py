import openai
from aiogram.types import Message

from dependencies import assistance as asis
from dependency import assistant
from dependencies import cache as cD
from dependencies import event as eD


async def default_handler(message: Message):
    text = message.text
    user_id = message.from_user.id

    eD.event_handler("Text Message", user_id)

    thread_id = await asis.get_thread_id(user_id)

    response = await asis.get_assistant_response(text, thread_id, assistant)

    await message.answer(response)
