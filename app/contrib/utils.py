from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from app.auth.models import Session, User
from app.auth.schemas import TokenSchema
from app.settings import SECRET_KEY, JWT_ALGORITHM, logger

UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)
FORBIDDEN_EXCEPTION = HTTPException(
    status_code=HTTP_403_FORBIDDEN,
    detail="You do not have permissions",
    headers={"WWW-Authenticate": "Bearer"},
)


class JWTAuth(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> User:
        token = await super().__call__(request)
        try:
            info = jwt.decode(token, SECRET_KEY, [JWT_ALGORITHM])
        except (jwt.PyJWTError, jwt.ExpiredSignatureError) as err:
            logger.warning(f'Error on decoding jwt token. Error: {err}')
            raise UNAUTHORIZED_EXCEPTION
        user = await User.get_or_none(pk=info.get('user_id', 0))
        if not user or not user.is_active:
            raise UNAUTHORIZED_EXCEPTION
        return user


jwt_auth = JWTAuth('/api/v1/auth/token')


def check_permissions(user: User, *permissions: str):
    for permission in permissions:
        if permission not in user.permissions:
            raise FORBIDDEN_EXCEPTION


async def get_jwt_token(user: User) -> TokenSchema:
    session = await Session.create(
        user=user,
        expired_at=datetime.utcnow() + timedelta(days=30)
    )
    access_token = jwt.encode(
        {
            'user_id': user.id,
            'permissions': user.permissions,
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        SECRET_KEY,
        JWT_ALGORITHM
    )
    return TokenSchema(refresh_token=f'{session.refresh_token}', access_token=access_token.decode())
