from pydantic import BaseModel
from typing import List,Optional


class UserModel(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: Optional[str]


class ResponseListUser(BaseModel):
    code: str
    message: str
    data: Optional[List[UserModel]]


class ResponseUser(BaseModel):
    code: str
    message: str
    data: Optional[UserModel]


class CreateUserModel(BaseModel):
    username: str
    email: str
    password: str