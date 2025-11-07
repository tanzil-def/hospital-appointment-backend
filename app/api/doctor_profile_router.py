from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.doctor_profile import DoctorProfileCreate, DoctorProfileUpdate, DoctorProfileOut
from app.crud.doctor_profile import (
    get_doctor_profile,
    get_doctor_profiles,
    create_doctor_profile,
    update_doctor_profile,
    delete_doctor_profile
)
from app.db.session import get_async_db
from app.core.security import require_role 

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/", response_model=DoctorProfileOut)
async def create_doctor_endpoint(
    profile: DoctorProfileCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(require_role("admin"))  
):
    return await create_doctor_profile(db, profile)


@router.get("/", response_model=List[DoctorProfileOut])
async def list_doctors(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db)
):
    return await get_doctor_profiles(db, skip=skip, limit=limit)


@router.get("/{doctor_id}", response_model=DoctorProfileOut)
async def get_doctor_endpoint(
    doctor_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    db_profile = await get_doctor_profile(db, doctor_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    return db_profile


@router.put("/{doctor_id}", response_model=DoctorProfileOut)
async def update_doctor_endpoint(
    doctor_id: int,
    profile: DoctorProfileUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(require_role("admin"))  
):
    db_profile = await update_doctor_profile(db, doctor_id, profile)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    return db_profile


@router.patch("/{doctor_id}", response_model=DoctorProfileOut)
async def patch_doctor_endpoint(
    doctor_id: int,
    profile: DoctorProfileUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(require_role("admin")) 
):
    db_profile = await update_doctor_profile(db, doctor_id, profile)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    return db_profile


@router.delete("/{doctor_id}", response_model=DoctorProfileOut)
async def delete_doctor_endpoint(
    doctor_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(require_role("admin")) 
):
    db_profile = await delete_doctor_profile(db, doctor_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Doctor profile not found")
    return db_profile

