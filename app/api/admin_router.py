from fastapi import APIRouter, Depends
from app.core.security import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
async def admin_dashboard(user: dict = Depends(require_role("admin"))):
    return {"message": f"Welcome Admin {user['user_id']}"}

