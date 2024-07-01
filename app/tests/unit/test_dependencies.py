from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_superuser, get_current_user, get_token
from app.models.user import User
from app.schemas.auth import TokenPayload


@pytest.mark.parametrize(
    "token",
    [
        "invalid_token",
        "valid_token",
    ],
)
async def test_get_token_valid_token(token):
    if token == "invalid_token":
        with pytest.raises(HTTPException) as excinfo:
            await get_token(token)
        assert excinfo.value.status_code == status.HTTP_403_FORBIDDEN
    else:
        expected_payload = TokenPayload(sub="1234567890", username="john_doe")

        with patch(
            "jose.jwt.decode",
            return_value={"sub": "1234567890", "username": "john_doe"},
        ):
            result = await get_token(token)

        assert result == expected_payload


@pytest.mark.parametrize("exists", [True, False])
async def test_get_current_user_user_exists(exists, mocker):
    db_mock = mocker.Mock(spec=Session)
    token_mock = AsyncMock()
    token_mock.sub = 1

    if exists:
        user_mock = AsyncMock(spec=User)
        mocker.patch("app.dao.user.UserDAO.find_one_or_none", return_value=user_mock)

        result = await get_current_user(db=db_mock, token=token_mock)

        assert result == user_mock

    else:
        mocker.patch("app.dao.user.UserDAO.find_one_or_none", return_value=None)
        with pytest.raises(HTTPException):
            await get_current_user(db=db_mock, token=token_mock)


@pytest.mark.parametrize("superuser", [True, False])
async def test_get_current_user_user_exists(superuser):
    if superuser:
        current_user = User(is_superuser=True)
        result = await get_current_superuser(current_user)
        assert result == current_user

    else:
        current_user = User(is_superuser=False)
        with pytest.raises(HTTPException):
            await get_current_superuser(current_user)
