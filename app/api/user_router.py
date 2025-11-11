from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.crud.user import (
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)
from app.db.session import get_db
from app.schemas.user import UserRead, UserUpdate
from app.core.security import get_current_user, require_role

router = APIRouter(tags=["Users"])


@router.get("/me", response_model=UserRead)
async def read_current_user(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    db_user = await get_user_by_id(db, current_user["user_id"])
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=List[UserRead])
async def read_all_users(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = Query(None, description="Filter by role: patient/doctor/admin"),
    gender: Optional[str] = Query(None, description="Filter by gender: male/female/others"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("admin"))
):
    users = await get_all_users(db, skip=skip, limit=limit, role=role, gender=gender)
    return users



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("admin"))
):
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None
