from fastapi import HTTPException
from fastapi import Depends
from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserOut
from app.services.jwt_service import JWTService
from passlib.context import CryptContext
import logging



# Настройка логгирования
logger = logging.getLogger(__name__)

# Контекст для работы с хэшированием паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def admin_required(current_user: UserOut = Depends(JWTService.get_current_user)):
    """Функция для проверки прав администратора у текущего пользователя."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен. Только администраторы могут выполнять это действие.",
        )
    return current_user

async def create_user(db: AsyncSession, username: str, email: str, password: str) -> User:
    """Создает нового пользователя, если такой пользователь еще не зарегистрирован."""
    existing_user_by_username = await db.execute(select(User).filter(User.username == username))
    if existing_user_by_username.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    existing_user_by_email = await db.execute(select(User).filter(User.email == email))
    if existing_user_by_email.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    
    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating user: {e}")  
        raise HTTPException(status_code=500, detail="Failed to create user")
        
    return new_user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    """Аутентифицирует пользователя по email и паролю."""
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalar_one_or_none()
    
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    
    return None