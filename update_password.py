import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from app.db.models.user import User  # tomer project er path check koro

DATABASE_URL = "postgresql+asyncpg://hospital:1234@localhost:5432/hospital_appointment"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def update_user_password(email: str, new_password: str):
    async with AsyncSessionLocal() as db:
        result = await db.execute(User.__table__.select().where(User.email == email))
        user_row = result.first()
        if not user_row:
            print("User not found")
            return

        hashed_password = pwd_context.hash(new_password)

        await db.execute(
            User.__table__.update()
            .where(User.id == user_row.id)
            .values(password=hashed_password)
        )
        await db.commit()
        print("Password updated successfully!")

if __name__ == "__main__":
    asyncio.run(update_user_password("tanzil@gmail.com", "1234"))
