import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(f".env.{os.getenv('ENV', 'dev')}", ".env"),
        extra="ignore",
    )

    env: str = "dev"

    project_name: str = "fastapi-base"

    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/fastapi_base"
    database_echo: bool = False
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_pool_timeout: int = 30
    database_pool_recycle: int = 1800
    database_pool_pre_ping: bool = True

    jwt_secret: str = "change_me"
    jwt_alg: str = "HS256"

    redis_url: str = "redis://localhost:6379/0"

    cors_origins: list[str] = ["*"]
    rate_limit: str = "100/minute"
    cache_prefix: str = "fastapi-cache"


settings = Settings()
