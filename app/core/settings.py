from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Uses pydantic-settings for type-safe configuration.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        case_sensitive=False,
    )

    environment: str = "dev"
    debug: bool = True
    sentry_dsn: str | None = None

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS
    cors_origins: list[str] = ["*"]

    # Database
    database_url: str | None = None
    redis_url: str = "redis://localhost:6379/0"
    rq_default_queue_name: str = "default"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(
        cls,
        value: str | list[str] | None,
    ) -> list[str]:
        if value is None:
            return ["*"]
        if isinstance(value, list):
            return value
        items = [item.strip() for item in value.split(",")]
        return [item for item in items if item]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()


