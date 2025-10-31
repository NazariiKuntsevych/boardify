from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import settings

url = URL.create(
    drivername=settings.DB_DRIVER,
    database=settings.DB_NAME,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    username=settings.DB_USER,
    password=settings.DB_PASSWORD.get_secret_value(),
)
engine = create_async_engine(url)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = session_maker()
    try:
        yield session
    except DatabaseError:
        await session.rollback()
        raise
    finally:
        await session.close()
