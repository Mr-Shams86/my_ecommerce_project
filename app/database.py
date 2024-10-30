from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from typing import AsyncGenerator
import logging


Base = declarative_base()


SQLALCHEMY_DATABASE_URL = settings.database_async_url
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)


async_session = sessionmaker(
    bind=engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

# Генератор асинхронной сессии
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        
# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def init_db() -> None:
    try:
        async with engine.begin() as conn:
            # Создание всех таблиц
            await conn.run_sync(Base.metadata.create_all)
            logger.info("База данных инициализирована успешно.")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")