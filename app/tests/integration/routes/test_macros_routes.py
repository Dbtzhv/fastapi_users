from httpx import AsyncClient


async def test_macros_success(ac: AsyncClient, valid_access_token):
    response = await ac.get("/macros", headers={"Authorization": valid_access_token})
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "calories": 2310,
        "proteins": 119,
        "fats": 56,
        "carbohydrates": 332
    }
