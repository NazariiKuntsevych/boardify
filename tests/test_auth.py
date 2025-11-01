import pytest
from httpx import AsyncClient

from tests.data import user_data
from tests.utils import create_user, omit_keys


class TestAuthPositiveCases:
    @pytest.mark.asyncio
    async def test_login_user(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        request_data = {
            "email": user_data[0]["email"],
            "password": user_data[0]["password"],
        }
        response = await client.post(url="/auth/login", json=request_data)

        assert response.status_code == 200
        response_data = response.json()
        assert "token" in response_data
        assert omit_keys(response_data, "token") == {
            "first_name": user_data[0]["first_name"],
            "last_name": user_data[0]["last_name"],
        }


class TestAuthNegativeCases:
    @pytest.mark.asyncio
    async def test_login_user_with_incorrect_password(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        request_data = {
            "email": user_data[0]["email"],
            "password": user_data[1]["password"],
        }
        response = await client.post(url="/auth/login", json=request_data)

        assert response.status_code == 403
        assert response.json()["detail"] == "Incorrect email or password"
