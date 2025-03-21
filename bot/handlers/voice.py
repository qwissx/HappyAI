import subprocess
import os

from aiogram.types import Message

from dependency import bot, assistant
from dependencies import assistance as asis
from dependencies import event as eD


async def voice_handler(message: Message):
    voice = message.voice
    user_id = message.from_user.id

    eD.event_handler("Voice Message", user_id)
    
    file_id = voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await bot.download_file(file_path, f"bot/static/voice_{file_id}.ogg")

    input_file = f"bot/static/voice_{file_id}.ogg"
    output_file = f"bot/static/voice_{file_id}.mp3"
    command = ["ffmpeg", "-i", input_file, output_file]

    subprocess.run(command, check=True)

    text = await asis.transcribe_audio(output_file)

    thread_id = await asis.get_user_thread_id(state)

    response = await asis.get_assistant_response(text, thread_id, assistant)

    save_as = f"bot/static/answer_{file_id}.mp3"
    voice_response = await asis.text_to_speech(response, save_as)

    await message.answer_audio(save_as)

    os.remove(input_file)
    os.remove(output_file)
    os.remove(save_as)
