from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import shutil
from pathlib import Path

from app.crud.document import create_document, get_documents_by_appointment
from app.schemas.document import DocumentCreate, DocumentRead
from app.db.session import get_db

router = APIRouter(prefix="/documents", tags=["Documents"])

# Upload directory
UPLOAD_DIR = Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Upload a document
@router.post("/", response_model=DocumentRead)
async def upload_document(appointment_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    file_path = UPLOAD_DIR / file.filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    document_in = DocumentCreate(
        appointment_id=appointment_id,
        file_name=file.filename,
        file_path=str(file_path),
        file_type=file.content_type
    )
    document = await create_document(db, document_in)
    return document

# List documents by appointment
@router.get("/{appointment_id}", response_model=List[DocumentRead])
async def list_documents(appointment_id: int, db: AsyncSession = Depends(get_db)):
    documents = await get_documents_by_appointment(db, appointment_id)
    return documents
