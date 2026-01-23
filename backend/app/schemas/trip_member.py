from pydantic import BaseModel


class TripMemberRead(BaseModel):
    id: str
    user_id: str
    role: str
    allocated_bytes: int
    used_bytes: int

    class Config:
        from_attributes = True
