from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(5000), nullable=False)
    published = Column(Boolean, server_default="true")  # Указание на опубликованность поста
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))  # Связь с таблицей пользователей
    user = relationship("User", back_populates="posts")  # Обратная связь с моделью User
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))  # Связь с категорией
    category = relationship("Category", back_populates="posts")  # Обратная связь с моделью Category

    def __repr__(self):
        return (f"Post(id={self.id!r}, title={self.title!r}, content={self.content[:50]!r}, "
                f"published={self.published!r}, user_id={self.user_id!r}, category_id={self.category_id!r})")