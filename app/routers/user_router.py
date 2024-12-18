from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user import UserCreate
from app.schemas.user import UserRead
from app.schemas.user import UserLogin
from app.crud import user_crud
from app.services.jwt_service import create_access_token
from app.services.jwt_service import get_current_user
from app.services.jwt_service import get_admin_user
from app.database import get_async_session
from logging_config import logger  # Импорт логирования

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Регистрация нового пользователя
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_async_session)):
    logger.info(f"Attempting to register user with email: {user_in.email}")
    existing_user = await user_crud.get_user_by_email(db, email=user_in.email)
    if existing_user:
        logger.error(f"Registration failed: user with email {user_in.email} already exists")
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует.")
    
    user = await user_crud.create_user(db, user_in)
    logger.info(f"User registered successfully: {user.email}")
    return user

# Логин пользователя и получение JWT токена
@router.post("/login", response_model=dict)
async def login_user(user_in: UserLogin, db: AsyncSession = Depends(get_async_session)):
    logger.info(f"User login attempt: {user_in.email}")
    user = await user_crud.authenticate_user(db, email=user_in.email, password=user_in.password)
    if not user:
        logger.error(f"Login failed for user: {user_in.email}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль.")
    
    access_token = await create_access_token(data={"sub": str(user.id)})
    logger.info(f"User logged in successfully: {user_in.email}")
    return {"access_token": access_token, "token_type": "bearer"}

# Получение текущего аутентифицированного пользователя
@router.get("/me", response_model=UserRead)
async def get_me(current_user = Depends(get_current_user)):
    logger.info(f"Fetching current user: {current_user.email}")
    return current_user

# Только администраторы могут просматривать всех пользователей
@router.get("/", response_model=List[UserRead], dependencies=[Depends(get_admin_user)])
async def get_users(db: AsyncSession = Depends(get_async_session)):
    logger.info(f"Admin fetching all users")
    users = await user_crud.get_all_users(db)
    logger.info(f"{len(users)} users fetched by admin")
    return users