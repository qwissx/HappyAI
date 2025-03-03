import json

from dependency import openai_cli
from database.userRepository import UsersRepository
from database.connection import async_session_maker


async def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = await openai_cli.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    return transcript.text


async def get_assistant_response(user_input, assistant):
    thread = await openai_cli.beta.threads.create()

    await openai_cli.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )

    run = await openai_cli.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    try:
        while True:
            status = run.status

            if status == "completed":
                return response
            elif status == "failed":
                return None
            elif status == "pending":
                await asyncio.sleep(2) 
            else:
                return None

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

    messages = await openai_cli.beta.threads.messages.list(
        thread_id=thread.id,
    )

    for message in messages.data:
        if message.role == "user":
            response = json.dumps(message.content[0].text.value)

            return {
                'response': response.get('response'), 
                'value': response.get('value'),
            }


async def text_to_speech(text, output_file):
    response = await openai_cli.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    response.stream_to_file(output_file)


async def value_completions(value, user_id):
    response = await openai_cli.chat.completions.create(
        model="gpt-4o",
        messages=[{'role':'user', 'content': f"Check, if {value} is value or purpose of man. The answer only can be 'true' or 'false'"}]
    )

    result_bool = bool(response.choices[0].message.content)

    if result_bool:
        async with async_session_maker() as session:
            user = await UsersRepository.get(session, id=user_id)

            if user:
                return 
            
            await UsersRepository.add(
                session, 
                id=user_id, 
                value=value,
            )
            await session.commit()
