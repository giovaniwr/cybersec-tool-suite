"""
Configurações centralizadas da aplicação via variáveis de ambiente (.env).
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/cybersec_db"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "insecure-default-key"

    # Origens permitidas no CORS — separadas por vírgula no .env
    # Ex: ALLOWED_ORIGINS=https://meusite.onrender.com,https://www.meusite.com
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

