from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pytest import Session

from src.config import settings
from src.main import app
from tests.utils import truncate_tables


@pytest_asyncio.fixture(autouse=True)
async def clear_database() -> AsyncGenerator[None, None]:
    await truncate_tables()
    yield
    await truncate_tables()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


def pytest_sessionstart(session: Session) -> None:
    if not settings.DEBUG:
        raise RuntimeError("Tests can only be run in debug mode")
