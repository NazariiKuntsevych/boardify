from typing import Type, TypeVar, Union

from fastapi import HTTPException
from sqlalchemy import select

from ..database import get_session

ORMModel = TypeVar("ORMModel")


class Repository:
    def __init__(self, model: Type[ORMModel]):
        self.model = model

    async def create(self, **data) -> ORMModel:
        instance = self.model(**data)
        async with get_session() as session:
            session.add(instance)
            return instance

    async def get(self, many: bool = False, **filters) -> Union[ORMModel, list[ORMModel]]:
        async with get_session() as session:
            result = await session.execute(
                select(self.model).filter_by(**filters)
            )
            return list(result.scalars()) if many else result.scalar_one_or_none()

    async def get_or_404(self, **filters) -> ORMModel:
        instance = await self.get(**filters)
        if not instance:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} does not exist")
        return instance

    @staticmethod
    async def update(instance: ORMModel, **data) -> None:
        async with get_session() as session:
            for key, value in data.items():
                if value is not None:
                    setattr(instance, key, value)
            session.add(instance)

    @staticmethod
    async def delete(instance: ORMModel) -> None:
        async with get_session() as session:
            await session.delete(instance)

    async def truncate(self) -> None:
        async with get_session() as session:
            for instance in await self.get(many=True):
                await session.delete(instance)
