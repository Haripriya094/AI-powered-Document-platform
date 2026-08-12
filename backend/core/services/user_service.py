from fastapi import APIRouter, Depends, HTTPException
from backend.constants.app_constants import APIS
from backend.core.handlers.user_handler import userManagement
from backend.core.schemas import schemas
from backend.core.dependencies.auth import get_current_user
from backend.utils.security.jwt_util import decode_token, create_access_token, create_refresh_token
from backend.utills.logger_utill import logger

user_router = APIRouter()
user_handler = userManagement()


@user_router.post(APIS.login, tags=["user_management"])
def login(input_data: schemas.user_login):
    final_json = {"status": "failed", "message": "failed to login"}
    try:
        if input_data:
            res = user_handler.login(input_data)
            if res == "user not found":
                final_json["message"] = "user not found, try to register first"
                return final_json
            if res == "invalid credentials":
                final_json["message"] = "invalid username or password"
                return final_json
            final_json = res
            return final_json
    except Exception as error:
        logger.exception(f"login failed: {error}")
        return final_json


@user_router.post(APIS.logout, tags=["user_management"])
def logout(input_data: schemas.user_logout):
    final_json = {"status": "failed", "message": "logout failed"}
    try:
        if input_data:
            final_json = {"status": "success", "message": "logout success"}
            return final_json
    except Exception as error:
        logger.exception(f"logout failed: {error}")
        return final_json


@user_router.post(APIS.register, tags=["user_management"])
def register(input_data: schemas.user_register):
    final_json = {"status": "failed", "message": "registration failed"}
    try:
        if input_data:
            res = user_handler.create_user_account(input_data)
            if res:
                final_json = {"status": "success", "message": "registration success"}
                return final_json
            return final_json
    except Exception as error:
        logger.exception(f"register failed: {error}")
        return final_json


@user_router.post(APIS.refresh, tags=["user_management"], response_model=schemas.TokenResponse)
def refresh_token(body: schemas.RefreshTokenRequest):
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
        return schemas.TokenResponse(
            access_token=create_access_token(user_id),
            refresh_token=create_refresh_token(user_id),
        )
    except HTTPException:
        raise
    except Exception as error:
        logger.exception(f"token refresh failed: {error}")
        raise HTTPException(status_code=500, detail="Token refresh failed")


@user_router.get("/me", tags=["user_management"])
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {"status": "success", "data": {"user_id": current_user.get("sub")}}
