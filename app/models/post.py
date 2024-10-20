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
    published = Column(Boolean, server_default="true")  
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    def __repr__(self):
        return (f"Post(id={self.id!r}, title={self.title!r}, content={self.content[:50]!r}, "
                f"published={self.published!r}, user_id={self.user_id!r}, category_id={self.category_id!r})")  