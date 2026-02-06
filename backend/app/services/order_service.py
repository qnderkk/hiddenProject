from fastapi import HTTPException, status
from app.repositories.order_repo import OrderRepository
from app.repositories.product_repo import ProductRepository
from app.schemas.order_item import OrderCreate

class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo

    async def place_order(self, user_id: int, order_data: OrderCreate):
        if not order_data.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Корзина пуста. Невозможно создать заказ."
            )

        for item in order_data.items:
            product = await self.product_repo.get_by_id(item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Товар с ID {item.product_id} не найден."
                )
            
        new_order = await self.order_repo.create(user_id, order_data)
        
        return new_order

    async def get_my_orders(self, user_id: int):
        return await self.order_repo.get_user_orders(user_id)

    async def get_order_details(self, order_id: int, user_id: int):
        order = await self.order_repo.get_order_by_id(order_id)
        
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")
            
        if order.user_id != user_id:
            raise HTTPException(status_code=403, detail="Нет доступа к чужому заказу")
            
        return order