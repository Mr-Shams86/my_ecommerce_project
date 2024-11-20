from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from passlib.context import CryptContext

# Настройка контекста для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)  
    hashed_password = Column(String(255), nullable=False)  
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  

    posts = relationship("Post", back_populates="user")  # Связь с постами
    carts = relationship("Cart", back_populates="user")  # Связь с корзинами
    orders = relationship("Order", back_populates="user")  # Связь с заказами
    
    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, is_admin={self.is_admin})"
    
    def set_password(self, password: str):
        """Устанавливает хэшированный пароль."""
        self.hashed_password = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Проверяет правильность пароля."""
        return pwd_context.verify(password, self.hashed_password)