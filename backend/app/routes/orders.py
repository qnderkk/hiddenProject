from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.order_item import OrderCreate, OrderResponse
from app.repositories.order_repo import OrderRepository
from app.repositories.product_repo import ProductRepository
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db)
    # Тут в будущем добавим: current_user = Depends(get_current_user)
):
    # Временно используем ID=1, пока не настроишь получение ID из токена на фронте
    user_id = 1

    o_repo = OrderRepository(db)
    p_repo = ProductRepository(db)
    service = OrderService(o_repo, p_repo)

    return await service.place_order(user_id, order_data)