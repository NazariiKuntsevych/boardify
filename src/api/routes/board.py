from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path

from ...models import Board
from ...repositories import board_repository
from ...schemas import BoardCreate, BoardRead, BoardUpdate
from ..dependencies import get_user_id_from_token

router = APIRouter(prefix="/boards")


@router.post("/", status_code=201, response_model=BoardRead)
async def create_board(
    user_id: Annotated[int, Depends(get_user_id_from_token)],
    board_in: Annotated[BoardCreate, Body()],
) -> Board:
    return await board_repository.create(**board_in.model_dump(exclude_unset=True), user_id=user_id)


@router.get("/", status_code=200, response_model=list[BoardRead])
async def list_boards(
    user_id: Annotated[int, Depends(get_user_id_from_token)],
) -> list[Board]:
    return await board_repository.list(user_id=user_id)


@router.get("/{board_id}", status_code=200, response_model=BoardRead)
async def retrieve_board(
    user_id: Annotated[int, Depends(get_user_id_from_token)],
    board_id: Annotated[int, Path],
) -> Board:
    return await board_repository.retrieve(id=board_id, user_id=user_id)


@router.put("/{board_id}", status_code=200, response_model=BoardRead)
async def update_board(
    user_id: Annotated[int, Depends(get_user_id_from_token)],
    board_id: Annotated[int, Path],
    board_in: Annotated[BoardUpdate, Body()],
) -> Board:
    return await board_repository.update(_data=board_in.model_dump(exclude_unset=True), id=board_id, user_id=user_id)


@router.delete("/{board_id}", status_code=204)
async def destroy_board(
    user_id: Annotated[int, Depends(get_user_id_from_token)],
    board_id: Annotated[int, Path],
) -> None:
    await board_repository.destroy(id=board_id, user_id=user_id)
