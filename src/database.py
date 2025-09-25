from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi.exceptions import HTTPException
from sqlalchemy import URL
from sqlalchemy.exc import IntegrityError
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
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail="Integrity database error")
    finally:
        await session.close()
        await engine.dispose()
