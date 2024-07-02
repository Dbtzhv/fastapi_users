from typing import Optional

from sqlalchemy.orm import Session

from app.dao.base import BaseDAO
from app.models.user import User
from app.security import verify_password


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def authenticate_user(
        cls, db: Session, email: str, password: str
    ) -> Optional[User]:
        user = await cls.find_one_or_none(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def is_super_user(user: User) -> bool:
        return user.is_superuser

    @staticmethod
    async def is_subscribed(user: User) -> bool:
        return user.is_subscribed
