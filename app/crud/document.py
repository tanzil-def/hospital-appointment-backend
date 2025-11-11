from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.document import Document
from app.schemas.document import DocumentCreate
from typing import List, Optional

# Create a document
async def create_document(db: AsyncSession, document: DocumentCreate) -> Document:
    db_document = Document(
        appointment_id=document.appointment_id,
        file_name=document.file_name,
        file_path=document.file_path,
        file_type=document.file_type
    )
    db.add(db_document)
    await db.commit()
    await db.refresh(db_document)
    return db_document

# Get documents by appointment
async def get_documents_by_appointment(db: AsyncSession, appointment_id: int) -> List[Document]:
    result = await db.execute(select(Document).where(Document.appointment_id == appointment_id))
    return result.scalars().all()

# Get document by ID
async def get_document_by_id(db: AsyncSession, document_id: int) -> Optional[Document]:
    result = await db.execute(select(Document).where(Document.id == document_id))
    return result.scalar_one_or_none()

# Delete document
async def delete_document(db: AsyncSession, document_id: int) -> None:
    doc = await get_document_by_id(db, document_id)
    if doc:
        await db.delete(doc)
        await db.commit()
