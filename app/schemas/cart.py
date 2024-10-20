from pydantic import BaseModel
from typing import Optional

# Базовая схема для корзины
class CartBase(BaseModel):
    user_id: int
    product_id: int
    quantity: Optional[int] = 1  
    
# Схема для создания новой корзины
class CartCreate(CartBase):
    pass

# Схема для обновления корзины
class CartUpdate(BaseModel):
    quantity: Optional[int]

# Схема для чтения данных о корзине
class CartRead(CartBase):
    id: int

    class Config:
        orm_mode = True  

