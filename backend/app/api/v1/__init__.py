from fastapi import APIRouter
from app.api.v1 import health, users, trips, files
# from app.api.v1.trips import router as trips_router



router = APIRouter()
router.include_router(health.router)
router.include_router(users.router)
router.include_router(trips.router)
router.include_router(files.router)
