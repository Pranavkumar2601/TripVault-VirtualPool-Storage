from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User


def get_current_user(
    request: Request,                # ✅ MUST be here
    db: Session = Depends(get_db),
) -> User:
    user_id = request.headers.get("X-User-Id")  # ✅ correct header

    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = user_id.strip()

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    return user
