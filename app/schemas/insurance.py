from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Request schema for creating insurance
class InsuranceCreate(BaseModel):
    user_id: int
    provider_name: str
    policy_number: str
    coverage_details: Optional[str] = None

# Response schema for reading insurance
class InsuranceRead(BaseModel):
    id: int
    user_id: int
    provider_name: str
    policy_number: str
    coverage_details: Optional[str] = None
    verified_status: bool
    created_at: datetime

    class Config:
        orm_mode = True

# Optional schema for updating verification status
class InsuranceUpdate(BaseModel):
    verified_status: bool
