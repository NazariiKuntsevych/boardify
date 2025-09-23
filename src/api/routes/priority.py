from fastapi import APIRouter

from ...models import Priority
from ...repositories import priority_repository
from ...schemas import PriorityRead

router = APIRouter(prefix="/priorities")


@router.get("/", status_code=200, response_model=list[PriorityRead])
async def get_priorities() -> list[Priority]:
    return await priority_repository.get(many=True)
