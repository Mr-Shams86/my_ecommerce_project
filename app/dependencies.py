from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.jwt_service import oauth2_scheme
from app.services.jwt_service import JWTService
from app.database import get_async_session
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

async def get_current_active_user(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme),
):
    if hasattr(request.state, "user"):
        logger.info("User found in request.state.")
        return request.state.user

    try:
        user = await JWTService.get_current_user(token, db)
        request.state.user = user
        return user
    except HTTPException as e:
        logger.warning(f"Authentication failed: {e.detail}")
        raise e
