from sqlalchemy import DECIMAL
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  
    description = Column(String)
    price = Column(DECIMAL(10, 2), nullable=False)  
    image_url = Column(String)  
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return (f"Product(id={self.id!r}, name={self.name!r}, "
                f"price={self.price!r}, image_url={self.image_url!r})")  