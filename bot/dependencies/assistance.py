import json

from openai import OpenAIError

from main import logging
from dependencies.tools import tools, choose_call_func
from dependency import openai_cli
from database.userRepository import UsersRepository
from database.connection import async_session_maker
from dependencies import cache as cD


async def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = await openai_cli.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    return transcript.text


async def get_assistant_response(user_input, user_id, assistant):
    thread = await openai_cli.beta.threads.create()

    await cD.add_cache_message(user_id, user_input)
    users_messages = await cD.get_cache_messages(user_id)

    try:
        response = await openai_cli.beta.threads.runs.create_and_poll(
            thread_id=thread.id, 
            assistant_id=assistant.id, 
            poll_interval_ms=2000,
            messages=[
                {"role": "system", "content": "\
                    Find in the dialogue the value of the user and validate this value.\
                    If value is value or purpose of a man then call function save_value"},
            ] + users_messages,
            tools=tools,
        )
        
        if response.status == "completed":
            await choose_call_func(response)

            return response["choices"][0]["message"]["content"]


        if response.status in ['expired','failed','cancelled','incomplete']:
            logging.exception("Failed get response from OpenAI.")

    except OpenAIError as e:
        logging.exception("Error exception:", e)


async def text_to_speech(text, output_file):
    response = await openai_cli.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    response.stream_to_file(output_file)
