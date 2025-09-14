from typing import Optional

from pydantic import BaseModel, Field


class BoardCreate(BaseModel):
    name: str = Field(max_length=50)


class BoardRead(BoardCreate):
    id: int


class BoardUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=50)
