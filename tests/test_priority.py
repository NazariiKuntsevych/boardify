import pytest
from httpx import AsyncClient

from tests.utils import get_priorities


class TestPriorityPositiveCases:
    @pytest.mark.asyncio
    async def test_get_priorities(self, client: AsyncClient) -> None:
        response = await client.get(url="/priorities/")

        assert response.status_code == 200
        assert response.json() == await get_priorities()
