from datetime import datetime

from fastapi import APIRouter, Body, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from app.auth.models import User, Session
from app.auth.schemas import TokenSchema, LoginSchema, RefreshSchema
from app.contrib.schemas import MessageSchema, StatusSchema
from app.contrib.utils import get_jwt_token

v1 = APIRouter()


@v1.post(
    '/login',
    response_model=TokenSchema,
    name='Login',
    status_code=200,
    tags=['auth'],
    responses={'401': {'model': MessageSchema}}
)
async def login(data: LoginSchema = Body(...,)):
    user = await User.get_or_none(login=data.login.strip().lower(), is_active=True)
    if user and user.verify(data.password):
        return await get_jwt_token(user)
    raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@v1.post(
    '/refresh',
    name='Refresh access token',
    tags=['auth'],
    response_model=TokenSchema,
    responses={'401': {'model': MessageSchema}}
)
async def refresh(token: RefreshSchema = Body(None)):
    session = await Session.get_or_none(refresh_token=token.refresh_token, expired_at__lt=datetime.utcnow())

    if not session:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect refresh token or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await get_jwt_token(session.user)


@v1.post(
    '/revoke',
    name='Revoke refresh token',
    tags=['auth'],
    response_model=StatusSchema
)
async def revoke(token: RefreshSchema = Body(None)):
    await Session.filter(refresh_token=token.refresh_token).delete()
    return {'status': 'success'}
