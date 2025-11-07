from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate

# ------------------------------
# GET single appointment
# ------------------------------
async def get_appointment(db: AsyncSession, appointment_id: int):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    return result.scalars().first()

# ------------------------------
# GET multiple appointments
# ------------------------------
async def get_appointments(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Appointment).offset(skip).limit(limit))
    return result.scalars().all()

# ------------------------------
# CREATE appointment
# ------------------------------
async def create_appointment(db: AsyncSession, appointment: AppointmentCreate):
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment

# ------------------------------
# UPDATE appointment (PUT / PATCH)
# ------------------------------
async def update_appointment(db: AsyncSession, appointment_id: int, appointment: AppointmentUpdate):
    db_appointment = await get_appointment(db, appointment_id)
    if not db_appointment:
        return None
    for field, value in appointment.dict(exclude_unset=True).items():
        setattr(db_appointment, field, value)
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment

# ------------------------------
# DELETE appointment
# ------------------------------
async def delete_appointment(db: AsyncSession, appointment_id: int):
    db_appointment = await get_appointment(db, appointment_id)
    if not db_appointment:
        return None
    await db.delete(db_appointment)
    await db.commit()
    return db_appointment
