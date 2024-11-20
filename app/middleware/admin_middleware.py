from fastapi import Request
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.jwt_service import JWTService
from app.database import get_async_session
import logging

logger = logging.getLogger("admin_middleware")



class AdminMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_paths = ["/login", "/register", "/docs", "/openapi.json"]
        if request.url.path in excluded_paths:
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            logger.error("Authorization header missing.")
            raise HTTPException(status_code=403, detail="Authorization required.")

        try:
            token = authorization.split(" ")[1]
            async with get_async_session() as db:
                user = await JWTService.verify_user(token, db, admin_only=True)
                request.state.user = user
        except HTTPException as e:
            logger.error(f"Authorization failed: {e.detail}")
            raise

        return await call_next(request)