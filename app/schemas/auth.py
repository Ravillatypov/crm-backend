from pydantic import Field, BaseModel
from typing import List


class LoginSchema(BaseModel):
    phone: str
    password: str


class TokenSchema(BaseModel):
    id: int
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    permissions: List[str]


class UserSchema(TokenSchema):
    phone: str = Field(min_length=10, max_length=15)
    is_active: bool


class UserPostSchema(UserSchema):
    password: str = Field(min_length=6, max_length=50)
