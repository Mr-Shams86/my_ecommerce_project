from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)  
    hashed_password = Column(String(255), nullable=False)  
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    carts = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")
    
    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, is_admin={self.is_admin})"