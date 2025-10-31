from typing import Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(max_length=50)
    body: str = Field(max_length=255)
    status_id: int
    priority_id: int


class TaskRead(TaskCreate):
    id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=50)
    body: Optional[str] = Field(default=None, max_length=255)
    status_id: Optional[int] = Field(default=None)
    priority_id: Optional[int] = Field(default=None)
