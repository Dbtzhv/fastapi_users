from datetime import timedelta, datetime, timezone

from fastapi import Response, HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings
from app.log import get_logger

log = get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    log.info(f"getting password hash...")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    log.info(f"verifying password...")
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    log.info(f"access token has been created")
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    log.info(f"refresh token has been created")
    return encoded_jwt


def add_refresh_token_cookie(response: Response, token: str):
    exp = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    exp.replace(tzinfo=timezone.utc)
    log.info(f"refresh token cookie has been set")

    response.set_cookie(
        key="refresh",
        value=token,
        expires=int(exp.timestamp()),
        httponly=True,
    )


def refresh_token_state(token: str):
    try:
        payload = jwt.decode(
            token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError as ex:
        log.exception(ex)
        raise HTTPException(status_code=400, detail="Token error")
    log.info(f"refreshing access token...")

    return {"token": create_access_token(data=payload)}
