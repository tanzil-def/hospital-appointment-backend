from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.notification import Notification   # ✅ Corrected import
from app.schemas.notification import NotificationCreate, NotificationUpdate


# ✅ Create Notification
async def create_notification(db: AsyncSession, notification_in: NotificationCreate):
    new_notification = Notification(**notification_in.dict())
    db.add(new_notification)
    await db.commit()
    await db.refresh(new_notification)
    return new_notification


# ✅ Get single Notification by ID
async def get_notification(db: AsyncSession, notification_id: int):
    result = await db.execute(select(Notification).where(Notification.id == notification_id))
    return result.scalar_one_or_none()


# ✅ Get all Notifications
async def get_notifications(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Notification).offset(skip).limit(limit))
    return result.scalars().all()


# ✅ Update Notification
async def update_notification(db: AsyncSession, notification_id: int, notification_in: NotificationUpdate):
    notification = await get_notification(db, notification_id)
    if not notification:
        return None
    update_data = notification_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(notification, field, value)
    await db.commit()
    await db.refresh(notification)
    return notification


# ✅ Delete Notification
async def delete_notification(db: AsyncSession, notification_id: int):
    notification = await get_notification(db, notification_id)
    if not notification:
        return None
    await db.delete(notification)
    await db.commit()
    return notification
