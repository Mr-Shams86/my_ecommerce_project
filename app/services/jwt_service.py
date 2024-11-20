from jose import JWTError
from jose import jwt
from jose import ExpiredSignatureError
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
import logging

logger = logging.getLogger(__name__)
# Определение схемы безопасности OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class JWTService:
    @staticmethod
    async def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        logger.info("Creating access token...")
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
            logger.info("Access token created successfully.")
            return encoded_jwt
        except Exception as e:
            logger.error(f"Failed to create access token: {e}")
            raise


    @staticmethod
    async def decode_token(token: str) -> dict:
        logger.info("Decoding token...")
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            logger.info("Token decoded successfully.")
            return payload
        except ExpiredSignatureError:
            logger.warning("Token has expired.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except JWTError:
            logger.error(f"JWT decoding error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)
    ) -> UserOut:
        logger.info("Validating current user from token...")
        payload = await JWTService.decode_token(token)
        user_id: str = payload.get("sub")
        if not user_id:
            logger.warning("User ID is missing in token.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID is missing in token.",
            )

        user = await user_crud.get_user_by_id(db, user_id=user_id)
        if not user:
            logger.warning(f"User with ID {user_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found.",
            )
    
        logger.info(f"User with ID {user_id} validated successfully.")
        return UserOut.from_orm(user)


    @staticmethod
    async def verify_user(
        token: str,
        db: AsyncSession,
        require_admin: bool = False
    ) -> UserOut:
        """
        Проверяет пользователя из токена, а также его права администратора.
        """
        payload = JWTService.decode_token(token)
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID is missing in token."
            )

        user = await user_crud.get_user_by_id(db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found."
            )

        if require_admin and not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required."
            )
        
        return UserOut.from_orm(user)