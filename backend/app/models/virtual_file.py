import uuid
from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


class VirtualFile(Base):
    __tablename__ = "virtual_files"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    trip_id = Column(
        String,
        ForeignKey("trips.id"),
        nullable=False,
        index=True
    )

    path = Column(
        String,
        nullable=False
    )

    size_bytes = Column(
        BigInteger,
        nullable=False
    )

    checksum = Column(
        String,
        nullable=True
    )

    uploaded_by = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # relationships
    chunks = relationship(
        "FileChunk",
        back_populates="virtual_file",
        cascade="all, delete-orphan"
    )
