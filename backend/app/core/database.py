from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


Database_url = "sqlite:///./tripvault.db"


engine = create_engine(Database_url,connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# This ensures: One session per request ,No leaks ,Thread-safe behavior
def get_db():
    db = SessionLocal()
    try:
        yield db              
    finally:
        db.close()