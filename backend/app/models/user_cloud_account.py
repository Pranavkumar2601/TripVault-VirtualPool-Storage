import uuid
from sqlalchemy import Column, String, ForeignKey
from app.models.base import Base


class UserCloudAccount(Base):
    __tablename__ = "user_cloud_accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    provider = Column(String, nullable=False)  # "google_drive"

    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    token_expiry = Column(String, nullable=True)
