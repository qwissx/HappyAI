import json

from cache.connection import redis


async def add_cache_message(user_id, message: str, exp=3600):
    val_key = f"messages:{user_id}"

    message = {"role": "user", "content": message}
    serialized_message = json.dumps(message)
    await redis.rpush(val_key, serialized_message)

    await redis.expire(val_key, exp)


async def get_cache_messages(user_id, offset=0, limit=5):
    val_key = f"messages:{user_id}"

    messages = await redis.lrange(val_key, offset, offset+limit)
    if not messages:
        return None

    serialized_messages = []
    for message in messages:
        serialized_messages.append(json.loads(message.decode()))

    return serialized_messages
