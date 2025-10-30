from ..models import User
from ..security import hash_password
from .base import ORMModel, Repository


class UserRepository(Repository):
    async def create(self, **data) -> ORMModel:
        data["password"] = hash_password(data["password"])
        return await super().create(**data)


repository = UserRepository(model=User)
