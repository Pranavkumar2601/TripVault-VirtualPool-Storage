from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import router as v1_router
# from app.api.v1.trips import router as trips_router
from app.core import database
from app import models
from app.models.base import Base
import logging

setup_logging()
logger = logging.getLogger("app")

app = FastAPI(title=settings.APP_NAME)




@app.on_event("startup")
def on_startup():
    logger.info("TripVault application started")


app.include_router(v1_router, prefix="/api/v1")
# app.include_router(trips_router)


Base.metadata.create_all(bind=database.engine)