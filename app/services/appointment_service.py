from app.schemas.notification import NotificationCreate
from app.crud.notification import create_notification

async def send_appointment_notifications(db, appointment):
    
    email_message = f"Your appointment with Dr.{appointment.doctor_id} is confirmed at {appointment.start_time}"
    await create_notification(db, NotificationCreate(
        user_id=appointment.patient_id,
        appointment_id=appointment.id,
        type="email",
        message=email_message
    ))

    
    await create_notification(db, NotificationCreate(
        user_id=appointment.patient_id,
        appointment_id=appointment.id,
        type="sms",
        message=email_message
    ))
