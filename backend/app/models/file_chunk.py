import uuid
from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class FileChunk(Base):
    __tablename__ = "file_chunks"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    virtual_file_id = Column(
        String,
        ForeignKey("virtual_files.id"),
        nullable=False,
        index=True
    )

    owner_user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    provider = Column(
        String,
        nullable=False
    )

    provider_file_id = Column(
        String,
        nullable=False
    )

    offset_bytes = Column(
        BigInteger,
        nullable=False
    )

    size_bytes = Column(
        BigInteger,
        nullable=False
    )

    # relationships
    virtual_file = relationship(
        "VirtualFile",
        back_populates="chunks"
    )
