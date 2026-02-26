"""
Configurações centralizadas da aplicação via variáveis de ambiente (.env).
Em produção (Render), as variáveis vêm do ambiente do sistema — sem arquivo .env.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import os

_ENV_FILE = os.path.join(os.path.dirname(__file__), "../../.env")


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/cybersec_db"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "insecure-default-key"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_database_url(cls, v):
        """
        Converte postgres:// ou postgresql:// para postgresql+asyncpg://
        e adiciona ?ssl=require para o Render.
        """
        if isinstance(v, str):
            if v.startswith("postgres://"):
                v = v.replace("postgres://", "postgresql+asyncpg://", 1)
            elif v.startswith("postgresql://"):
                v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
            # Render exige SSL — adiciona se ainda não estiver na URL
            if "ssl=" not in v and "oregon-postgres.render.com" in v:
                v += "?ssl=require"
        return v

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE if os.path.exists(_ENV_FILE) else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()


def get_allowed_origins() -> list[str]:
    """
    Lê ALLOWED_ORIGINS do ambiente de forma segura.
    Aceita string separada por vírgula ou valor único.
    Fallback para localhost em desenvolvimento.
    """
    raw = os.getenv("ALLOWED_ORIGINS", "")
    if not raw:
        return ["http://localhost:5173", "http://127.0.0.1:5173"]
    return [o.strip() for o in raw.split(",") if o.strip()]
