from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from app.database import Base

class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)  

    # Связь с заказами
    orders = relationship("Order", back_populates="status_relation")

    def __repr__(self):
        return f"<OrderStatus(id={self.id}, name='{self.name}')>"