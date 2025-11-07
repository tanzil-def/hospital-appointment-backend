from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

# Enum for user roles
class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"

# Base schema shared by multiple schemas
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str

# Schema for creating a new user
class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.patient  # default role is patient

# Schema for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for updating user
class UserUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    role: Optional[UserRole]
    is_active: Optional[bool]

# Schema for reading user data
class UserRead(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Pydantic v2 config
    model_config = {
        "from_attributes": True
    }
