from typing import Annotated

from fastapi import APIRouter, Body, HTTPException

from ...models import User
from ...repositories import user_repository
from ...schemas import UserLogin, UserReadWithToken
from ...security import encode_token

router = APIRouter(prefix="/auth")


@router.post("/login", status_code=200, response_model=UserReadWithToken)
async def login_user(
    user_in: Annotated[UserLogin, Body()],
) -> User:
    user = await user_repository.get(email=user_in.email)
    if not user or not user_repository.check_password(user, user_in.password):
        raise HTTPException(status_code=403, detail="Incorrect email or password")

    user.token = encode_token({"user_id": user.id})
    return user
