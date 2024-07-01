from fastapi import Response

from app.security import (
    add_refresh_token_cookie,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)


def test_password_hash():
    password = "password123"
    hashed = get_password_hash(password)
    assert password != hashed, "Password was not hashed: " + hashed


def test_verify_password():
    password = "password123"
    hashed = "$2b$12$k16ZXqQk8PEBrhienxfV3OSRZ4/e8gMhsErhiG/Hw6J4TJatXsCs6"
    assert verify_password(password, hashed), "Password was not verified: " + hashed


def test_access_token_creation():
    access_token = create_access_token({"user_id": "1"})
    assert type(access_token) is str, "Access token is not a string: " + access_token


def test_refresh_token_creation():
    refresh_token = create_refresh_token({"user_id": "1"})
    assert type(refresh_token) is str, "Refresh token is not a string: " + refresh_token


def test_add_refresh_token_cookie():
    token = "test_token"
    response = Response()

    add_refresh_token_cookie(response, token)

    set_cookie_header = response.headers.get("set-cookie")
    assert set_cookie_header is not None, "Set-Cookie header not found"

    assert (
        "refresh=test_token" in set_cookie_header
    ), f"Expected 'refresh=test_token' in Set-Cookie, but got '{set_cookie_header}'"
    assert "httponly" in set_cookie_header.lower(), "Expected 'httponly' in Set-Cookie"
