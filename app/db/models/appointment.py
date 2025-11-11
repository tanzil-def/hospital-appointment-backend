from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id", ondelete="CASCADE"))
    scheduled_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = relationship("User", back_populates="appointments")
    doctor = relationship("DoctorProfile", back_populates="appointments")

    notifications = relationship("Notification", back_populates="appointment", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="appointment", cascade="all, delete-orphan")
