from aiogram.types import Message

from dependency import bot
from dependencies import assistance as asis


async def analyze_image_handler(message: Message):
    image = message.photo
    user_id = message.from_user.id

    file_id = image.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    image_path = f"bot/static/image_{file_id}.jpg"
    await bot.download_file(file_path, image_path)

    thread_id = await asis.get_thread_id(user_id)
    response = await asis.analyze_image(image_path)

    await message.answer(response)
