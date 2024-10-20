from pydantic import BaseModel
from pydantic import Field
from app.models.order import OrderStatus

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str  

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus  