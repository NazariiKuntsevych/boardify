from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from ..models import User
from ..repositories import user_repository
from ..security import decode_token


async def get_user_from_token(
    token: Annotated[str, Depends(HTTPBearer())],
) -> User:
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=403, detail="Token is invalid")

    return await user_repository.get_or_404(id=payload["user_id"])
