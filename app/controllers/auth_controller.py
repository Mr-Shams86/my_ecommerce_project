from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from app.models.user import User
from app.helpers.auth_helper import create_user
from app.helpers.auth_helper import authenticate_user
from app.services.jwt_service import create_access_token
from app.database import get_db
from app.dependencies import get_current_active_user


router = APIRouter()

# Модели для валидации
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    
    # Проверка на уникальность пользователя по имени или email
    existing_user = await db.execute(select(User).filter((User.username == user.username) | (User.email == user.email)))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="User with this username or email already exists.")
    
    # Создание пользователя
    return await create_user(db, user.username, user.email, user.password)

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    # Аутентификация пользователя
    authenticated_user = await authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Создание токена доступа
    access_token = await create_access_token(data={"sub": authenticated_user.id})
    return {"access_token": access_token}