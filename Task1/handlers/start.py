from aiogram.types import Message

async def start_handler(message: Message) -> None:
    text = f"Hello, {message.from_user.full_name}! Send me the voice message and I will answer the question."
    await message.answer(text=text)
