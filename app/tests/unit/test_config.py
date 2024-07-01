import pytest

from app.config import get_settings


@pytest.mark.parametrize("env", ["test", "local", "non-existent"])
def test_local_settings(env):
    if env == "non-existent":
        with pytest.raises(ValueError):
            get_settings(env=env)
    else:
        settings = get_settings(env=env)
        assert settings.DATABASE_URL == "sqlite:///test.db"
        assert settings.SERVER_HOST == "127.0.0.1"
        assert settings.SERVER_PORT == 8000
        assert settings.SECRET_KEY == "test_secret"
        assert settings.REFRESH_SECRET_KEY == "test_refresh_secret"
        assert settings.ALGORITHM == "HS256"
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
        assert settings.REFRESH_TOKEN_EXPIRE_MINUTES == 60
        assert settings.ENV == "test"
