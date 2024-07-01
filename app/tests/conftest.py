import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session, engine
from app.main import app
from app.models.user import User
from app.security import create_access_token


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.ENV == "test"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    user = {
        "email": "admin@admin.com",
        "hashed_password": "$2b$12$JH0KQ08oyPWt3HYMggPtj.5T.5sXjN3e8RQAnD4Ny2QHrP3SoBr/e",
        "weight": 70,
        "is_superuser": True
    }

    async with async_session() as session:
        add_users = insert(User).values(user)

        await session.execute(add_users)
        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/auth/login", data={"username": "admin@admin.com", "password": "password"}
        )
        assert ac.cookies["refresh"]
        yield ac


@pytest.fixture(scope="function")
async def get_test_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()


@pytest.fixture
def valid_access_token():
    token = create_access_token(data={"sub": "1"})
    return f"Bearer {token}"
