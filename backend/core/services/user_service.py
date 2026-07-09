from fastapi import APIRouter
from backend.constants.app_constants import APIS
from backend.core.handlers.user_handler import userManagement
from backend.core.schemas import schemas
from backend.utills.logger_utill import logger
user_router = APIRouter()
user_handler=userManagement()

@user_router.post(APIS.login, tags=["user_management"])
def login(input_data: schemas.user_login):
    final_json = {"status": "failed", "message": "failed to login"}
    try:
        if input_data:
            res = user_handler.login(input_data)
            if res == "user not found":
                final_json["message"] = "user not found try to register first"
                final_json["status"] = "failed"
            else:
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
            print(input_data)
            res = user_handler.create_user_account(input_data)
            print(res)
            if res:
                final_json = {"status": "success", "message": "registration success"}
                return final_json
            return final_json
    except Exception as error:
        logger.exception(f"register failed : {error}")
        return final_json