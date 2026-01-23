import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name = Column(String, nullable=False)

    created_by = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    # relationships
    creator = relationship("User")
    members = relationship("TripMember", back_populates="trip")
