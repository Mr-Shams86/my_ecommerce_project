from jose import JWTError
from jose import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from datetime import timedelta
from app.schemas.user import UserOut
from app.crud import user_crud
from app.database import get_async_session
from app.config import settings


# Определение схемы безопасности OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHM = "HS256"

class JWTService:
    @staticmethod
    async def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=30))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_session)
    ) -> UserOut:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось проверить учетные данные.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Расшифровка токена
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # Поиск пользователя в базе данных
        user = await user_crud.get_user_by_id(db, user_id=user_id)  # Убедитесь, что эта функция определена в user_crud
        if user is None:
            raise credentials_exception
        return UserOut.from_orm(user)  # Приведение к Pydantic-схеме

    @staticmethod
    async def verify_user(
        token: str,
        db: AsyncSession,
        require_admin: bool = False
    ) -> UserOut:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось проверить учетные данные.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Расшифровка токена
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # Поиск пользователя в базе данных
        user = await user_crud.get_user_by_id(db, user_id=user_id)
        if user is None:
            raise credentials_exception

        if require_admin and not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Доступ запрещен. Только администраторы могут выполнять это действие.",
            )
        
        return UserOut.from_orm(user)  # Приведение к Pydantic-схеме