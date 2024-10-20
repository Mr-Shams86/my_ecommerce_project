from sqlalchemy import Column 
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# Определение статусов заказа
class OrderStatus(enum.Enum):
    pending = "pending"      # Заказ оформлен, но не подтверждён
    confirmed = "confirmed"   # Заказ подтверждён
    shipped = "shipped"       # Заказ отправлен
    delivered = "delivered"   # Заказ доставлен
    cancelled = "cancelled"   # Заказ отменён

# Модель для заказа
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Внешний ключ на пользователя
    total_price = Column(Integer, nullable=False)  # Итоговая сумма заказа в копейках
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)  # Статус заказа
    
    # Связи
    user = relationship("User", back_populates="orders")  # Связь с пользователем
    items = relationship("OrderItem", back_populates="order")  # Связь с OrderItem

    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, status={self.status}, total_price={self.total_price})"

# Модель для элемента заказа (OrderItem)    
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)  # Количество единиц товара, не может быть null
    price = Column(Integer, nullable=False)  # Цена на момент заказа, не может быть null    
    
    # Связи
    order = relationship("Order", back_populates="items")  # Связь с Order
    product = relationship("Product", back_populates="order_items")  # Связь с продуктом 
    
    def __repr__(self):
        return f"OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity}, price={self.price})"


    
    


