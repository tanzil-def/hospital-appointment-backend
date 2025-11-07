from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate

async def get_notification(db: AsyncSession, notification_id: int):
    result = await db.execute(select(Notification).where(Notification.id == notification_id))
    return result.scalars().first()

async def get_notifications(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Notification).offset(skip).limit(limit))
    return result.scalars().all()

async def create_notification(db: AsyncSession, notification: NotificationCreate):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification

async def update_notification(db: AsyncSession, notification_id: int, notification: NotificationUpdate):
    db_notification = await get_notification(db, notification_id)
    if not db_notification:
        return None
    for field, value in notification.dict(exclude_unset=True).items():
        setattr(db_notification, field, value)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification

async def delete_notification(db: AsyncSession, notification_id: int):
    db_notification = await get_notification(db, notification_id)
    if not db_notification:
        return None
    await db.delete(db_notification)
    await db.commit()
    return db_notification
