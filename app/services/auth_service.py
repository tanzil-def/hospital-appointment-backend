from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

# ✅ Register User
async def register_user(db: AsyncSession, user_in: UserCreate):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("Email already registered")
    user_in.password = hash_password(user_in.password)
    new_user = await create_user(db, user_in)
    return new_user

# ✅ Authenticate User
async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user
