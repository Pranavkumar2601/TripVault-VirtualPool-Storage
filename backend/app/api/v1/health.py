from fastapi import APIRouter
import logging

router = APIRouter()
logger = logging.getLogger("app")


@router.get("/health")
def health():
    logger.info("v1 health check called")
    return {"status": "ok"}
