from aiogram.types import Message

from dependencies import assistance as asis
from dependency import assistant


async def default_handler(message: Message):
    text = message.text

    response = await asis.get_assistant_response(text, assistant)

    await message.answer(response)
