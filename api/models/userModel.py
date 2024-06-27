from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserModel(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

class UserCollection(BaseModel):
    users: List[UserModel]