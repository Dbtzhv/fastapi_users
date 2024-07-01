import pytest
from httpx import AsyncClient


async def test_macros_success(ac: AsyncClient, valid_access_token):
    response = await ac.get("/users/all", headers={"Authorization": valid_access_token})
    data = response.json()

    assert response.status_code == 200
    assert data[0]["email"] == "admin@admin.com"


@pytest.mark.parametrize(
    "old_password, new_password, expected_status, detail",
    [
        ("password", "new_password", 200, None),
        (
            "password",
            "password",
            400,
            "New password cannot be the same as old password",
        ),
        ("wrong_password", "new_password", 400, "Incorrect password"),
    ],
)
async def test_update_user_password(
    ac: AsyncClient,
    old_password,
    new_password,
    expected_status,
    detail,
    valid_access_token,
):
    response = await ac.patch(
        "/users/change_password",
        json={"password": old_password, "new_password": new_password},
        headers={"Authorization": valid_access_token},
    )
    data = response.json()

    assert response.status_code == expected_status
    if detail:
        assert data["detail"] == detail


async def test_current_user(ac: AsyncClient, valid_access_token):
    response = await ac.get(
        "/users/current_user", headers={"Authorization": valid_access_token}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "admin@admin.com"


@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        (1, 200),
        (2, 404),
    ],
)
async def test_fetch_user(
    ac: AsyncClient, valid_access_token, user_id, expected_status
):
    response = await ac.get(
        f"/users/{user_id}", headers={"Authorization": valid_access_token}
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "user_id, endpoint_response",
    [
        (4, "User with id 4 not found"),
        (1, "User with id 1 has been updated"),
    ],
)
async def test_fetch_user(
    ac: AsyncClient, valid_access_token, user_id, endpoint_response
):
    response = await ac.patch(
        f"/users/{user_id}",
        json={"is_active": False},
        headers={"Authorization": valid_access_token},
    )

    if user_id == 4:
        assert response.json()["detail"] == endpoint_response
    else:
        assert response.json() == endpoint_response
