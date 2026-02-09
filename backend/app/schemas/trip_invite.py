from pydantic import BaseModel


class TripInviteRequest(BaseModel):
    user_id: str

