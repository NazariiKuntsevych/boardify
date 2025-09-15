import pytest
from httpx import AsyncClient

from src.repositories import board_repository
from tests.data import board_data, user_data
from tests.utils import create_board, create_user, get_auth_headers, omit_keys


class TestBoardPositiveCases:
    @pytest.mark.asyncio
    async def test_create_board(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        request_data = {
            "name": board_data[0]["name"],
        }
        response = await client.post(url="/boards/", headers=get_auth_headers(user_data[0]), json=request_data)

        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert omit_keys(response_data, "id") == request_data
        assert await board_repository.get(**request_data)

    @pytest.mark.asyncio
    async def test_get_board(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        await create_board(board_data[0], user_id=user_data[0]["id"])
        response = await client.get(url=f"/boards/{board_data[0]['id']}", headers=get_auth_headers(user_data[0]))

        assert response.status_code == 200
        assert response.json() == board_data[0]

    @pytest.mark.asyncio
    async def test_get_boards(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        await create_board(board_data[0], user_id=user_data[0]["id"])
        await create_board(board_data[1], user_id=user_data[0]["id"])

        await create_user(user_data[1])
        await create_board(board_data[2], user_id=user_data[1]["id"])
        response = await client.get(url="/boards/", headers=get_auth_headers(user_data[0]))

        assert response.status_code == 200
        assert response.json() == [board_data[0], board_data[1]]

    @pytest.mark.asyncio
    async def test_update_board(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        await create_board(board_data[0], user_id=user_data[0]["id"])
        request_data = {
            "name": board_data[1]["name"],
        }
        response = await client.put(
            url=f"/boards/{board_data[0]['id']}", headers=get_auth_headers(user_data[0]), json=request_data
        )
        updated_board_data = {**board_data[0], **request_data}

        assert response.status_code == 200
        assert response.json() == updated_board_data
        assert await board_repository.get(**updated_board_data)

    @pytest.mark.asyncio
    async def test_delete_board(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        await create_board(board_data[0], user_id=user_data[0]["id"])
        response = await client.delete(
            url=f"/boards/{board_data[0]['id']}", headers=get_auth_headers(user_data[0])
        )

        assert response.status_code == 204
        assert response.text == ""
        assert not await board_repository.get(many=True)


class TestBoardNegativeCases:
    @pytest.mark.asyncio
    async def test_create_board_without_name(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        request_data = {}
        response = await client.post(url="/boards/", headers=get_auth_headers(user_data[0]), json=request_data)

        assert response.status_code == 422
        assert response.json()["detail"][0] == {
            "type": "missing",
            "loc": ["body", "name"],
            "msg": "Field required",
            "input": request_data,
        }
        assert not await board_repository.get(many=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("headers, status_code, detail", [
        ({"Authorization": "Bearer incorrect_token"}, 403, "Token is invalid"),
        (get_auth_headers(user_data[0]), 404, "Board does not exist"),
    ])
    async def test_get_board_with_invalid_token_or_non_existing_id(
        self, client: AsyncClient, headers: dict, status_code: int, detail: str
    ) -> None:
        await create_user(user_data[0])
        response = await client.get(url=f"/boards/{board_data[0]['id']}", headers=headers)

        assert response.status_code == status_code
        assert response.json()["detail"] == detail
