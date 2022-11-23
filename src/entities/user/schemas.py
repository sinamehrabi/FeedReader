import datetime
from pydantic import BaseModel, EmailStr


class UserSignDTO(BaseModel):
    email: EmailStr
    password: str


class UserInfoDTO(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime.datetime


class UserTokenDTO(BaseModel):
    access_token: str
    refresh_token: str
