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
from app.schemas.user import TokenResponse


router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    existing_user = await user_crud.get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists.",
        )

    existing_email = await user_crud.get_user_by_email(db, email=user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists.",
        )
        
    # Автоматическое назначение is_admin для первого пользователя
    is_admin = not bool(await db.execute("SELECT COUNT(*) FROM users"))
    user.is_admin = is_admin    

    new_user = await user_crud.create_user(db, user)
    return UserOut.from_orm(new_user)


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_async_session)):
    authenticated_user = None
    if user.username:
        authenticated_user = await user_crud.authenticate_user_by_username(db, user.username, user.password)
    elif user.email:
        authenticated_user = await user_crud.authenticate_user_by_email(db, user.email, user.password)

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username, email, or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await JWTService.create_access_token(data={"sub": authenticated_user.id})
    return TokenResponse(access_token=access_token)
