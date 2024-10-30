from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_async_db
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.schemas.product import ProductUpdate
from app.schemas.product import ProductOut
from app.schemas.user import UserOut
from app.services.jwt_service import get_admin_user

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# Получение всех продуктов
@router.get("/", response_model=List[ProductOut])
async def get_products(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_db)):
    query = select(Product).offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    return products

# Получение продукта по ID
@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Создание нового продукта (только для администраторов)
@router.post("/", response_model=ProductOut)
async def create_product(
    product: ProductCreate, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: UserOut = Depends(get_admin_user)  # Обновите тип возвращаемого пользователя
):
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Обновление продукта (только для администраторов)
@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int, 
    product: ProductUpdate, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: UserOut = Depends(get_admin_user)  # Обновите тип возвращаемого пользователя
):
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    db_product = result.scalar_one_or_none()
    
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Удаление продукта (только для администраторов)
@router.delete("/{product_id}", response_model=dict)
async def delete_product(
    product_id: int, 
    db: AsyncSession = Depends(get_async_db), 
    current_user: UserOut = Depends(get_admin_user)  # Обновите тип возвращаемого пользователя
):
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    db_product = result.scalar_one_or_none()
    
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await db.delete(db_product)
    await db.commit()
    return {"detail": "Product deleted successfully"}
