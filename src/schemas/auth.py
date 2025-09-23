from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserReadWithToken(BaseModel):
    first_name: str
    last_name: str
    token: str
