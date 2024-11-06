from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import settings
import logging


Base = declarative_base()

# Асинхронный движок для использования в FastAPI
SQLALCHEMY_DATABASE_URL_ASYNC = settings.database_async_url
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC, echo=True)

# Синхронный движок для Alembic
SQLALCHEMY_DATABASE_URL_SYNC = settings.database_sync_url
sync_engine = create_engine(SQLALCHEMY_DATABASE_URL_SYNC, echo=True)

# Асинхронная сессия для использования в FastAPI
async_session = sessionmaker(
    bind=async_engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

# Генератор асинхронной сессии
async def get_async_session():
    async with async_session() as session:
        yield session
        
# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def init_db() -> None:
    try:
        async with async_engine.begin() as conn:
            # Создание всех таблиц
            await conn.run_sync(Base.metadata.create_all)
            logger.info("База данных инициализирована успешно.")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")