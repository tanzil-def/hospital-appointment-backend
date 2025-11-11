from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
from enum import Enum

class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"

class Gender(str, Enum):
    male = "male"
    female = "female"
    others = "others"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default=UserRole.patient.value)
    gender = Column(String(20), default=Gender.others.value)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor_profile = relationship("DoctorProfile", back_populates="user", uselist=False)
    appointments = relationship("Appointment", back_populates="patient")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    insurances = relationship("Insurance", back_populates="user", cascade="all, delete-orphan")
