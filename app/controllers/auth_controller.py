from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user_crud
from app.services.jwt_service import JWTService 
from app.database import get_async_session
from app.schemas.user import UserCreate
from app.schemas.user import UserLogin
from app.schemas.user import UserOut


router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    # Проверка, существует ли пользователь с таким же именем пользователя или email
    existing_user = await user_crud.get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует."
        )
    
    existing_email = await user_crud.get_user_by_email(db, email=user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует."
        )

    # Создание пользователя
    new_user = await user_crud.create_user(db, user)  # Передаем объект UserCreate
    return UserOut.from_orm(new_user)  # Приведение к Pydantic-схеме

@router.post("/login", response_model=str)  # Возвращаем строку с токеном
async def login(user: UserLogin, db: AsyncSession = Depends(get_async_session)):
    # Аутентификация пользователя
    authenticated_user = await user_crud.authenticate_user(db, user.username, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создание и возвращение токена
    access_token = await JWTService.create_access_token(data={"sub": authenticated_user.id})
    return access_token
