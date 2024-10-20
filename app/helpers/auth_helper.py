from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from passlib.context import CryptContext
import logging

# Настройка логгирования
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def admin_required(current_user: User):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have access to this resource.")

async def create_user(db: AsyncSession, username: str, email: str, password: str):
    existing_user = await db.execute(select(User).filter(User.username == username))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating user: {e}")  
        raise HTTPException(status_code=500, detail="Failed to create user")
        
    return new_user

async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalar_one_or_none()
    if user and pwd_context.verify(password, user.password):
        return user
    return None