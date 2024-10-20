from app.database import get_async_session
from models.order_status import OrderStatus
from sqlalchemy.future import select

async def add_default_order_statuses():
    async with get_async_session() as db:
        statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]

        for status in statuses:
            existing_status = await db.execute(select(OrderStatus).where(OrderStatus.name == status))
            if existing_status.scalars().first() is None:
                db.add(OrderStatus(name=status))
        
        await db.commit()

