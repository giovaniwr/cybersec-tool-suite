"""
Configurações centralizadas da aplicação via variáveis de ambiente (.env).
Em produção (Render), as variáveis vêm do ambiente do sistema — sem arquivo .env.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List
import os

_ENV_FILE = os.path.join(os.path.dirname(__file__), "../../.env")


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/cybersec_db"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "insecure-default-key"

    # Aceita string separada por vírgula OU lista JSON
    # Ex Render:  ALLOWED_ORIGINS=https://cybersec-frontend.onrender.com
    # Ex local:   ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # tenta JSON primeiro: '["https://..."]'
            import json
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
            # fallback: string separada por vírgula
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE if os.path.exists(_ENV_FILE) else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
