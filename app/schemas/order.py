from pydantic import BaseModel
from pydantic import Field
from app.models.order import OrderStatus

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
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus = Field(..., description="Новый статус заказа")