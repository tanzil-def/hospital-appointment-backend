from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime
from enum import Enum

class AppointmentStatus(str, Enum):
    booked = "booked"
    cancelled = "cancelled"
    rescheduled = "rescheduled"
    completed = "completed"

class AppointmentBase(BaseModel):
    appointment_date: date
    appointment_time: time
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    patient_id: int
    doctor_id: int
    fee: Optional[float] = 0.0

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None
    fee: Optional[float] = None

class AppointmentOut(AppointmentBase):
    id: int
    patient_id: int
    doctor_id: int
    fee: float
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
