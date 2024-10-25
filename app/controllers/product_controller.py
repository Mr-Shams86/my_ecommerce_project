from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from app.helpers.auth_helper import admin_required 
from sqlalchemy.ext.asyncio import AsyncSession 
from app.schemas.product import ProductCreate
from app.schemas.product import ProductUpdate
from app.schemas.product import ProductOut as ProductSchema
from app.helpers.auth_helper import admin_required  # Вынесем проверку администратора
from app.database import get_db
from app.crud.product_crud import (
    create_product,
    get_products as crud_get_products,
    get_product as crud_get_product,
    update_product as crud_update_product,
    delete_product as crud_delete_product
)

router = APIRouter()

# Основные маршруты для работы с продуктами
@router.post("/", response_model=ProductSchema)
async def create_product_endpoint(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_product(db, product)

@router.get("/", response_model=list[ProductSchema])
async def get_products(db: AsyncSession = Depends(get_db)):
    return await crud_get_products(db)

@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud_get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Админские маршруты для управления продуктами
@router.post("/admin/", response_model=ProductSchema)
async def add_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(admin_required)
):
    return await create_product(db, product)

@router.put("/admin/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    admin=Depends(admin_required)
):
    updated_product = await crud_update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return updated_product

@router.delete("/admin/{product_id}", response_model=dict)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(admin_required)
):
    deleted_product = await crud_delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"detail": "Product successfully deleted"}