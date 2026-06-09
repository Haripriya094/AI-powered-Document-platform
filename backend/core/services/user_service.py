from fastapi import APIRouter
from backend.constants.app_constants import APIS
from backend.core.handlers.user_handler import userManagement
from backend.core.schemas import schemas
user_router = APIRouter()
user_handler=userManagement()

@user_router.post(APIS.login,tags=["user_management"])
def login(input_data:schemas.user_login):
    final_json={"status":"failed","message":"failed to login"}
    try:
        if input_data:
            res=user_handler.login(input_data)
            if res:
                final_json={"status":"success","message":"login success"}
                return final_json
            return final_json

    except Exception as error:
        print(error)
        return final_json