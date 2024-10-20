from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str  


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None  
    password: Optional[str] = None    
    username: Optional[str] = None    

    class Config:
        orm_mode = True


class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool

# Схема для логина
class UserLogin(BaseModel):
    email: EmailStr
    password: str  
