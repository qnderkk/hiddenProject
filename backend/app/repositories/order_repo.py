from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order_item import OrderCreate


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_id: int, order_data: OrderCreate):
        db_order = Order(
            user_id=user_id,
            delivery_address=order_data.delivery_address,
            status="new",
            total_amount=0.0
        )
        self.db.add(db_order)

        await self.db.flush()

        total_price = 0.0

        for item in order_data.items:
            product = await self.db.get(Product, item.product_id)

            if product:
                item_price = product.price * item.quantity
                total_price += item_price

                db_item = OrderItem(
                    order_id=db_order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    price=product.price
                )
                self.db.add(db_item)

        db_order.total_amount = total_price

        await self.db.commit()
        await self.db.refresh(db_order)
        return db_order
    
    async def get_user_orders(self, user_id: int):
        result = await self.db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
        )
        return result.scalars().all()
    
    async def get_order_by_id(self, order_id: int):
        result = await self.db.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order))
        )
        return result.scalars().all()


