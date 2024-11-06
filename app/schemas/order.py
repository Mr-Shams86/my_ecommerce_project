from pydantic import BaseModel
from pydantic import Field
from enum import Enum
from app.models.order import OrderStatusEnum  # Импорт перечисления Enum


class OrderStatusEnum(Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderCreate(BaseModel):
    user_id: int = Field(..., description="ID пользователя, создающего заказ")
    product_id: int = Field(..., description="ID продукта, который заказывается")
    quantity: int = Field(..., gt=0, description="Количество товара, должно быть больше 0")

class OrderResponse(BaseModel):
    id: int = Field(..., description="ID заказа")
    user_id: int = Field(..., description="ID пользователя, которому принадлежит заказ")
    total_price: float = Field(..., description="Общая цена заказа")
    status: str = Field(..., description="Текущий статус заказа")  

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatusEnum = Field(..., description="Новый статус заказа")

    class Config:
        arbitrary_types_allowed = True
