from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.config import settings
from app.dao.user import UserDAO
from app.database import db_dependency
from app.models.user import User
from app.schemas.auth import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from e
    return token_data


async def get_current_user(
    db: db_dependency, token: TokenPayload = Depends(get_token)
) -> User:
    user = await UserDAO.find_one_or_none(db, id=token.sub)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not await UserDAO.is_super_user(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges",
        )
    return current_user


async def get_current_subscribed_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not await UserDAO.is_subscribed(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have subscription",
        )
    return current_user
