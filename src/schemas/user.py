from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)


class UserCreate(UserBase):
    password: str = Field(min_length=5, max_length=50)


class UserRead(UserBase):
    id: int


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=50)
    last_name: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = Field(default=None, max_length=50)
    password: Optional[str] = Field(default=None, min_length=5, max_length=50)
