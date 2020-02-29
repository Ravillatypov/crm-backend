from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from fastapi import APIRouter, Body, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from app.auth.models import User, Session
from app.auth.schemas import TokenSchema, LoginSchema
from app.contrib.schemas import MessageSchema
from app.settings import SECRET_KEY

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
        session = await Session.create(
            user=user,
            refresh_token=uuid4(),
            expired_at=datetime.utcnow() + timedelta(days=30)
        )
        access_token = jwt.encode(
            {
                'sub': {
                    'user_id': user.id,
                    'permissions': user.permissions
                },
                'exp': datetime.utcnow() + timedelta(hours=1)
            },
            SECRET_KEY
        )
        return {'access_token': access_token, 'refresh_token': f'{session.refresh_token}'}
    raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
