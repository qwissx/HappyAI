from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Users


class UsersRepository:
    @classmethod
    async def add(cls, connection: AsyncSession, **data):
        query = insert(Users).values(**data)
        await connection.execute(query)

    @classmethod
    async def get(cls, connection: AsyncSession, **filter_by):
        query = select(Users).filter_by(**filter_by)
        user = await connection.execute(query)
        return user.scalar_one_or_none()
