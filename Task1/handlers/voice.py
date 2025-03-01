import subprocess
import os

from aiogram.types import Message

from dependency import bot
from dependencies import assistance as asis


async def voice_handler(message: Message):
    voice = message.voice
    
    file_id = voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await bot.download_file(file_path, f"Task1/static/voice_{file_id}.ogg")

    input_file = f"Task1/static/voice_{file_id}.ogg"
    output_file = f"Task1/static/voice_{file_id}.mp3"
    command = ["ffmpeg", "-i", input_file, output_file]

    subprocess.run(command, check=True)

    text = await asis.transcribe_audio(output_file)
    response = await asis.get_assistant_response(text)

    save_as = f"Task1/static/answer_{file_id}.mp3"
    voice_response = await asis.text_to_speech(response, save_as)

    await message.answer_audio(save_as)

    os.remove(input_file)
    os.remove(output_file)
    os.remove(save_as)
