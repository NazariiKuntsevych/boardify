from src.repositories import board_repository, priority_repository, status_repository, task_repository, user_repository
from src.security import encode_token


async def truncate_tables() -> None:
    for repository in board_repository, task_repository, user_repository:
        await repository.truncate()


async def create_user(user_data: dict) -> None:
    await user_repository.create(**user_data)


async def create_board(board_data: dict, user_id: int) -> None:
    await board_repository.create(user_id=user_id, **board_data)


async def create_task(task_data: dict, board_id: int) -> None:
    await task_repository.create(board_id=board_id, **task_data)


async def get_statuses() -> list[dict]:
    return [
        {"id": status.id, "name": status.name}
        for status in
        await status_repository.get(many=True)
    ]


async def get_priorities() -> list[dict]:
    return [
        {"id": priority.id, "name": priority.name}
        for priority in
        await priority_repository.get(many=True)
    ]


def omit_keys(data: dict, *keys) -> dict:
    return {
        key: value
        for key, value in data.items()
        if key not in keys
    }


def get_auth_headers(user_data: dict) -> dict:
    token = encode_token({"user_id": user_data["id"]})
    return {"Authorization": f"Bearer {token}"}
