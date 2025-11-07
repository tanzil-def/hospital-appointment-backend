from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.doctor_availability import DoctorAvailabilityCreate, DoctorAvailabilityUpdate, DoctorAvailabilityOut
from app.crud.doctor_availability import (
    get_availability,
    get_availabilities,
    create_availability,
    update_availability,
    delete_availability
)
from app.db.session import get_async_db

router = APIRouter(prefix="/doctor-availability", tags=["DoctorAvailability"])

@router.post("/", response_model=DoctorAvailabilityOut)
async def create_availability_endpoint(availability: DoctorAvailabilityCreate, db: AsyncSession = Depends(get_async_db)):
    return await create_availability(db, availability)

@router.get("/", response_model=List[DoctorAvailabilityOut])
async def list_availabilities(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)):
    return await get_availabilities(db, skip=skip, limit=limit)

@router.get("/{availability_id}", response_model=DoctorAvailabilityOut)
async def get_availability_endpoint(availability_id: int, db: AsyncSession = Depends(get_async_db)):
    db_availability = await get_availability(db, availability_id)
    if not db_availability:
        raise HTTPException(status_code=404, detail="Doctor availability not found")
    return db_availability

@router.put("/{availability_id}", response_model=DoctorAvailabilityOut)
async def update_availability_endpoint(availability_id: int, availability: DoctorAvailabilityUpdate, db: AsyncSession = Depends(get_async_db)):
    db_availability = await update_availability(db, availability_id, availability)
    if not db_availability:
        raise HTTPException(status_code=404, detail="Doctor availability not found")
    return db_availability

@router.patch("/{availability_id}", response_model=DoctorAvailabilityOut)
async def patch_availability_endpoint(availability_id: int, availability: DoctorAvailabilityUpdate, db: AsyncSession = Depends(get_async_db)):
    db_availability = await update_availability(db, availability_id, availability)
    if not db_availability:
        raise HTTPException(status_code=404, detail="Doctor availability not found")
    return db_availability

@router.delete("/{availability_id}", response_model=DoctorAvailabilityOut)
async def delete_availability_endpoint(availability_id: int, db: AsyncSession = Depends(get_async_db)):
    db_availability = await delete_availability(db, availability_id)
    if not db_availability:
        raise HTTPException(status_code=404, detail="Doctor availability not found")
    return db_availability
