from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.api.dependencies import get_current_superuser, get_current_user
from app.dao.user import UserDAO
from app.database import db_dependency
from app.log import get_logger
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, UserUpdatePassword
from app.security import get_password_hash, verify_password

user_router = APIRouter()

log = get_logger(__name__)


@user_router.get("/all", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def fetch_all_users(
    user: Annotated[User, Depends(get_current_user)], db: db_dependency
):
    users = await UserDAO.find_all(db)
    log.info("fetch_all_users: users have been received")
    return users


@user_router.patch(
    "/change_password", response_model=str, status_code=status.HTTP_200_OK
)
async def update_user_password(
    db: db_dependency,
    user_request: UserUpdatePassword,
    user: User = Depends(get_current_user),
):
    if user_request.new_password == user_request.password:
        log.info("change_password: new password cannot be the same as old password")
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as old password"
        )
    if not verify_password(user_request.password, user.hashed_password):
        log.info("change_password: incorrect old password")
        raise HTTPException(status_code=400, detail="Incorrect password")
    model = user_request.model_dump()
    model.pop("password")
    model["hashed_password"] = get_password_hash(model.pop("new_password"))
    user = await UserDAO.update(db, user.id, **model)
    log.info("change_password: password has been changed")
    return user


@user_router.get(
    "/current_user", response_model=UserOut, status_code=status.HTTP_200_OK
)
async def get_current_user(
    user: Annotated[User, Depends(get_current_user)],
):
    log.info("current_user: user has been received")
    return user


@user_router.get(
    "/{user_id}", response_model=Optional[UserOut], status_code=status.HTTP_200_OK
)
async def fetch_user_by_id(
    user: Annotated[User, Depends(get_current_superuser)],
    db: db_dependency,
    user_id: int = Path(..., gt=0),
):
    user = await UserDAO.find_by_id(db, user_id)
    if not user:
        log.info("fetch_user_by_id: user not found")
        raise HTTPException(status_code=404, detail="User not found")
    log.info("fetch_user_by_id: user has been received")
    return user


@user_router.patch(
    "/{user_id}", response_model=str, status_code=status.HTTP_201_CREATED
)
async def update_user(
    db: db_dependency,
    user: Annotated[User, Depends(get_current_superuser)],
    user_request: UserUpdate,
    user_id: int = Path(..., gt=0),
):
    user = await UserDAO.update(
        db, user_id, **user_request.model_dump(exclude_unset=True)
    )
    log.info("update_user: user has been updated")
    return user
