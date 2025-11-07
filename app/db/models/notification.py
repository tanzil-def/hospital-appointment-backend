from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as PgEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="SET NULL"), nullable=True)
    type = Column(PgEnum(NotificationType), nullable=False)
    message = Column(String(500), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="notifications")
    appointment = relationship("Appointment", back_populates="notifications")
