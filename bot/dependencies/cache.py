import json

from cache.connection import redis


async def add_user_thread(user_id, thread_id, exp=3600):
    val_key = f"thread:{user_id}"

    await redis.set(val_key, thread_id)

    await redis.expire(val_key, exp)


async def get_user_thread(user_id):
    val_key = f"thread:{user_id}"

    thread_id = await redis.get(val_key)

    if not thread_id:
        return None

    return thread_id.decode() 
