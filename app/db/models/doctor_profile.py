from datetime import datetime
import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    
    specialization = Column(String(100), nullable=False)
    about = Column(Text, nullable=True) 
    consultation_fee = Column(Float, default=0.0)
    languages = Column(String(100), nullable=True)  
    photo_url = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    user = relationship("User", back_populates="doctor_profile")
    appointments = relationship("Appointment", back_populates="doctor")
    availability_slots = relationship("DoctorAvailability", back_populates="doctor")

