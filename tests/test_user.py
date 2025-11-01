import pytest
from httpx import AsyncClient

from src.repositories import user_repository
from tests.data import user_data
from tests.utils import create_user, get_auth_headers, omit_keys


class TestUserPositiveCases:
    @pytest.mark.asyncio
    async def test_create_user(self, client: AsyncClient) -> None:
        request_data = {
            "first_name": user_data[0]["first_name"],
            "last_name": user_data[0]["last_name"],
            "email": user_data[0]["email"],
            "password": user_data[0]["password"],
        }
        response = await client.post(url="/users/", json=request_data)

        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert omit_keys(response_data, "id") == omit_keys(request_data, "password")
        assert await user_repository.retrieve_or_none(**omit_keys(request_data, "password"))

    @pytest.mark.asyncio
    async def test_retrieve_user(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        response = await client.get(url="/users/me", headers=get_auth_headers(user_data[0]))

        assert response.status_code == 200
        assert response.json() == omit_keys(user_data[0], "password")

    @pytest.mark.asyncio
    async def test_update_user(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        request_data = {
            "first_name": user_data[1]["first_name"],
            "email": user_data[1]["email"],
        }
        response = await client.put(url="/users/me", headers=get_auth_headers(user_data[0]), json=request_data)
        updated_task_data = omit_keys({**user_data[0], **request_data}, "password")

        assert response.status_code == 200
        assert response.json() == updated_task_data
        assert await user_repository.retrieve_or_none(**updated_task_data)

    @pytest.mark.asyncio
    async def test_destroy_user(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        response = await client.delete(url="/users/me", headers=get_auth_headers(user_data[0]))

        assert response.status_code == 204
        assert response.text == ""
        assert not await user_repository.list()


class TestUserNegativeCases:
    @pytest.mark.asyncio
    async def test_create_user_without_email(self, client: AsyncClient) -> None:
        request_data = {
            "first_name": user_data[0]["first_name"],
            "last_name": user_data[0]["last_name"],
            "password": user_data[0]["password"],
        }
        response = await client.post(url="/users/", json=request_data)

        assert response.status_code == 422
        assert response.json()["detail"][0] == {
            "type": "missing",
            "loc": ["body", "email"],
            "msg": "Field required",
            "input": request_data,
        }
        assert not await user_repository.list()

    @pytest.mark.asyncio
    async def test_create_user_with_too_short_password(self, client: AsyncClient) -> None:
        request_data = {
            "first_name": user_data[0]["first_name"],
            "last_name": user_data[0]["last_name"],
            "email": user_data[0]["email"],
            "password": "",
        }
        response = await client.post(url="/users/", json=request_data)

        assert response.status_code == 422
        assert response.json()["detail"][0] == {
            "type": "string_too_short",
            "loc": ["body", "password"],
            "msg": "String should have at least 5 characters",
            "ctx": {"min_length": 5},
            "input": "",
        }
        assert not await user_repository.list()

    @pytest.mark.asyncio
    async def test_create_user_with_incorrect_email(self, client: AsyncClient) -> None:
        request_data = {
            "first_name": user_data[0]["first_name"],
            "last_name": user_data[0]["last_name"],
            "email": "",
            "password": user_data[0]["password"],
        }
        response = await client.post(url="/users/", json=request_data)

        assert response.status_code == 422
        assert response.json()["detail"][0] == {
            "type": "value_error",
            "loc": ["body", "email"],
            "msg": "value is not a valid email address: An email address must have an @-sign.",
            "ctx": {"reason": "An email address must have an @-sign."},
            "input": "",
        }
        assert not await user_repository.list()

    @pytest.mark.asyncio
    async def test_create_user_with_used_email(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        request_data = {
            "first_name": user_data[0]["first_name"],
            "last_name": user_data[0]["last_name"],
            "email": user_data[0]["email"],
            "password": user_data[0]["password"],
        }
        response = await client.post(url="/users/", json=request_data)

        assert response.status_code == 400
        assert response.json()["detail"] == "Email is already in use"

    @pytest.mark.asyncio
    async def test_retrieve_user_with_invalid_token(self, client: AsyncClient) -> None:
        response = await client.get(url="/users/me", headers={"Authorization": "Bearer incorrect_token"})

        assert response.status_code == 403
        assert response.json()["detail"] == "Token is invalid"

    @pytest.mark.asyncio
    async def test_update_user_with_used_email(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        await create_user(user_data[1])
        request_data = {
            "email": user_data[1]["email"],
        }
        response = await client.put(url="/users/me", headers=get_auth_headers(user_data[0]), json=request_data)

        assert response.status_code == 400
        assert response.json()["detail"] == "Email is already in use"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", ["get", "put", "delete"])
    async def test_user_with_non_existing_id(self, client: AsyncClient, method: str) -> None:
        response = await client.request(
            method=method, url="/users/me", headers=get_auth_headers(user_data[0]), json={}
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "No matching data found"
