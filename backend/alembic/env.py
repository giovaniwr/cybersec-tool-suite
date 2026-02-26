import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context

# Garante que o pacote 'app' seja encontrado mesmo rodando alembic da raiz do backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import settings          # lê DATABASE_URL do .env
from app.database import Base                 # metadata base
import app.models.senha_validador_model       # noqa: F401 — registra tabelas no metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Aponta para o metadata dos models para autogenerate funcionar
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Modo offline: gera SQL sem conectar ao banco."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Modo online assíncrono: conecta ao PostgreSQL via asyncpg."""
    import ssl as _ssl

    _is_production = os.getenv("ENVIRONMENT", "development") == "production"

    # Lê DATABASE_URL direto do ambiente — ignora .env para funcionar no Docker
    db_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    # Remove query string existente
    db_url = db_url.split("?")[0]
    # Garante prefixo correto
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    engine_kwargs: dict = {}
    if _is_production:
        ssl_ctx = _ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = _ssl.CERT_NONE
        engine_kwargs["connect_args"] = {"ssl": ssl_ctx}

    connectable = create_async_engine(
        db_url,
        poolclass=pool.NullPool,
        **engine_kwargs,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
