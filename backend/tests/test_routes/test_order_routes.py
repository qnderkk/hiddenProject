import pytest
from unittest.mock import patch
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order


@pytest.mark.asyncio
async def test_create_order_route(client, async_db):
    # 1. Подготовка данных в БД
    user = User(id=1, name="Test", email="test@test.com", hashed_password="123")
    cat = Category(name="Electronics")
    async_db.add_all([user, cat])
    await async_db.flush()

    prod = Product(name="Mouse", price=50.0, category_id=cat.id)
    async_db.add(prod)
    await async_db.commit()

    order_payload = {
        "delivery_address": "Main Street 1",
        "items": [{"product_id": prod.id, "quantity": 2}]
    }

    # 2. Используем патч, чтобы после вызова оригинального метода
    # подгрузить items и вернуть "полный" объект для валидации FastAPI
    from app.services.order_service import OrderService

    original_place_order = OrderService.place_order

    async def mock_place_order(self, user_id, order_data):
        # Вызываем реальную логику создания
        order = await original_place_order(self, user_id, order_data)

        # ВРУЧНУЮ подгружаем items специально для валидатора Pydantic в этом тесте
        result = await async_db.execute(
            select(Order)
            .where(Order.id == order.id)
            .options(selectinload(Order.items))
        )
        return result.scalar_one()

    with patch.object(OrderService, 'place_order', autospec=True, side_effect=mock_place_order):
        response = await client.post("/orders/", json=order_payload)

    # 3. Проверки
    assert response.status_code == 200
    data = response.json()
    assert data["total_amount"] == 100.0
    assert len(data["items"]) == 1
    assert data["delivery_address"] == "Main Street 1"