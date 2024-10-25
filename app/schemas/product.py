from pydantic import BaseModel
from pydantic import Field
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., description="Название продукта")
    description: Optional[str] = Field(None, description="Описание продукта")
    price: float = Field(..., gt=0, description="Цена продукта (должна быть больше 0)")
    image_url: Optional[str] = Field(None, description="URL изображения продукта")
    category_id: int = Field(..., description="ID категории, к которой принадлежит продукт")

# Схема для создания продукта
class ProductCreate(ProductBase):
    pass  # Унаследует все поля от ProductBase

# Схема для обновления продукта
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Новое название продукта")
    description: Optional[str] = Field(None, description="Новое описание продукта")
    price: Optional[float] = Field(None, gt=0, description="Новая цена продукта (должна быть больше 0)")
    image_url: Optional[str] = Field(None, description="Новый URL изображения продукта")
    category_id: Optional[int] = Field(None, description="Новый ID категории, к которой принадлежит продукт")

# Схема для вывода информации о продукте
class ProductOut(ProductBase):
    id: int = Field(..., description="ID продукта")

    class Config:
        orm_mode = True