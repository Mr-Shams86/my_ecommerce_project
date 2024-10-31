from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.jwt_service import oauth2_scheme
from app.crud.user_crud import get_user_by_username
from app.database import get_async_session
from app.config import settings
import logging
from jose import JWTError
from jose import jwt


# Настройка логирования
logger = logging.getLogger(__name__)

async def get_current_active_user(
    request: Request, 
    db: AsyncSession = Depends(get_async_session), 
    token: str = Depends(oauth2_scheme)
):
    """
    Получение текущего активного пользователя на основе JWT токена.

    :param request: Объект запроса FastAPI.
    :param db: Асинхронная сессия базы данных.
    :param token: JWT токен, передаваемый в заголовке запроса.
    :raises HTTPException: Если токен не может быть проверен или пользователь не найден.
    :return: Объект пользователя.
    """
    # Проверка на заполненность request.state.user
    if hasattr(request.state, "user"):
        logger.info("User found in request.state.")
        return request.state.user

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("JWT payload does not contain a username.")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"JWT error: {e}")
        raise credentials_exception

    user = await get_user_by_username(db, username)
    if user is None:
        logger.warning(f"User not found: {username}")
        raise credentials_exception

    logger.info(f"User {username} authenticated successfully.")
    request.state.user = user  # Заполнение request.state для дальнейшего использования
    return user
