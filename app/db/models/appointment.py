# app/db/models/appointment.py

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Enum, Float, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
import enum

class AppointmentStatus(str, enum.Enum):
    BOOKED = "booked"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"
    COMPLETED = "completed"

class PaymentStatus(str, enum.Enum):
    PAID = "paid"
    PENDING = "pending"
    NOT_REQUIRED = "not_required"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor_profiles.id", ondelete="CASCADE"), nullable=False)
    branch_id = Column(Integer, ForeignKey("hospital_branches.id", ondelete="SET NULL"), nullable=True)

    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.BOOKED, nullable=False)

    booking_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    fee = Column(Float, default=0.0)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.NOT_REQUIRED)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("User", back_populates="appointments")
    doctor = relationship("DoctorProfile", back_populates="appointments")
    branch = relationship("HospitalBranch", back_populates="appointments")
