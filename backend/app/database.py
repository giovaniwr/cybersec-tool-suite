"""
Configuração da conexão assíncrona com o PostgreSQL usando SQLAlchemy.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Motor assíncrono — usa asyncpg por baixo dos panos
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",  # loga SQL apenas em dev
    pool_pre_ping=True,                           # verifica conexão antes de usar
    pool_size=10,
    max_overflow=20,
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

