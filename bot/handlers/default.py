import openai
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from dependencies import assistance as asis
from dependency import assistant
from dependencies import event as eD


async def default_handler(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id

    eD.event_handler("Text Message", user_id)

    thread_id = await asis.get_user_thread_id(user_id)

    response = await asis.get_assistant_response(text, thread_id, assistant)

    await message.answer(response)
