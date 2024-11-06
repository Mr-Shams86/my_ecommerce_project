from fastapi import Request
from fastapi import Depends
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.jwt_service import JWTService
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


class AdminMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db: AsyncSession = Depends(get_async_session)):
        super().__init__(app)
        self.db = db

    async def dispatch(self, request: Request, call_next):
        # Исключаем маршруты, которые не требуют проверки прав администратора
        if request.url.path in ["/docs", "/openapi.json", "/register"]:
            return await call_next(request)

        # Получаем заголовок авторизации
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=403, detail="Authorization required.")

        try:
            token = authorization.split(" ")[1]
            user = await JWTService.verify_user(token, self.db, admin_only=True)
            request.state.user = user
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail) from e

        return await call_next(request)