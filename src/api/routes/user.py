from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException

from ...models import User
from ...repositories import user_repository
from ...schemas import UserCreate, UserRead, UserUpdate
from ..dependencies import get_user_id_from_token

router = APIRouter(prefix="/users")


@router.post("/", status_code=201, response_model=UserRead)
async def create_user(
    user_in: Annotated[UserCreate, Body()],
) -> User:
    user_by_email = await user_repository.retrieve_or_none(email=user_in.email)
    if user_by_email:
        raise HTTPException(status_code=400, detail="Email is already in use")

    return await user_repository.create(**user_in.model_dump(exclude_unset=True))


@router.get("/me", status_code=200, response_model=UserRead)
async def retrieve_user(
    user_id: Annotated[int, Depends(get_user_id_from_token)],
) -> User:
    return await user_repository.retrieve(id=user_id)


@router.put("/me", status_code=200, response_model=UserRead)
async def update_user(
    user_id: Annotated[int, Depends(get_user_id_from_token)],
    user_in: Annotated[UserUpdate, Body()],
) -> User:
    if user_in.email:
        user_by_email = await user_repository.retrieve_or_none(email=user_in.email)
        if user_by_email and user_id != user_by_email.id:
            raise HTTPException(status_code=400, detail="Email is already in use")

    return await user_repository.update(_data=user_in.model_dump(exclude_unset=True), id=user_id)


@router.delete("/me", status_code=204)
async def destroy_user(
    user_id: Annotated[int, Depends(get_user_id_from_token)],
) -> None:
    await user_repository.destroy(id=user_id)
