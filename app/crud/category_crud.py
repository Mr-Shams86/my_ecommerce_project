from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category
from fastapi import HTTPException


# Создание новой категории
async def create_category(db: AsyncSession, name: str):
    # Проверка на существование категории с таким именем
    existing_category_result = await db.execute(
        select(Category).filter(Category.name == name)
    )
    existing_category = existing_category_result.scalar_one_or_none()

    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    # Создание новой категории
    category = Category(name=name)
    db.add(category)
    await db.commit()
    await db.refresh(category) 
    return category

# Получение всех категорий
async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()

# Обновление категории по ID
async def update_category(db: AsyncSession, category_id: int, new_name: str):
    # Поиск категории по ID
    result = await db.execute(
        select(Category).filter(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Обновление имени категории
    category.name = new_name
    await db.commit()
    await db.refresh(category)  
    return category

# Удаление категории по ID
async def delete_category(db: AsyncSession, category_id: int):
    # Поиск категории по ID
    result = await db.execute(
        select(Category).filter(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Удаление категории
    await db.delete(category)
    await db.commit()
    return {"detail": "Category successfully deleted"}