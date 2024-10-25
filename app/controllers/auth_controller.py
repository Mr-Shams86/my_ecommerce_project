from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.helpers.auth_helper import create_user
from app.helpers.auth_helper import authenticate_user
from app.services.jwt_service import create_access_token
from app.database import get_db
from app.schemas.user import UserCreate
from app.schemas.user import UserLogin
from app.schemas.user import UserRead
from app.schemas.user import TokenResponse
router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверка на уникальность пользователя по email
    existing_user = await db.execute(
        select(User).filter((User.email == user.email))
    )
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    # Создание пользователя
    new_user = await create_user(db, user.username, user.email, user.password)
    return UserRead.from_orm(new_user)

@router.post("/login",  response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    # Аутентификация пользователя
    authenticated_user = await authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Создание токена доступа
    access_token = await create_access_token(data={"sub": str(authenticated_user.id)})
    return TokenResponse(access_token=access_token)  # Возвращаем схему