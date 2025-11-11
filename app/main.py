from fastapi import FastAPI

# Routers
from app.api.auth_router import router as auth_router
from app.api.user_router import router as user_router
from app.api.admin_router import router as admin_router
from app.api.appointment_router import router as appointment_router
from app.api.doctor_profile_router import router as doctor_profile_router
from app.api.doctor_availability_router import router as availability_router
from app.api.notification_router import router as notification_router
from app.api.document_router import router as document_router
from app.api.insurance_router import router as insurance_router

app = FastAPI(
    title="Doctor Appointment Booking API",
    version="1.0.0",
    description="API for managing hospital appointments, doctors, availability, notifications, documents, insurance, and users."
)

# ----------------------
# Root endpoint
# ----------------------
@app.get("/")
async def root():
    return {"message": "Hospital Appointment Booking API is running 🚀"}

# ----------------------
# Include all routers
# ----------------------
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(appointment_router, prefix="/appointments", tags=["Appointments"])
app.include_router(doctor_profile_router, prefix="/doctors", tags=["Doctors"])
app.include_router(availability_router, prefix="/doctor-availability", tags=["Doctor Availability"])
app.include_router(notification_router, prefix="/notifications", tags=["Notifications"])
app.include_router(document_router, prefix="/documents", tags=["Documents"])
app.include_router(insurance_router, prefix="/insurance", tags=["Insurance"])
