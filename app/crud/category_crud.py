from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException

async def create_category(db: AsyncSession, name: str):
    
    # Проверяем, существует ли категория с таким именем
    existing_category_result = await db.execute(select(Category).filter(Category.name == name))
    existing_category = existing_category_result.scalar_one_or_none()

    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    # Создаем новую категорию
    category = Category(name=name)
    db.add(category)
    await db.commit()
    await db.refresh(category) 
    return category


async def get_categories(db: AsyncSession):
    # Получаем список всех категорий
    result = await db.execute(select(Category))
    return result.scalars().all()

async def update_category(db: AsyncSession, category_id: int, new_name: str):
    # Обновляем категорию по ID
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.name = new_name
    db.add(category)
    await db.commit()
    await db.refresh(category)  
    return category

async def delete_category(db: AsyncSession, category_id: int):
    # Удаляем категорию по ID
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    await db.delete(category)
    await db.commit()
    return {"detail": "Category successfully deleted"}


