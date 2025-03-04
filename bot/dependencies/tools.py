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


tools = [{
    "type": "function",
    "function": {

        "name": "save_value",
        "description": "If in text founds value then this function will call.",
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