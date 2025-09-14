from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ...models import Board, Task
from ...repositories import task_repository
from ...schemas import TaskCreate, TaskRead, TaskUpdate
from ..dependencies import get_board_by_id, get_task_by_id

router = APIRouter(prefix="/boards/{board_id:int}/tasks")


@router.post("/", status_code=201, response_model=TaskRead)
async def create_task(
    board: Annotated[Board, Depends(get_board_by_id)],
    task_in: Annotated[TaskCreate, Body()],
) -> Task:
    return await task_repository.create(**task_in.model_dump(), board=board)


@router.get("/", status_code=200, response_model=list[TaskRead])
async def get_tasks(
    board: Annotated[Board, Depends(get_board_by_id)],
) -> list[Task]:
    return await task_repository.get(board=board, many=True)


@router.get("/{task_id:int}", status_code=200, response_model=TaskRead)
async def get_task(
    task: Annotated[Task, Depends(get_task_by_id)],
) -> Task:
    return task


@router.put("/{task_id:int}", status_code=200, response_model=TaskRead)
async def update_task(
    task_in: Annotated[TaskUpdate, Body()],
    task: Annotated[Task, Depends(get_task_by_id)],
) -> Task:
    await task_repository.update(task, **task_in.model_dump())
    return task


@router.delete("/{task_id:int}", status_code=204)
async def delete_task(
    task: Annotated[Task, Depends(get_task_by_id)],
) -> None:
    await task_repository.delete(task)
