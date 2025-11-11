from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"

class Gender(str, Enum):
    male = "male"
    female = "female"
    others = "others"

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    gender: Optional[Gender] = Gender.others

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.patient

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    role: Optional[UserRole]
    gender: Optional[Gender]
    is_active: Optional[bool]

class UserRead(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
