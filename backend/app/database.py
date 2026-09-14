"""
Configuración de la base de datos con SQLAlchemy async.
"""
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    """Base para todos los modelos."""
    pass


# Motor async de base de datos
engine = create_async_engine(
    settings.database_url,
    echo=False,  # Cambiar a True para debug SQL
    future=True,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """Dependencia para obtener una sesión de base de datos."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Crea todas las tablas al iniciar la app."""
    # Importar modelos para que se registren en Base.metadata
    from app.models import test_result  # noqa: F401
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)