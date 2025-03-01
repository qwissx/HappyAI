from dependency import openai_cli

async def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = await openai_cli.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    return transcript.text

async def get_assistant_response(user_input):
    assistant = await openai_cli.beta.assistants.create(
        name="Assistant",
        instructions="You are helpful assistant who answers questions.",
        model="gpt-4",
    )

    thread = await openai_cli.beta.threads.create()

    await openai_cli.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )

    run = await openai_cli.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while run.status != "completed":
        await asyncio.sleep(1)
        run = await openai_cli.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )

    messages = await openai_cli.beta.threads.messages.list(
        thread_id=thread.id,
    )

    for message in messages.data:
        if message.role == "assistant":
            return message.content[0].text.value


async def text_to_speech(text, output_file):
    response = await openai_cli.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    response.stream_to_file(output_file)
