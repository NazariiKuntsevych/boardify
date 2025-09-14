from pydantic import BaseModel


class StatusRead(BaseModel):
    id: int
    name: str
