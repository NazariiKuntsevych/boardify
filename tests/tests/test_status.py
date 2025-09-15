import pytest
from httpx import AsyncClient

from tests.utils import get_statuses


class TestStatusPositiveCases:
    @pytest.mark.asyncio
    async def test_get_statuses(self, client: AsyncClient) -> None:
        response = await client.get(url="/statuses/")

        assert response.status_code == 200
        assert response.json() == await get_statuses()
