from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import register_user, authenticate_user
from app.db.session import get_async_db  

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_async_db)):
    try:
        user = await register_user(db, user_in)
        return {"message": "User registered successfully", "user_id": user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_async_db)):
    auth = await authenticate_user(db, credentials.email, credentials.password)
    if not auth:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": auth["access_token"], "token_type": "bearer"}
