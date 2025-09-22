from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import DB_DRIVER, DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD

url = URL.create(
    drivername=DB_DRIVER,
    database=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
    username=DB_USER,
    password=DB_PASSWORD,
)
engine = create_async_engine(url)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = session_maker()
    try:
        yield session
        await session.commit()
    except IntegrityError:
        await session.rollback()
    finally:
        await session.close()
