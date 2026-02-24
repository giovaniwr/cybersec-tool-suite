"""
Configurações centralizadas da aplicação via variáveis de ambiente (.env).
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/cybersec_db"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "insecure-default-key"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

