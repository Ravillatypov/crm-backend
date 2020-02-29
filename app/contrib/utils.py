from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from app.auth.models import Session, User
from app.auth.schemas import TokenSchema
from app.settings import SECRET_KEY, JWT_ALGORITHM, logger


def check_permissions(authorization: str, *permissions: str):
    method, token = authorization.split(' ', 1)
    try:
        info = jwt.decode(token, SECRET_KEY, [JWT_ALGORITHM])
    except (jwt.PyJWTError, jwt.ExpiredSignatureError) as err:
        logger.warning(f'Error on decoding jwt token. Error: {err}')
        raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Incorrect JWT",
                headers={"WWW-Authenticate": "Bearer"},
            )

    for permission in permissions:
        if permission not in info.get('permissions', []):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="You do not have permissions",
                headers={"WWW-Authenticate": "Bearer"},
            )


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
