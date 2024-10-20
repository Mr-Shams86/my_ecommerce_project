from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.order import Order
from app.models.order import OrderStatus
from app.database import get_async_session
from app.helpers.auth_helper import get_current_user
from app.schemas.order import OrderResponse
from app.schemas.order import OrderStatusUpdate


router = APIRouter()

# Получение всех заказов для администратора
@router.get("/orders/", response_model=list[OrderResponse])
async def get_all_orders(db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    
    # Проверяем, является ли пользователь администратором
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have access to this resource.")
    
    result = await db.execute(select(Order))
    orders = result.scalars().all()
    return orders

# Добавление нового статуса заказа
@router.post("/order-status/", response_model=OrderStatus)
async def add_order_status(status_data: OrderStatusUpdate, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    # Проверяем, является ли пользователь администратором
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have access to this resource.")
    
    # Создаем новый статус заказа
    new_status = OrderStatus(status=status_data.status)
    db.add(new_status)
    await db.commit()  
    await db.refresh(new_status)
    
    return new_status