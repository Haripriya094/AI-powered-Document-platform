from fastapi import APIRouter
from backend.core.services import health
from backend.core.services import user_service
from backend.core.services.project_service import interview_router


router = APIRouter()

router.include_router(health.health_router)
router.include_router(user_service.user_router)
router.include_router(interview_router)
