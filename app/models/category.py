from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  

    products = relationship("Product", back_populates="category")  # Связь с продуктами
    posts = relationship("Post", back_populates="category")  # связь с постами

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
