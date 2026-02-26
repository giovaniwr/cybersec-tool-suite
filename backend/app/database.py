"""
Configuração da conexão assíncrona com o PostgreSQL usando SQLAlchemy.
"""
import os
import ssl
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

_is_production = os.getenv("ENVIRONMENT", "development") == "production"

# asyncpg exige SSL via connect_args — não via query string na URL
# Remove ?ssl=require da URL se existir para evitar conflito
_db_url = settings.DATABASE_URL.split("?")[0] if "?" in settings.DATABASE_URL else settings.DATABASE_URL

_connect_args = {}
if _is_production:
    # Render exige SSL — usa ssl=True que o asyncpg aceita corretamente
    _connect_args = {"ssl": True}

engine = create_async_engine(
    _db_url,
    echo=not _is_production,     # loga SQL apenas em dev
    pool_pre_ping=True,          # verifica conexão antes de usar
    pool_size=5,
    max_overflow=10,
    connect_args=_connect_args,
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
