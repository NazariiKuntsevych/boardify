from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException

from ...models import User
from ...repositories import user_repository
from ...schemas import UserCreate, UserRead, UserUpdate
from ..dependencies import get_user_from_token

router = APIRouter(prefix="/users")


@router.post("/", status_code=201, response_model=UserRead)
async def create_user(
    user_in: Annotated[UserCreate, Body()],
) -> User:
    user_by_email = await user_repository.get(email=user_in.email)
    if user_by_email:
        raise HTTPException(status_code=400, detail="Email is already in use")

    return await user_repository.create(**user_in.model_dump())


@router.get("/me", status_code=200, response_model=UserRead)
async def get_user(
    user: Annotated[User, Depends(get_user_from_token)],
) -> User:
    return user


@router.put("/me", status_code=200, response_model=UserRead)
async def update_user(
    user_in: Annotated[UserUpdate, Body()],
    user: Annotated[User, Depends(get_user_from_token)],
) -> User:
    if user_in.email:
        user_by_email = await user_repository.get(email=user_in.email)
        if user_by_email and user != user_by_email:
            raise HTTPException(status_code=400, detail="Email is already in use")

    await user_repository.update(user, **user_in.model_dump())
    return user


@router.delete("/me", status_code=204)
async def delete_user(
    user: Annotated[User, Depends(get_user_from_token)],
) -> None:
    await user_repository.delete(user)
