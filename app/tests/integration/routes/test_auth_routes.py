from unittest.mock import patch

import pytest
from httpx import AsyncClient
from jose import jwt


@pytest.mark.parametrize(
    "email,password,confirm_password,status_code",
    [
        ("test@etest.com", "password", "password", 200),
        ("bad@bad.com", "password", "password1", 400),
    ],
)
async def test_register_user(
    email, password, confirm_password, status_code, ac: AsyncClient
):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,successful",
    [
        ("admin@admin.com", "password", True),
        ("bad@bad.com", "password", False),
    ],
)
async def test_login_for_access_token(email, password, successful, ac: AsyncClient):
    response = await ac.post(
        "/auth/login", data={"username": email, "password": password}
    )
    data = response.json()
    if successful is False:
        assert "detail" in data
    else:
        assert (
            "access_token" in data
            and data["token_type"] == "bearer"
            and response.status_code == 200
        )


async def test_refresh_token(ac: AsyncClient):
    with patch("app.security.create_access_token", return_value="new_access_token") as mock_create_access_token:
        with patch("jose.jwt.decode", return_value={"sub": "user_id"}):
            cookies = {"refresh": "valid_refresh_token"}

            response = await ac.post("/auth/refresh", cookies=cookies)
            data = response.json()

            assert response.status_code == 200
            assert "token" in data
            assert data["token"] == "new_access_token"
            mock_create_access_token.assert_called_once_with(data={"sub": "user_id"})


async def test_refresh_token_missing(ac: AsyncClient):
    response = await ac.post("/auth/refresh")
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "refresh token required"


async def test_refresh_token_invalid(ac: AsyncClient):
    with patch("jose.jwt.decode", side_effect=jwt.JWTError):
        cookies = {"refresh": "invalid_refresh_token"}

        response = await ac.post("/auth/refresh", cookies=cookies)
        data = response.json()

        assert response.status_code == 400
        assert data["detail"] == "Token error"
