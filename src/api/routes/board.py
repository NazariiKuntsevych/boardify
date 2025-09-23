from typing import Annotated

from fastapi import APIRouter, Body, Depends

from ...models import Board, User
from ...repositories import board_repository
from ...schemas import BoardCreate, BoardRead, BoardUpdate
from ..dependencies import get_board_by_id, get_user_from_token

router = APIRouter(prefix="/boards")


@router.post("/", status_code=201, response_model=BoardRead)
async def create_board(
    board_in: Annotated[BoardCreate, Body()],
    user: Annotated[User, Depends(get_user_from_token)],
) -> Board:
    return await board_repository.create(**board_in.model_dump(), user=user)


@router.get("/", status_code=200, response_model=list[BoardRead])
async def get_boards(
    user: Annotated[User, Depends(get_user_from_token)],
) -> list[Board]:
    return await board_repository.get(user=user, many=True)


@router.get("/{board_id:int}", status_code=200, response_model=BoardRead)
async def get_board(
    board: Annotated[Board, Depends(get_board_by_id)],
) -> Board:
    return board


@router.put("/{board_id:int}", status_code=200, response_model=BoardRead)
async def update_board(
    board_in: Annotated[BoardUpdate, Body()],
    board: Annotated[Board, Depends(get_board_by_id)],
) -> Board:
    await board_repository.update(board, **board_in.model_dump())
    return board


@router.delete("/{board_id:int}", status_code=204)
async def delete_board(
    board: Annotated[Board, Depends(get_board_by_id)],
) -> None:
    await board_repository.delete(board)
