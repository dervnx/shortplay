import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    # Application
    APP_NAME: str = "ShortPlay"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://shortplay:shortplay123@localhost:5432/shortplay"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # RabbitMQ
    RABBITMQ_URL: str = "amqp://shortplay:shortplay123@localhost:5672"

    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False

    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"

    # MiniMax LLM
    MINIMAX_API_KEY: str = ""
    MINIMAX_API_BASE: str = "https://api.minimax.chat/v1"
    MINIMAX_MODEL: str = "MiniMax-Text-01"
    MINIMAX_IMAGE_MODEL: str = "MiniMax-Image-01"

    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # CORS - comma-separated string, parsed manually
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
