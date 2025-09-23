from typing import Annotated

from fastapi import Depends, HTTPException, Path
from fastapi.security import HTTPBearer

from ..models import Board, User
from ..repositories import board_repository, user_repository
from ..security import decode_token


async def get_user_from_token(
    token: Annotated[str, Depends(HTTPBearer())],
) -> User:
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=403, detail="Token is invalid")

    return await user_repository.get_or_404(id=payload["user_id"])


async def get_board_by_id(
    board_id: Annotated[int, Path],
    user: Annotated[User, Depends(get_user_from_token)],
) -> Board:
    return await board_repository.get_or_404(id=board_id, user=user)
