from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.cart import Cart

async def create_cart_item(db: AsyncSession, user_id: int, product_id: int, quantity: int):
    
    # Проверка на существование товара в корзине пользователя
    existing_item_result = await db.execute(
        select(Cart).filter(Cart.user_id == user_id, Cart.product_id == product_id)
    )
    existing_item = existing_item_result.scalar_one_or_none()

    if existing_item:
        # Если товар уже в корзине, просто увеличиваем количество
        existing_item.quantity += quantity
        await db.commit()
        await db.refresh(existing_item)
        return existing_item

    # Если товара нет, добавляем новый элемент в корзину
    cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(cart_item)
    await db.commit()
    await db.refresh(cart_item)
    return cart_item

async def get_cart_items(db: AsyncSession, user_id: int):
    result = await db.execute(select(Cart).filter(Cart.user_id == user_id))
    return result.scalars().all()

async def delete_cart_item(db: AsyncSession, cart_item_id: int):
    result = await db.execute(select(Cart).filter(Cart.id == cart_item_id))
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        return None  

    await db.delete(cart_item)
    await db.commit()
    return cart_item

