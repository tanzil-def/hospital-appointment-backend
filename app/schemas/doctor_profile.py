from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DoctorProfileBase(BaseModel):
    specialization: str
    about: Optional[str] = None
    consultation_fee: Optional[float] = 0.0
    languages: Optional[str] = None
    photo_url: Optional[str] = None

class DoctorProfileCreate(DoctorProfileBase):
    user_id: int

class DoctorProfileUpdate(BaseModel):
    specialization: Optional[str] = None
    about: Optional[str] = None
    consultation_fee: Optional[float] = None
    languages: Optional[str] = None
    photo_url: Optional[str] = None

class DoctorProfileOut(DoctorProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  
