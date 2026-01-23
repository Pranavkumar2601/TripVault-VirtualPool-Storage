import uuid
from sqlalchemy import Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship


from app.models.base import Base


class TripMember(Base):
    __tablename__ = "trip_members"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    trip_id = Column(
        String,
        ForeignKey("trips.id"),
        nullable=False
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    role = Column(
        String,
        nullable=False,  # ADMIN / MEMBER
        default="MEMBER"
    )

    allocated_bytes = Column(
        BigInteger,
        nullable=False,
        default=0
    )

    used_bytes = Column(
        BigInteger,
        nullable=False,
        default=0
    )

    # relationships
    trip = relationship("Trip", back_populates="members")
    user = relationship("User")
