from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from typing import Optional


# Базовая схема пользователя
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    username: str = Field(..., description="Имя пользователя")

# Схема для создания нового пользователя
class UserCreate(UserBase):
    password: str = Field(..., description="Пароль пользователя")

# Схема для обновления информации о пользователе
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Новая электронная почта")
    password: Optional[str] = Field(None, description="Новый пароль")
    username: Optional[str] = Field(None, description="Новое имя пользователя")

# Схема для чтения данных о пользователе
class UserRead(UserBase):
    id: int = Field(..., description="ID пользователя")
    is_active: bool = Field(..., description="Активен ли пользователь")
    is_admin: bool = Field(..., description="Является ли пользователь администратором")

# Схема для логина пользователя
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Схема для ответа с токеном
class TokenResponse(BaseModel):
    access_token: str
    
    
# Схема для возврата данных о пользователе (можно использовать вместо UserRead)
class UserOut(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True