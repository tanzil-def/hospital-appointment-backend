from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.insurance import Insurance
from app.schemas.insurance import InsuranceCreate, InsuranceUpdate
from typing import List

# Create new insurance
async def create_insurance(db: AsyncSession, insurance_in: InsuranceCreate) -> Insurance:
    insurance = Insurance(**insurance_in.dict())
    db.add(insurance)
    await db.commit()
    await db.refresh(insurance)
    return insurance

# Get insurance by ID
async def get_insurance_by_id(db: AsyncSession, insurance_id: int) -> Insurance | None:
    result = await db.execute(select(Insurance).where(Insurance.id == insurance_id))
    return result.scalars().first()

# Get insurance by user
async def get_insurance_by_user(db: AsyncSession, user_id: int) -> List[Insurance]:
    result = await db.execute(select(Insurance).where(Insurance.user_id == user_id))
    return result.scalars().all()

# Update verification status
async def update_insurance_verification(db: AsyncSession, insurance: Insurance, update_in: InsuranceUpdate) -> Insurance:
    insurance.verified_status = update_in.verified_status
    db.add(insurance)
    await db.commit()
    await db.refresh(insurance)
    return insurance

# Delete insurance
async def delete_insurance(db: AsyncSession, insurance: Insurance):
    await db.delete(insurance)
    await db.commit()
