from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category
from app.database import get_async_session
from app.schemas.category import CategoryResponse
from app.schemas.category import CategoryCreate
from app.schemas.category import CategoryUpdate

router = APIRouter()

# Вспомогательная функция для получения категории по ID
async def get_category_by_id(category_id: int, db: AsyncSession):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,  
    db: AsyncSession = Depends(get_async_session)
):
    new_category = Category(name=category.name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return categories

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_async_session)):
    return await get_category_by_id(category_id, db)

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,  
    db: AsyncSession = Depends(get_async_session)
):
    category = await get_category_by_id(category_id, db)

    # Обновляем поля категории
    category.name = category_update.name
    await db.commit()
    await db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_async_session)):
    category = await get_category_by_id(category_id, db)

    await db.delete(category)
    await db.commit()
