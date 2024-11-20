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
    is_active: bool = Field(default=True, description="Активен ли пользователь")
    is_admin: bool = Field(default=False, description="Является ли пользователь администратором")

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
    username: Optional[str] = None  # Необязательное поле
    email: Optional[EmailStr] = None  # Необязательное поле
    password: str  # Обязательное поле
    
    def validate_credentials(self):
        if not self.username and not self.email:
            raise ValueError("Either 'username' or 'email' must be provided.")

# Схема для ответа с токеном
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    
# Схема для возврата данных о пользователе 
class UserOut(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True