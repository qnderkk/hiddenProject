from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas.order_item import OrderCreate, OrderResponse
from ..repositories.order_repo import OrderRepository
from ..repositories.product_repo import ProductRepository
from ..services.order_service import OrderService

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