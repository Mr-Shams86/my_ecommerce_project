from pydantic import BaseModel
from pydantic import Field
from pydantic import conint
from typing import Optional


# Базовая схема для корзины
class CartBase(BaseModel):
    user_id: int = Field(..., description="ID пользователя, которому принадлежит корзина")
    product_id: int = Field(..., description="ID продукта, добавленного в корзину")
    quantity: Optional[conint(gt=0)] = Field(1, description="Количество товара в корзине (по умолчанию 1)")

# Схема для создания новой корзины
class CartCreate(CartBase):
    pass

# Схема для обновления корзины
class CartUpdate(BaseModel):
    quantity: Optional[conint(gt=0)] = Field(None, description="Обновляемое количество товара в корзине")

# Схема для чтения данных о корзине
class CartRead(CartBase):
    id: int = Field(..., description="ID записи корзины")

    class Config:
        orm_mode = True