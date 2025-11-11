from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    appointment_id: int
    file_name: str
    file_path: str
    file_type: str

class DocumentCreate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True  
