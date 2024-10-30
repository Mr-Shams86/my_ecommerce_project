from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.schemas.product import ProductUpdate
from app.schemas.product import ProductOut


# Создание нового продукта
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
    return [ProductOut.from_orm(product) for product in products]  # Преобразование в Pydantic-схемы

# Получение продукта по ID
async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductOut.from_orm(product)  # Преобразование в Pydantic-схему

# Обновление продукта
async def update_product(db: AsyncSession, product_id: int, product_update: ProductUpdate):
    product = await get_product(db, product_id)  # Получаем продукт
    for var, value in product_update.dict(exclude_unset=True).items():
        setattr(product, var, value) # Обновляем поля продукта

    db.add(product)  # Добавляем обновленный продукт в сессию
    await db.commit() # Подтверждаем изменения
    await db.refresh(product) # Обновляем объект
    return ProductOut.from_orm(product)  # Преобразование в Pydantic-схему

# Удаление продукта
async def delete_product(db: AsyncSession, product_id: int):
    product = await get_product(db, product_id)  # Получаем продукт по ID
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)  # Удаляем продукт из сессии
    await db.commit()  # Подтверждаем изменения в базе данных
    return {"detail": "Product successfully deleted"}  # Возвращаем сообщение об успешном удалении