from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.dao.user import UserDAO
from app.database import db_dependency
from app.log import get_logger
from app.tasks.tasks import send_registration_email
from app.schemas.auth import Token, UserRegister
from app.security import (
    add_refresh_token_cookie,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    refresh_token_state,
)

auth_router = APIRouter()

log = get_logger(__name__)


@auth_router.post("/register", response_model=str)
async def register(data: UserRegister, db: db_dependency):
    user = await UserDAO.find_one_or_none(db=db, email=data.email)
    if user:
        log.info(f"register: User with email {data.email} already exists")
        raise HTTPException(status_code=400, detail="Email has already registered")

    if data.password != data.confirm_password:
        log.info("register: Passwords do not match")
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # hashing password
    password = data.password
    user_data = data.dict(exclude={"confirm_password", "password"})
    user_data["hashed_password"] = get_password_hash(password)

    # save user to db
    user = await UserDAO.add(db=db, **user_data)

    log.info("register: User has been registered")

    send_registration_email.delay(user_data["email"])
    log.info("register: email has been sent")

    return "User has been registered"


@auth_router.post("/login", response_model=Token)
async def login_for_access_token(
    db: db_dependency,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = await UserDAO.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        log.info("login: Incorrect email or password")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}, expires_delta=refresh_token_expires
    )

    add_refresh_token_cookie(response=response, token=refresh_token)

    log.info("login: tokens have been sent")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth_router.post("/refresh")
async def refresh_token(refresh: Annotated[str | None, Cookie()] = None):
    if not refresh:
        log.info("refresh: refresh token required")
        raise HTTPException(status_code=400, detail="refresh token required")
    log.info("refresh: token has been sent")
    return refresh_token_state(token=refresh)



