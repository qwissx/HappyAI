from openai import AsyncOpenAI

from dependencies import assistance as asis


async def create_file_store(client: AsyncOpenAI):
    file = await client.files.create(
        file=open("bot.static.stress.docx", "rb"),
        purpose="assistans"
        )

    file_id = file.get("id")

    store_id = await asis.get_vectore_store_id(client)

    store_file = vector_store_file = await client.vector_stores.files.create(
        vector_store_id=store_id,
        file_id=file_id
        )

    return store_file
