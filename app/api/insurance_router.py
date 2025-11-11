from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.insurance import InsuranceCreate, InsuranceRead, InsuranceUpdate
from app.crud import insurance as crud_insurance
from app.db.session import get_db  # ✅ updated

router = APIRouter(prefix="/insurance", tags=["Insurance"])

@router.post("/", response_model=InsuranceRead)
async def add_insurance(insurance_in: InsuranceCreate, db: AsyncSession = Depends(get_db)):
    return await crud_insurance.create_insurance(db, insurance_in)

@router.get("/{insurance_id}", response_model=InsuranceRead)
async def get_insurance(insurance_id: int, db: AsyncSession = Depends(get_db)):
    insurance = await crud_insurance.get_insurance_by_id(db, insurance_id)
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return insurance

@router.get("/user/{user_id}", response_model=List[InsuranceRead])
async def get_user_insurances(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud_insurance.get_insurance_by_user(db, user_id)

@router.patch("/{insurance_id}", response_model=InsuranceRead)
async def verify_insurance(insurance_id: int, update_in: InsuranceUpdate, db: AsyncSession = Depends(get_db)):
    insurance = await crud_insurance.get_insurance_by_id(db, insurance_id)
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return await crud_insurance.update_insurance_verification(db, insurance, update_in)

@router.delete("/{insurance_id}")
async def delete_insurance(insurance_id: int, db: AsyncSession = Depends(get_db)):
    insurance = await crud_insurance.get_insurance_by_id(db, insurance_id)
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    await crud_insurance.delete_insurance(db, insurance)
    return {"detail": "Insurance deleted successfully"}
