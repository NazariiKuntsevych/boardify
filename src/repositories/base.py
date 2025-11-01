from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.orm import DeclarativeBase

from ..database import get_session

ORMModel = TypeVar("ORMModel", bound=DeclarativeBase)


class NotFoundError(Exception):
    pass


class Repository(Generic[ORMModel]):
    def __init__(self, model: Type[ORMModel]):
        self.model = model

    async def create(self, **data) -> ORMModel:
        async with get_session() as session:
            instance = self.model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def retrieve_or_none(self, **filters) -> Optional[ORMModel]:
        async with get_session() as session:
            return await session.scalar(
                select(self.model).filter_by(**filters)
            )

    async def retrieve(self, **filters) -> ORMModel:
        instance = await self.retrieve_or_none(**filters)
        if not instance:
            raise NotFoundError
        return instance

    async def list(self, **filters) -> list[ORMModel]:
        async with get_session() as session:
            result = await session.scalars(
                select(self.model).filter_by(**filters)
            )
            return result.all()

    async def update(self, _data: dict, **filters) -> ORMModel:
        async with get_session() as session:
            instance = await session.scalar(
                select(self.model).filter_by(**filters)
            )
            if not instance:
                raise NotFoundError

            for key, value in _data.items():
                setattr(instance, key, value)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def destroy(self, **filters) -> None:
        async with get_session() as session:
            instance = await session.scalar(
                select(self.model).filter_by(**filters)
            )
            if not instance:
                raise NotFoundError

            await session.delete(instance)
            await session.commit()

    async def clear(self) -> None:
        async with get_session() as session:
            await session.execute(delete(self.model))
            await session.commit()
