from pydantic import BaseModel
from datetime import datetime


class user_login(BaseModel):
    username: str
    password: str


class user_logout(BaseModel):
    username: str


class user_register(BaseModel):
    username: str
    password: str
    email: str

class userInfo(BaseModel):
    user_id: str
    username: str
    password: str
    email: str
    last_login:datetime
