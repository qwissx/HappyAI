import json

from database.connection import async_session_maker
from database.userRepository import UsersRepository


async def save_value(value):
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


async def choose_call_func(response: dict):
    if "tool_calls" in response["choices"][0]["message"]:
        tool_calls = response["choices"][0]["message"]["tool_calls"]

        for tool_call in tool_calls:
            args = json.loads(tool_call["function"]["arguments"])

            if tool_call["function"]["name"] == "save_value":
                await save_value(**args)


tools = [{
    "type": "function",
    "function": {

        "name": "save_value",
        "description": "If in text founds value then this function will call. Function must return True.",
        "parameters": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "description": "key value of user"
                }
            },
            "required": ["value"]
        }
    }
}]