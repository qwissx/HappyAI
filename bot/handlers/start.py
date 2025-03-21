from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from dependencies import event as eD
from dependencies import assistance as asis


async def start_handler(message: Message, state: FSMContext) -> None:
    eD.event_handler("Start Message", message.from_user.id)

    await asis.get_user_thread_id(state)

    text = f"Hello, {message.from_user.full_name}! Send me the voice message and I will answer the question."
    await message.answer(text=text)
