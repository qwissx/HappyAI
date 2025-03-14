import json

import openai

from main import logging
from dependencies.tools import tools, choose_call_func
from dependency import openai_cli
from database.userRepository import UsersRepository
from database.connection import async_session_maker
from dependencies import cache as cD
from dependencies import funcs as fD
from dependencies import image as iD


async def make_action(run):
    tool_call, args = fD.get_tool_calls_and_args(run)

    if await validate_value(thread_id, **args) == "True":
        await choose_call_func(tool_call, **args)

    run = await client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run.id,
        tool_outputs=[
            {
            "output": "True",
            }
        ]
    )

    return run


async def validate_value(thread_id, **args):
    response = await openai.beta.threads.messages.list(thread_id)
    messages = fD.structured_messages(response)

    response = await openai_cli.chat.completions.create(
        messages=[
            {"role": "system", "content": f"check if {args} is the value or purpose of man. If it is return True, else False"}
        ] + messages,
    )

    return response["choices"][0]["message"]["content"]


async def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = await openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    return transcript.text


async def get_assistant_response(user_input, thread_id, assistant):
    message = await openai.beta.thread.message.create(
        thread_id=thread_id,
        role="user",
        content=user_input,
    )

    try:
        run = await openai.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant.id, 
            poll_interval_ms=2000,
            message={"role": "system", "content": "Find value user in this chat.\
                Check value is value or purpose of man, if true than call function save_value with this value."
            },
            tools=tools,
        )
        
        if run.status == "required_action":
            
            run = await make_action(run)

        if run.status == "completed":

            return run["choices"][0]["message"]["content"]


        if run.status in ['expired','failed','cancelled','incomplete']:
            logging.exception("Failed get response from OpenAI.")

    except openai.OpenAIError as e:
        logging.exception("Error exception:", e)


async def text_to_speech(text, output_file):
    response = await openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    response.stream_to_file(output_file)


async def get_thread_id(user_id):
    thread_id = await cD.get_user_thread(user_id)

    if not thread_id:
        thread = await openai.beta.thread.create()
        thread_id = thread.id

        await cD.add_user_thread(user_id, thread_id)

    return thread_id


async def analyze_image(image, thread_id):
    base64_image = iD.encode_image(image)
    while len(base64_image) > 86_000:
            iD.reduce_image_quality(image)
            base64_image = iD.encode_image(image)

    try:
        run = await openai.chat.completions.create(
                    model = "gpt-4-vision-preview",
                    thread_id=thread_id,
                    messages = [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": "What mood this man is?"},
                                {
                                    "type": "image_url",
                                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            ],
                        }
                    ]
                )

        if run.status == "completed":

            return run["choices"][0]["message"]["content"]


        if run.status in ['expired','failed','cancelled','incomplete']:
            logging.exception("Failed get response from OpenAI.")

    except openai.OpenAIError as e:
        logging.exception("Error exception:", e)
        