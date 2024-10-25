from fastapi import Request
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.jwt_service import JWTService
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Получаем заголовок авторизации
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=401, detail="Требуется аутентификация.")

        try:
            # Извлекаем токен из заголовка Authorization
            token = authorization.split(" ")[1]
            # Раскодируем токен и извлекаем данные пользователя
            user_data = JWTService.decode_token(token)
        except (IndexError, ValueError) as e:
            raise HTTPException(status_code=401, detail="Неверный токен или ошибка аутентификации.") from e
        except Exception as e:
            raise HTTPException(status_code=401, detail="Ошибка аутентификации.") from e

        # Открываем сессию базы данных и проверяем, существует ли пользователь
        async with request.state.db as db:
            result = await db.execute(select(User).where(User.id == user_data["user_id"]))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(status_code=401, detail="Пользователь не найден.")

        # Добавляем пользователя в контекст запроса
        request.state.user = user

        response = await call_next(request)
        return response
