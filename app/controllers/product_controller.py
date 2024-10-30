from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.helpers.auth_helper import admin_required
from app.schemas.product import ProductCreate
from app.schemas.product import ProductUpdate
from app.schemas.product import ProductOut
from app.schemas.user import UserOut  # Pydantic схема
from app.database import get_async_session
from app.crud.product_crud import (
    create_product,
    get_products as crud_get_products,
    get_product as crud_get_product,
    update_product as crud_update_product,
    delete_product as crud_delete_product
)

router = APIRouter()

# Основные маршруты для работы с продуктами

# Создание продукта
@router.post("/", response_model=ProductOut)
async def create_product_endpoint(
    product: ProductCreate,
    db: AsyncSession = Depends(get_async_session)
):
    db_product = await create_product(db, product)
    return ProductOut.from_orm(db_product)

# Получение всех продуктов
@router.get("/", response_model=list[ProductOut])
async def get_products(db: AsyncSession = Depends(get_async_session)):
    products = await crud_get_products(db)
    return [ProductOut.from_orm(product) for product in products]

# Получение продукта по ID
@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_async_session)):
    product = await crud_get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut.from_orm(product)

# Админские маршруты для управления продуктами
@router.post("/admin/", response_model=ProductOut)
async def add_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserOut = Depends(admin_required)  # Вместо admin
):
    db_product = await create_product(db, product)
    return ProductOut.from_orm(db_product)

@router.put("/admin/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserOut = Depends(admin_required)  # Вместо admin
):
    updated_product = await crud_update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut.from_orm(updated_product)

@router.delete("/admin/{product_id}", response_model=dict)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: UserOut = Depends(admin_required)  # Вместо admin
):
    deleted_product = await crud_delete_product(db, product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product successfully deleted"}