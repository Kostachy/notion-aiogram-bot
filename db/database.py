from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(settings.db_url,
                             echo=True,
                             poolclass=AsyncAdaptedQueuePool,
                             pool_size=12,
                             max_overflow=4,
                             pool_pre_ping=True
                             )
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
