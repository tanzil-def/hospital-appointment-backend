from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.db.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password  


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100, role: str = None, gender: str = None):
    query = select(User)
    if role:
        query = query.where(User.role == role)
    if gender:
        query = query.where(User.gender == gender)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def create_user(db: AsyncSession, user_in: UserCreate):
    db_user = User(
        full_name=user_in.full_name,
        email=user_in.email,
        phone=user_in.phone,
        password=hash_password(user_in.password),  
        role=user_in.role.value,
        gender=user_in.gender.value
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return None
    await db.delete(db_user)
    await db.commit()
    return True
