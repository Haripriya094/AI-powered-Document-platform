from fastapi import APIRouter
from backend.core.services import health
from backend.core.services import user_service

router = APIRouter()

router.include_router(health.health_router)
router.include_router(user_service.user_router)