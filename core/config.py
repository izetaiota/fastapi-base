import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(f".env.{os.getenv('ENV', 'dev')}", ".env"),
        extra="ignore",
    )

    env: str = "dev"

    project_name: str = "fastapi-base"

    database_url: str = "mysql+asyncmy://root:Zl952610@127.0.0.1:3306/fastapi_base?charset=utf8mb4"
    database_echo: bool = False
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_pool_timeout: int = 30
    database_pool_recycle: int = 1800
    database_pool_pre_ping: bool = True

    admin_access_token_expire_minutes: int = 60
    admin_bootstrap_token: str = ""

    jwt_secret: str = "fastapi-base"
    jwt_alg: str = "HS256"

    redis_url: str = "redis://localhost:6379/0"

    cors_origins: str = "*"
    rate_limit: str = "100/minute"
    cache_prefix: str = "fastapi-cache"

    @property
    def cors_origins_list(self) -> list[str]:
        s = (self.cors_origins or "").strip()
        if not s or s == "*":
            return ["*"]
        return [item.strip() for item in s.split(",") if item.strip()]


settings = Settings()
