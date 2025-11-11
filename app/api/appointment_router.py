from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentOut
from app.crud.appointment import (
    get_appointment,
    get_appointments,
    create_appointment,
    update_appointment,
    delete_appointment
)
from app.db.session import get_db  # ✅ updated

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentOut)
async def create_appointment_endpoint(appointment: AppointmentCreate, db: AsyncSession = Depends(get_db)):
    return await create_appointment(db, appointment)

@router.get("/", response_model=List[AppointmentOut])
async def list_appointments(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_appointments(db, skip=skip, limit=limit)

@router.get("/{appointment_id}", response_model=AppointmentOut)
async def get_appointment_endpoint(appointment_id: int, db: AsyncSession = Depends(get_db)):
    db_appointment = await get_appointment(db, appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@router.put("/{appointment_id}", response_model=AppointmentOut)
async def update_appointment_endpoint(appointment_id: int, appointment: AppointmentUpdate, db: AsyncSession = Depends(get_db)):
    db_appointment = await update_appointment(db, appointment_id, appointment)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@router.patch("/{appointment_id}", response_model=AppointmentOut)
async def patch_appointment_endpoint(appointment_id: int, appointment: AppointmentUpdate, db: AsyncSession = Depends(get_db)):
    db_appointment = await update_appointment(db, appointment_id, appointment)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@router.delete("/{appointment_id}", response_model=AppointmentOut)
async def delete_appointment_endpoint(appointment_id: int, db: AsyncSession = Depends(get_db)):
    db_appointment = await delete_appointment(db, appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment
