from dependecies import openai_cli, bot

from aiogram.types import Message
import subprocess


async def voice_handler(message: Message):
    voice = message.voice
    
    file_id = voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    await bot.download_file(file_path, f"static/voice_{file_id}.ogg")

    input_file = f"static/voice_{file_id}.ogg"
    output_file = f"static/voice_{file_id}.mp3"
    command = ["ffmpeg", "-i", input_file, output_file]

    subprocess.run(command, check=True)

    audio_file = open(output_file, "rb")
    transcription = openai_cli.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

    print(transcription.text)
