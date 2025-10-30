from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path

from ...models import Board, Task
from ...repositories import board_repository, task_repository
from ...schemas import TaskCreate, TaskRead, TaskUpdate
from ..dependencies import get_user_id_from_token

router = APIRouter(prefix="/boards/{board_id}/tasks")


async def retrieve_board(
    user_id: Annotated[int, Depends(get_user_id_from_token)],
    board_id: Annotated[int, Path],
) -> Board:
    return await board_repository.retrieve(id=board_id, user_id=user_id)


@router.post("/", status_code=201, response_model=TaskRead)
async def create_task(
    board: Annotated[Board, Depends(retrieve_board)],
    task_in: Annotated[TaskCreate, Body()],
) -> Task:
    return await task_repository.create(**task_in.model_dump(exclude_unset=True), board=board)


@router.get("/", status_code=200, response_model=list[TaskRead])
async def list_tasks(
    board: Annotated[Board, Depends(retrieve_board)],
) -> list[Task]:
    return await task_repository.list(board=board)


@router.get("/{task_id}", status_code=200, response_model=TaskRead)
async def retrieve_task(
    board: Annotated[Board, Depends(retrieve_board)],
    task_id: Annotated[int, Path],
) -> Task:
    return await task_repository.retrieve(id=task_id, board=board)


@router.put("/{task_id}", status_code=200, response_model=TaskRead)
async def update_task(
    board: Annotated[Board, Depends(retrieve_board)],
    task_id: Annotated[int, Path],
    task_in: Annotated[TaskUpdate, Body()],
) -> Task:
    return await task_repository.update(_data=task_in.model_dump(exclude_unset=True), id=task_id, board=board)


@router.delete("/{task_id}", status_code=204)
async def destroy_task(
    board: Annotated[Board, Depends(retrieve_board)],
    task_id: Annotated[int, Path],
) -> None:
    await task_repository.destroy(id=task_id, board=board)
