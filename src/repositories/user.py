from ..models import User
from ..security import check_password, hash_password
from .base import ORMModel, Repository


class UserRepository(Repository):
    async def create(self, **data) -> ORMModel:
        data["password"] = hash_password(data["password"])
        return await super().create(**data)

    @staticmethod
    def check_password(instance: ORMModel, password: str) -> bool:
        return check_password(password, instance.password)


repository = UserRepository(model=User)
