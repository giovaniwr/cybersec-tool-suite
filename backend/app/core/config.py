"""
Configurações centralizadas da aplicação via variáveis de ambiente (.env).
Em produção (Render), as variáveis vêm do ambiente do sistema — sem arquivo .env.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

_ENV_FILE = os.path.join(os.path.dirname(__file__), "../../.env")


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/cybersec_db"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "insecure-default-key"

    # Origens permitidas no CORS — separadas por vírgula no .env / variável de ambiente
    # Ex: ALLOWED_ORIGINS=https://meusite.onrender.com,https://www.meusite.com
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        # env_file é opcional — ignora se não existir (produção no Render)
        env_file=_ENV_FILE if os.path.exists(_ENV_FILE) else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

