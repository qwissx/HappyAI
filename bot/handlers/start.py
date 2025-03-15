from aiogram.types import Message

from dependencies import event as eD


async def start_handler(message: Message) -> None:
    eD.event_handler("Start Message", message.from_user.id)
    text = f"Hello, {message.from_user.full_name}! Send me the voice message and I will answer the question."
    await message.answer(text=text)
