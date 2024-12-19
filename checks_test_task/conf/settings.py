from enum import Enum
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(str, Enum):
    TESTING = "TESTING"
    DEV = "DEV"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    ENV: Env = Env.DEV
    PORT: int = 4000
    ALLOWED_ORIGINS: str = "http://localhost http://localhost:3000 http://127.0.0.1:3000"
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days

    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    DB_DRIVER: str = "postgresql+asyncpg"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_TTL: int = 3600

    @property
    def sqlalchemy_database_uri(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
