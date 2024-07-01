from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env.local", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    DATABASE_URL: str
    SERVER_HOST: str
    SERVER_PORT: int
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    SMTP_PASS: str
    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    STRIPE_SECRET_KEY: str
    ENV: str


class TestSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=("../.env.test", ".env.test"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    ENV: str = "test"


def get_settings(env: str = "local") -> Settings:

    if env.lower() in ["test", "t", "testing"]:
        return TestSettings()
    if env.lower() in ["local", "l"]:
        return Settings()

    raise ValueError("Invalid environment. Must be 'dev' or 'test' ,'local'.")


settings = get_settings()
# settings = get_settings(env="test")
