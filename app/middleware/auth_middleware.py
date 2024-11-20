from fastapi import Request
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.jwt_service import JWTService
from app.database import get_async_session
import logging

logger = logging.getLogger("auth_middleware")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_paths = ["/docs", "/openapi.json", "/register", "/login"]
        if request.url.path in public_paths:
            return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            logger.error("Authentication required but no token provided.")
            raise HTTPException(status_code=401, detail="Authentication required.")

        try:
            token = authorization.split(" ")[1]
            async with get_async_session() as db:
                user = await JWTService.verify_user(token, db)
                request.state.user = user
        except HTTPException as e:
            logger.error(f"Authentication failed: {e.detail}")
            raise HTTPException(status_code=e.status_code, detail=e.detail) from e

        return await call_next(request)