from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from pydantic import BaseModel
from pydantic import Field
from app.database import Base



class CategoryBase(BaseModel):
    name: str = Field(..., description="Название категории")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int = Field(..., description="ID категории")

    class Config:
        from_attributes = True