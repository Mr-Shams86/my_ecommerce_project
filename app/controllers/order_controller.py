from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.order_crud import OrderCRUD
from app.models.order import OrderItem
from app.models.cart import CartItem
from app.models.order import OrderStatusEnum
from app.database import get_async_session
from app.services.jwt_service import JWTService  # Импорт JWTService вместо get_current_user
from app.helpers.auth_helper import admin_required
from app.schemas.order import OrderResponse
from app.schemas.order import OrderStatusUpdate


router = APIRouter()

@router.post("/", response_model=OrderResponse)
async def create_order(db: AsyncSession = Depends(get_async_session), user = Depends(JWTService.get_current_user)
):
    # Проверяем наличие товаров в корзине
    cart_items_result = await db.execute(select(CartItem).where(CartItem.user_id == user.id))
    cart_items = cart_items_result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Считаем общую сумму заказа
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Создание нового заказа через OrderCRUD
    new_order = await OrderCRUD.create_order(db, user.id, total_price, OrderStatusEnum.pending)


    # Создаем записи для заказанных товаров и очищаем корзину
    async with db.begin():
        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.add(order_item)
            await db.delete(item)  # Удаляем товар из корзины

    await db.commit()
    return new_order

@router.get("/", response_model=list[OrderResponse])
async def get_orders(db: AsyncSession = Depends(get_async_session), user = Depends(JWTService.get_current_user)
):
    # Получаем все заказы текущего пользователя
    orders = await OrderCRUD.get_orders(db, user.id)
    return orders

@router.patch("/{order_id}/status/", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: AsyncSession = Depends(get_async_session),
    admin=Depends(admin_required)  # Проверка, является ли пользователь администратором
):
    # Обновляем статус заказа через OrderCRUD
    order = await OrderCRUD.update_order_status(db, order_id, status_update.status)
    return order