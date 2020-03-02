from typing import List

from pydantic import Field, BaseModel, UUID4


class LoginSchema(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    id: int
    permissions: List[str]
    first_name: str = Field('', min_length=2, max_length=50)
    last_name: str = Field('', min_length=2, max_length=50)
    login: str = Field('', min_length=10, max_length=20)
    is_active: bool


class UserPostSchema(UserSchema):
    password: str = Field('', min_length=6, max_length=50)


class TokenSchema(BaseModel):
    refresh_token: str
    access_token: str


class JWTSchema(BaseModel):
    user_id: int
    permissions: List[str]


class RefreshSchema(BaseModel):
    refresh_token: UUID4
