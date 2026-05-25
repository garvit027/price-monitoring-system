from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    telegram_chat_id: Optional[str] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    telegram_chat_id: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
