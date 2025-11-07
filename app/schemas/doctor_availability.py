
from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

class DoctorAvailabilityBase(BaseModel):
    available_date: date
    start_time: time
    end_time: time
    is_holiday: Optional[bool] = False
    notes: Optional[str] = None

class DoctorAvailabilityCreate(DoctorAvailabilityBase):
    doctor_id: int

class DoctorAvailabilityUpdate(BaseModel):
    available_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_holiday: Optional[bool] = None
    notes: Optional[str] = None

class DoctorAvailabilityOut(DoctorAvailabilityBase):
    id: int
    doctor_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  
