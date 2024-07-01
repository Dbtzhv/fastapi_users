import pytest


@pytest.fixture(scope="function", autouse=True)
async def mock_env_vars(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    monkeypatch.setenv("SERVER_HOST", "127.0.0.1")
    monkeypatch.setenv("SERVER_PORT", "8000")
    monkeypatch.setenv("SECRET_KEY", "test_secret")
    monkeypatch.setenv("REFRESH_SECRET_KEY", "test_refresh_secret")
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    monkeypatch.setenv("REFRESH_TOKEN_EXPIRE_MINUTES", "60")
    monkeypatch.setenv("ENV", "test")
