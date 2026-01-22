from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    name: str


class UserRead(BaseModel):
    id: str
    email: EmailStr
    name: str

    class Config:
        from_attributes = True
