from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    role: Optional[str] = None
    password_hash: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    password_hash: Optional[str] = None


class UserResponse(BaseModel):
    user_id: int
    full_name: str
    email: str
    phone: Optional[str]
    role: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)