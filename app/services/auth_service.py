from sqlalchemy.orm import Session
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

def register_user(db: Session, user_in: UserCreate):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("Email already registered")
    user_in.password = hash_password(user_in.password)
    return create_user(db, user_in)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    token_data = {"user_id": user.id, "role": user.role.value}
    access_token = create_access_token(token_data)
    return {"user": user, "access_token": access_token}
