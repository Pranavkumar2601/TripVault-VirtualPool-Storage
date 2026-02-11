from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
import uuid


class UserCloudAccount(Base):
    __tablename__ = "user_cloud_accounts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)

    provider = Column(String, nullable=False)

    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)

    token_uri = Column(String, nullable=True)
    client_id = Column(String, nullable=True)
    client_secret = Column(String, nullable=True)

    token_expiry = Column(String, nullable=True)
