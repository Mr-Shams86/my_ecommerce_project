from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.schemas.product import ProductUpdate
from app.schemas.product import ProductOut
from app.services.jwt_service import get_current_user
from app.services.jwt_service import get_admin_user  
from app.models.user import User

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# Получение всех продуктов
@router.get("/", response_model=List[ProductOut])
async def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

# Получение продукта по ID
@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Создание нового продукта (только для администраторов)
@router.post("/", response_model=ProductOut)
async def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_admin_user)
):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Обновление продукта (только для администраторов)
@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int, 
    product: ProductUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_admin_user)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

# Удаление продукта (только для администраторов)
@router.delete("/{product_id}")
async def delete_product(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_admin_user)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted successfully"}
