from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "TransitPulse AI"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    API_PORT: int = 8000
    DATABASE_URL: str = "postgresql+asyncpg://transitpulse:transitpulse_secret@localhost:5432/transitpulse_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_BUS_LOCATION_TTL: int = 120

    JWT_SECRET: str = "super_secret_jwt_key_change_in_production_32chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200

    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
