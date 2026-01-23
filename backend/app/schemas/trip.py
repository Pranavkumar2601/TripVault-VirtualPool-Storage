from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import List     
from app.schemas.trip_member import TripMemberRead

class TripCreate(BaseModel):
    name: str
    


class TripRead(BaseModel):
    id: str
    name: str
    created_by: str
    members:List[TripMemberRead] = []


    
    class Config:
        from_attributes = True
