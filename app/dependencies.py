from fastapi import Depends
from fastapi import HTTPException
from jose import JWTError
from jose import  jwt
from app.services.jwt_service import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.crud.user_crud import get_user_by_username
from app.database import get_db
from app.config import settings

async def get_current_active_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
