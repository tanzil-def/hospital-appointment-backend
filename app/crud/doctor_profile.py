from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.doctor_profile import DoctorProfile
from app.schemas.doctor_profile import DoctorProfileCreate, DoctorProfileUpdate

async def get_doctor_profile(db: AsyncSession, doctor_id: int):
    result = await db.execute(select(DoctorProfile).where(DoctorProfile.id == doctor_id))
    return result.scalars().first()

async def get_doctor_profiles(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(DoctorProfile).offset(skip).limit(limit))
    return result.scalars().all()

async def create_doctor_profile(db: AsyncSession, profile: DoctorProfileCreate):
    db_profile = DoctorProfile(**profile.dict())
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    return db_profile

async def update_doctor_profile(db: AsyncSession, doctor_id: int, profile: DoctorProfileUpdate):
    db_profile = await get_doctor_profile(db, doctor_id)
    if not db_profile:
        return None
    for field, value in profile.dict(exclude_unset=True).items():
        setattr(db_profile, field, value)
    await db.commit()
    await db.refresh(db_profile)
    return db_profile

async def delete_doctor_profile(db: AsyncSession, doctor_id: int):
    db_profile = await get_doctor_profile(db, doctor_id)
    if not db_profile:
        return None
    await db.delete(db_profile)
    await db.commit()
    return db_profile
