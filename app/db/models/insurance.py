from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Insurance(Base):
    __tablename__ = "insurances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_name = Column(String, nullable=False)
    policy_number = Column(String, nullable=False, unique=True)
    coverage_details = Column(String, nullable=True)
    verified_status = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="insurances")
