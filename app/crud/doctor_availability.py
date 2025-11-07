from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.doctor_availability import DoctorAvailability
from app.schemas.doctor_availability import DoctorAvailabilityCreate, DoctorAvailabilityUpdate

async def get_availability(db: AsyncSession, availability_id: int):
    result = await db.execute(select(DoctorAvailability).where(DoctorAvailability.id == availability_id))
    return result.scalars().first()

async def get_availabilities(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(DoctorAvailability).offset(skip).limit(limit))
    return result.scalars().all()

async def create_availability(db: AsyncSession, availability: DoctorAvailabilityCreate):
    db_availability = DoctorAvailability(**availability.dict())
    db.add(db_availability)
    await db.commit()
    await db.refresh(db_availability)
    return db_availability

async def update_availability(db: AsyncSession, availability_id: int, availability: DoctorAvailabilityUpdate):
    db_availability = await get_availability(db, availability_id)
    if not db_availability:
        return None
    for field, value in availability.dict(exclude_unset=True).items():
        setattr(db_availability, field, value)
    await db.commit()
    await db.refresh(db_availability)
    return db_availability

async def delete_availability(db: AsyncSession, availability_id: int):
    db_availability = await get_availability(db, availability_id)
    if not db_availability:
        return None
    await db.delete(db_availability)
    await db.commit()
    return db_availability
