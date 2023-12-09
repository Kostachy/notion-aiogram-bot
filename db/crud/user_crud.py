from pyexpat import model

from sqlalchemy import select, insert

from db.models.user import User
from db.database import async_session


class UserCrud:
    model = User

    @classmethod
    async def get_user(cls, user_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(user_id=user_id)
            result = session.execute(query)
            return result.scalars().first()

    @classmethod
    async def create_user(cls, *data):
        async with async_session() as session:
            query = insert(cls.model).values(*data)
            session.execute(query)
            session.commit()
