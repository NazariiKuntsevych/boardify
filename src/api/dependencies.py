from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..security import decode_token


async def get_user_id_from_token(
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
) -> int:
    payload = decode_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=403, detail="Token is invalid")

    return payload["user_id"]
