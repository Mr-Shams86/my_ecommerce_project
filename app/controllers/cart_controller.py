from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cart import CartItem
from app.models.product import Product
from app.database import get_async_session
from app.helpers.auth_helper import get_current_user
from app.schemas.cart import CartResponse 


router = APIRouter()



@router.post("/", response_model=CartResponse)
async def add_to_cart(
    product_id: int,
    quantity: int = 1,
    db: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user)
):
    # Проверяем, существует ли продукт
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Проверяем, есть ли уже товар в корзине
    existing_item = await db.execute(select(CartItem).where(CartItem.user_id == user.id, CartItem.product_id == product_id))
    cart_item = existing_item.scalar_one_or_none()
    
    if cart_item:
        # Если товар уже есть в корзине, обновляем его количество
        cart_item.quantity += quantity
        await db.commit()
        await db.refresh(cart_item)  
        return cart_item
    else:
        # Если товара нет в корзине, добавляем новый
        cart_item = CartItem(user_id=user.id, product_id=product_id, quantity=quantity)
        db.add(cart_item)
        await db.commit()
        await db.refresh(cart_item)
        return cart_item

@router.get("/", response_model=list[CartResponse])
async def get_cart_items(
    db: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user)
):
    # Получаем все товары из корзины текущего пользователя
    result = await db.execute(select(CartItem).where(CartItem.user_id == user.id))
    cart_items = result.scalars().all()
    return cart_items

@router.delete("/{cart_item_id}", response_model=dict)
async def remove_from_cart(
    cart_item_id: int,
    db: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user)
):
    # Находим товар в корзине
    result = await db.execute(select(CartItem).where(CartItem.id == cart_item_id, CartItem.user_id == user.id))
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Удаляем товар из корзины
    await db.delete(cart_item)
    await db.commit()
    return {"message": "Item removed successfully"}  