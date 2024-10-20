from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: int

# Схема для создания продукта
class ProductCreate(ProductBase):
    pass  # Унаследует все поля от ProductBase

# Схема для обновления продукта
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

# Схема для вывода информации о продукте
class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True 


# Если нужен отдельный класс Product
class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True