import pytest
from httpx import AsyncClient

from src.repositories import task_repository
from tests.data import board_data, task_data, user_data
from tests.utils import create_board, create_task, create_user, get_auth_headers, omit_keys


class TestTaskPositiveCases:
    @pytest.mark.asyncio
    async def test_create_task(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        await create_board(board_data[0], user_id=user_data[0]["id"])
        request_data = {
            "title": task_data[0]["title"],
            "body": task_data[0]["body"],
            "status_id": task_data[0]["status_id"],
            "priority_id": task_data[0]["priority_id"],
        }
        response = await client.post(
            url=f"/boards/{board_data[0]['id']}/tasks/",
            headers=get_auth_headers(user_data[0]),
            json=request_data,
        )

        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert omit_keys(response_data, "id") == request_data
        assert await task_repository.get(**request_data)

    @pytest.mark.asyncio
    async def test_get_task(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        await create_board(board_data[0], user_id=user_data[0]["id"])
        await create_task(task_data[0], board_id=board_data[0]["id"])
        response = await client.get(
            url=f"/boards/{board_data[0]['id']}/tasks/{task_data[0]['id']}",
            headers=get_auth_headers(user_data[0]),
        )

        assert response.status_code == 200
        assert response.json() == task_data[0]

    @pytest.mark.asyncio
    async def test_get_tasks(self, client: AsyncClient) -> None:
        await create_user(user_data[0])

        await create_board(board_data[0], user_id=user_data[0]["id"])
        await create_task(task_data[0], board_id=board_data[0]["id"])
        await create_task(task_data[1], board_id=board_data[0]["id"])

        await create_board(board_data[1], user_id=user_data[0]["id"])
        await create_task(task_data[2], board_id=board_data[1]["id"])

        response = await client.get(
            url=f"/boards/{board_data[0]['id']}/tasks/", headers=get_auth_headers(user_data[0])
        )

        assert response.status_code == 200
        assert response.json() == [task_data[0], task_data[1]]

    @pytest.mark.asyncio
    async def test_update_task(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        await create_board(board_data[0], user_id=user_data[0]["id"])
        await create_task(task_data[0], board_id=board_data[0]["id"])
        request_data = {
            "title": task_data[1]["title"],
            "body": task_data[1]["body"],
        }
        response = await client.put(
            url=f"/boards/{board_data[0]['id']}/tasks/{task_data[0]['id']}",
            headers=get_auth_headers(user_data[0]),
            json=request_data,
        )
        updated_task_data = {**task_data[0], **request_data}

        assert response.status_code == 200
        assert response.json() == updated_task_data
        assert await task_repository.get(**updated_task_data)

    @pytest.mark.asyncio
    async def test_delete_task(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        await create_board(board_data[0], user_id=user_data[0]["id"])
        await create_task(task_data[0], board_id=board_data[0]["id"])
        response = await client.delete(
            url=f"/boards/{board_data[0]['id']}/tasks/{task_data[0]['id']}",
            headers=get_auth_headers(user_data[0]),
        )

        assert response.status_code == 204
        assert response.text == ""
        assert not await task_repository.get(many=True)


class TestTaskNegativeCases:
    @pytest.mark.asyncio
    async def test_create_task_without_title(self, client: AsyncClient) -> None:
        await create_user(user_data[0])
        await create_board(board_data[0], user_id=user_data[0]["id"])
        request_data = {
            "body": task_data[0]["body"],
            "status_id": task_data[0]["status_id"],
            "priority_id": task_data[0]["priority_id"],
        }
        response = await client.post(
            url=f"/boards/{board_data[0]['id']}/tasks/",
            headers=get_auth_headers(user_data[0]),
            json=request_data,
        )

        assert response.status_code == 422
        assert response.json()["detail"][0] == {
            "type": "missing",
            "loc": ["body", "title"],
            "msg": "Field required",
            "input": request_data,
        }
        assert not await task_repository.get(many=True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("headers, status_code, detail", [
        ({"Authorization": "Bearer incorrect_token"}, 403, "Token is invalid"),
        (get_auth_headers(user_data[0]), 404, "Task does not exist"),
    ])
    async def test_get_task_with_invalid_token_or_non_existing_id(
        self, client: AsyncClient, headers: dict, status_code: int, detail: str
    ) -> None:
        await create_user(user_data[0])
        await create_board(board_data[0], user_id=user_data[0]["id"])
        response = await client.get(
            url=f"/boards/{board_data[0]['id']}/tasks/{task_data[0]['id']}",
            headers=headers,
        )

        assert response.status_code == status_code
        assert response.json()["detail"] == detail
