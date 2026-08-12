from backend.core.db.mongo import user_collection
from backend.utills.logger_utill import logger
from backend.core.schemas.schemas import userInfo, TokenResponse
from backend.utils.security.password_util import hash_password, verify_password
from backend.utils.security.jwt_util import create_access_token, create_refresh_token
from datetime import datetime
import json


class userManagement:
    def __init__(self):
        self.user_collection = user_collection.UserCollection()

    def login(self, input_data):
        final_json = {"status": "failed", "message": "login failed", "data": {}}
        try:
            name = input_data.username
            logger.info("Logging in...")
            existing_user = self.user_collection.find_one({"username": name})
            logger.info(f"Existing User: {existing_user}")
            if not existing_user:
                return "user not found"
            if not verify_password(input_data.password, existing_user.get("password", "")):
                return "invalid credentials"
            self.user_collection.update_one(
                {"username": name},
                {"last_login": datetime.now().isoformat()}
            )
            user_id = existing_user.get("user_id")
            token_response = TokenResponse(
                access_token=create_access_token(user_id),
                refresh_token=create_refresh_token(user_id),
            )
            final_json["status"] = "success"
            final_json["message"] = "login success"
            final_json["data"] = token_response.model_dump()
        except Exception:
            logger.exception("Failed to log in")
        return final_json

    def create_user_account(self, input_data):
        try:
            logger.info("user auto create for sso")
            if get_user_id := list(
                    user_collection.UserCollection().find({}, sort=[("user_id", 1)])):
                last_user_id = get_user_id[-1].get("user_id", None)
                new_user_id = "user_" + str(int(last_user_id.split("_")[-1]) + 1)
            else:
                new_user_id = "user_100"

            res = userInfo(
                user_id=new_user_id,
                username=input_data.username,
                email=input_data.email,
                password=hash_password(input_data.password),
                last_login=datetime.now(),
            )
            res_json = json.loads(res.model_dump_json())
            self.user_collection.insert_one(res_json)
            return res_json
        except Exception as e:
            logger.error(f"Failed to create user::{input_data.username}")
            return f"Failed to create user. Please try again::{str(e)}"
