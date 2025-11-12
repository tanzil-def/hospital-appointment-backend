from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.doctor_profile import (
    get_doctor_profile,
    get_doctor_profiles,
    create_doctor_profile,
    update_doctor_profile,
    delete_doctor_profile
)
from app.schemas.doctor_profile import DoctorProfileOut
import os
import shutil

router = APIRouter(tags=["Doctors"])

@router.post("/", response_model=DoctorProfileOut)
async def create_doctor_form(
    name: str = Form(...),
    specialization: str = Form(...),
    degree: Optional[str] = Form(None),
    about: Optional[str] = Form(None),
    consultation_fee: Optional[float] = Form(0.0),
    languages: Optional[str] = Form(None),
    user_id: int = Form(...),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    profile_data = {
        "name": name,
        "specialization": specialization,
        "degree": degree,
        "about": about,
        "consultation_fee": consultation_fee,
        "languages": languages,
        "user_id": user_id
    }

    if file:
        file_path = f"static/doctors/{user_id}_{file.filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        profile_data["photo_url"] = file_path

    doctor = await create_doctor_profile(db, profile_data)
    return doctor

@router.get("/", response_model=List[DoctorProfileOut])
async def list_doctors(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_doctor_profiles(db, skip, limit)

@router.get("/{doctor_id}", response_model=DoctorProfileOut)
async def get_doctor_endpoint(doctor_id: int, db: AsyncSession = Depends(get_db)):
    doctor = await get_doctor_profile(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.put("/{doctor_id}", response_model=DoctorProfileOut)
async def update_doctor_form(
    doctor_id: int,
    name: Optional[str] = Form(None),
    specialization: Optional[str] = Form(None),
    degree: Optional[str] = Form(None),
    about: Optional[str] = Form(None),
    consultation_fee: Optional[float] = Form(None),
    languages: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    profile_data = {k: v for k, v in {
        "name": name,
        "specialization": specialization,
        "degree": degree,
        "about": about,
        "consultation_fee": consultation_fee,
        "languages": languages
    }.items() if v is not None}

    if file:
        file_path = f"static/doctors/{doctor_id}_{file.filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        profile_data["photo_url"] = file_path

    doctor = await update_doctor_profile(db, doctor_id, profile_data)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.delete("/{doctor_id}", response_model=DoctorProfileOut)
async def delete_doctor_endpoint(doctor_id: int, db: AsyncSession = Depends(get_db)):
    doctor = await delete_doctor_profile(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
