from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.patient

class UserUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]

class UserOut(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
