from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.schemas.product import ProductUpdate


async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        image_url=product.image_url,
        category_id=product.category_id
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Получение всех продуктов
async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products

# Получение продукта по ID
async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    return result.scalar_one_or_none()

# Обновление продукта
async def update_product(db: AsyncSession, product_id: int, product_update: ProductUpdate):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Обновляем только переданные поля
    update_data = product_update.dict(exclude_unset=True)
    for var, value in update_data.items():
        setattr(product, var, value)

    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

# Удаление продукта
async def delete_product(db: AsyncSession, product_id: int):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return {"detail": "Product successfully deleted"}