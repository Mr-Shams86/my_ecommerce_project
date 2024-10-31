from fastapi import HTTPException
from fastapi import Depends
from fastapi import status
from app.services.jwt_service import JWTService
from app.crud.user_crud import create_user as crud_create_user
from app.crud.user_crud import authenticate_user as crud_authenticate_user
from app.schemas.user import UserCreate
from app.schemas.user import UserOut
from passlib.context import CryptContext


# Контекст для работы с хэшированием паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user_data: UserCreate) -> UserOut:
    user = await crud_create_user(user_data.username, user_data.email, user_data.password)
    return UserOut.from_orm(user)

async def authenticate_user(username: str, password: str) -> UserOut:
    user = await crud_authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",  # Улучшение пользовательского опыта
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserOut.from_orm(user)

async def admin_required(current_user: UserOut = Depends(JWTService.get_current_user)) -> UserOut:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admins only.",
        )
    return current_user