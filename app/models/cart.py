from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)  # Идентификатор корзины
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Идентификатор пользователя
    user = relationship("User", back_populates="carts")  # Связь с моделью User
    cart_items = relationship("CartItem", back_populates="cart")  # Связь с элементами корзины

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id})>"

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)  # Идентификатор элемента корзины
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)  # Идентификатор продукта
    quantity = Column(Integer, default=1)  # Количество продукта в корзине
    product = relationship("Product")  # Связь с моделью Product
    cart = relationship("Cart", back_populates="cart_items")  # Связь с моделью Cart

    def __repr__(self):
        return f"<CartItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
