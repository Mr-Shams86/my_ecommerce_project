from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


# Базовая схема пользователя
class UserBase(BaseModel):
    email: EmailStr
    username: str

    class Config:
        orm_mode = True  # Позволяет использовать SQLAlchemy модели

# Схема для создания нового пользователя
class UserCreate(UserBase):
    password: str  

# Схема для обновления информации о пользователе
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None  
    password: Optional[str] = None    
    username: Optional[str] = None    

    class Config:
        orm_mode = True  # Добавлено для совместимости с SQLAlchemy моделями

# Схема для чтения данных о пользователе
class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True  # Добавлено для совместимости с SQLAlchemy моделями

# Схема для логина пользователя
class UserLogin(BaseModel):
    email: EmailStr
    password: str