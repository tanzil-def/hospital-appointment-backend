from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationOut
from app.crud.notification import (
    get_notification,
    get_notifications,
    create_notification,
    update_notification,
    delete_notification
)
from app.db.session import get_db  # ✅ updated

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", response_model=NotificationOut)
async def create_notification_endpoint(notification: NotificationCreate, db: AsyncSession = Depends(get_db)):
    return await create_notification(db, notification)

@router.get("/", response_model=List[NotificationOut])
async def list_notifications(skip: int = 1, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_notifications(db, skip=skip, limit=limit)

@router.get("/{notification_id}", response_model=NotificationOut)
async def get_notification_endpoint(notification_id: int, db: AsyncSession = Depends(get_db)):
    db_notification = await get_notification(db, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@router.patch("/{notification_id}", response_model=NotificationOut)
async def patch_notification_endpoint(notification_id: int, notification: NotificationUpdate, db: AsyncSession = Depends(get_db)):
    db_notification = await update_notification(db, notification_id, notification)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@router.delete("/{notification_id}", response_model=NotificationOut)
async def delete_notification_endpoint(notification_id: int, db: AsyncSession = Depends(get_db)):
    db_notification = await delete_notification(db, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification
