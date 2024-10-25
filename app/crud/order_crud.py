from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.order import Order

# Создание нового заказа
async def create_order(db: AsyncSession, user_id: int):
    order = Order(user_id=user_id)
    db.add(order)
    await db.commit()   
    await db.refresh(order)
    
    return {"detail": "Order successfully created", "order": order}  

# Получение всех заказов пользователя
async def get_orders(db: AsyncSession, user_id: int):
    # Получаем заказы по ID пользователя с загрузкой связанных элементов заказа
    result = await db.execute(
        select(Order).filter(Order.user_id == user_id).options(joinedload(Order.items))
    )
    return result.scalars().all()   

# Обновление статуса заказа
async def update_order_status(db: AsyncSession, order_id: int, status: str):
    # Получаем заказ по его ID
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalar_one_or_none()   
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Обновляем статус заказа
    order.status = status
    await db.commit()   
    await db.refresh(order)   
    
    return order
