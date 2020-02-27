from fastapi import APIRouter, Body
from app.schemas.auth import TokenSchema, UserSchema, UserPostSchema, LoginSchema

auth = APIRouter()


@auth.post('/login', response_model=TokenSchema, name='', status_code=201, tags=['auth'])
async def login(data: LoginSchema = Body(...,)):
    return TokenSchema()
