"""
Configuração da conexão assíncrona com o PostgreSQL usando SQLAlchemy.
"""
import os
import ssl
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

_is_production = os.getenv("ENVIRONMENT", "development") == "production"

def _build_engine_kwargs() -> dict:
    """
    Em produção (Render) passa SSL via connect_args.
    Em desenvolvimento (local/Docker) sem SSL.
    """
    if not _is_production:
        return {}
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    return {"connect_args": {"ssl": ssl_ctx}}

# URL sempre sem query string — SSL tratado via connect_args
_db_url = settings.DATABASE_URL.split("?")[0] if "?" in settings.DATABASE_URL else settings.DATABASE_URL

engine = create_async_engine(
    _db_url,
    echo=not _is_production,     # loga SQL apenas em dev
    pool_pre_ping=True,          # verifica conexão antes de usar
    pool_size=5,
    max_overflow=10,
    **_build_engine_kwargs(),
)

# Fábrica de sessões assíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Classe base para todos os modelos SQLAlchemy."""
    pass


async def get_db() -> AsyncSession:
    """Dependency do FastAPI — injeta uma sessão de banco por request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_tables():
    """Cria todas as tabelas no banco se não existirem (usado na inicialização)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
