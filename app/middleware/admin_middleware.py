from fastapi import Request
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.models.user import User
from app.services.jwt_service import JWTService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class AdminMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Получаем заголовок авторизации
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=403, detail="Требуется авторизация.")

        try:
            # Извлекаем токен из заголовка Authorization
            token = authorization.split(" ")[1]
            # Раскодируем токен и извлекаем данные пользователя
            user_data = JWTService.decode_token(token)
        except (IndexError, ValueError) as e:
            raise HTTPException(status_code=403, detail="Неверный токен или ошибка аутентификации.") from e
        except Exception as e:
            raise HTTPException(status_code=403, detail="Ошибка аутентификации.") from e

        async with request.state.db as db:  # Используем соединение с базой данных
            # Получаем пользователя по ID из токена
            result = await db.execute(select(User).where(User.id == user_data["user_id"]))
            user = result.scalar_one_or_none()

            if not user or not user.is_admin:
                raise HTTPException(status_code=403, detail="Доступ разрешён только администраторам.")
            
        response = await call_next(request)
        return response