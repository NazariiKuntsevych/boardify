from fastapi import APIRouter

from ...models import Status
from ...repositories import status_repository
from ...schemas import StatusRead

router = APIRouter(prefix="/statuses")


@router.get("/", status_code=200, response_model=list[StatusRead])
async def get_statuses() -> list[Status]:
    return await status_repository.get(many=True)
