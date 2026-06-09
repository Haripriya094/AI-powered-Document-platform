from fastapi import APIRouter

from backend.constants.app_constants import APIS

health_router = APIRouter()


@health_router.get(APIS.health)
def health_check():
    return {"status": "UP"}