import uuid
from sqlalchemy import Column, String
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    name = Column(
        String,
        nullable=False
    )
