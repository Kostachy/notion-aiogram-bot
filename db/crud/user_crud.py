from sqlalchemy import select, insert

from db.models.user import User
from db.database import async_session


class UserCrud:
    model = User

    @classmethod
    async def get_user_id(cls, user_id: int):
        async with async_session() as session:
            query = select(cls.model.user_id).filter_by(user_id=user_id)
            result = await session.execute(query)
            return result.one_or_none()

    @classmethod
    async def create_user(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_db_link(cls, db_link: str):
        async with async_session() as session:
            query = insert(cls.model).values(db_link=db_link)
            await session.execute(query)
            await session.commit()
