from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext  
from app.models import User  
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate  


# Контекст для работы с хэшированием паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    # Создаем нового пользователя и хэшируем его пароль
    db_user = User(**user.dict())
    db_user.hashed_password = pwd_context.hash(user.password)  
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    # Получаем пользователя по ID
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> User:
    # Получаем пользователя по имени
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> User:
    # Получаем пользователя по email
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
    # Обновляем информацию о пользователе
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int) -> User:
    # Удаляем пользователя по ID
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(db_user)
    await db.commit()
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    """Проверяет правильность email и пароля пользователя."""
    user = await get_user_by_email(db, email=email)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user