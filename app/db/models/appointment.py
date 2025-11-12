from datetime import datetime, date, time
from sqlalchemy import Column, Integer, ForeignKey, Date, Time, Float, String, Enum, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class AppointmentStatus(enum.Enum):
    booked = "booked"
    cancelled = "cancelled"
    rescheduled = "rescheduled"
    completed = "completed"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id", ondelete="CASCADE"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    fee = Column(Float, default=0.0)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.booked)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = relationship("User", back_populates="appointments")
    doctor = relationship("DoctorProfile", back_populates="appointments")
    notifications = relationship("Notification", back_populates="appointment", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="appointment", cascade="all, delete-orphan")
