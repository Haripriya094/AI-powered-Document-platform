from pydantic import BaseModel


class user_login(BaseModel):
    username: str
    password: str


class user_logout(BaseModel):
    username: str