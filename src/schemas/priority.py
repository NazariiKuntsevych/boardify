from pydantic import BaseModel


class PriorityRead(BaseModel):
    id: int
    name: str
