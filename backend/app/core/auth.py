from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User


def get_current_user(
        reuest:Request,
        db:Session = Depends(get_db),

)-> User:
     """
     Temproray auth resolver,
     From now reads user_id from header set after Oauth
     Later will be replaced  with JWT/session

    
     """

     user_id = request.headers.get("X-User-ID")
     if not user_id:
          raise HTTPException(status_code= 401, detail = "Not authenticated")
     
     user = db.get(User, user_id)
     if not user:
          raise HTTPException(staus_code=401, detail = "Invalid User")
     return user