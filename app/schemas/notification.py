from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"

class NotificationBase(BaseModel):
    user_id: int
    type: NotificationType
    message: str
    appointment_id: Optional[int] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    type: Optional[NotificationType] = None
    message: Optional[str] = None
    appointment_id: Optional[int] = None

class NotificationOut(NotificationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 compatible
