import pytest
from app.repositories.order_repo import OrderRepository
from app.repositories.user_repo import UserRepository
from app.repositories.product_repo import ProductRepository
from app.repositories.category_repo import CategoryRepository
from pydantic import BaseModel
from typing import List


# --- MOCKS ---
class MockUserCreate(BaseModel):
    name: str;
    email: str;
    password: str


class MockCategoryCreate(BaseModel):
    name: str


class MockProductCreate(BaseModel):
    name: str;
    price: float;
    category_id: int;
    description: str = ""


class MockOrderItemSchema(BaseModel):
    product_id: int
    quantity: int


class MockOrderCreate(BaseModel):
    delivery_address: str
    items: List[MockOrderItemSchema]


@pytest.mark.asyncio
async def test_create_order_logic(async_db):
    # 1. Подготовка: User, Category, Product
    user = await UserRepository(async_db).create(
        MockUserCreate(name="U", email="e@e.com", password="p"), "hash"
    )
    cat = await CategoryRepository(async_db).create(MockCategoryCreate(name="C"))

    prod1 = await ProductRepository(async_db).create(
        MockProductCreate(name="P1", price=100.0, category_id=cat.id)
    )
    prod2 = await ProductRepository(async_db).create(
        MockProductCreate(name="P2", price=50.0, category_id=cat.id)
    )

    # 2. Создание заказа (1 шт P1 и 2 шт P2)
    # Ожидаемая сумма: 100*1 + 50*2 = 200.0
    order_repo = OrderRepository(async_db)
    order_data = MockOrderCreate(
        delivery_address="Main St",
        items=[
            MockOrderItemSchema(product_id=prod1.id, quantity=1),
            MockOrderItemSchema(product_id=prod2.id, quantity=2),
        ]
    )

    order = await order_repo.create(user_id=user.id, order_data=order_data)

    # 3. Проверки
    assert order.id is not None
    assert order.total_amount == 200.0
    assert order.status == "new"


@pytest.mark.asyncio
async def test_get_user_orders(async_db):
    # Setup
    user = await UserRepository(async_db).create(
        MockUserCreate(name="U2", email="e2@e.com", password="p"), "hash"
    )
    order_repo = OrderRepository(async_db)

    # Создаем пустой заказ для простоты
    order_data = MockOrderCreate(delivery_address="Addr", items=[])
    await order_repo.create(user.id, order_data)

    orders = await order_repo.get_user_orders(user.id)
    assert len(orders) == 1
    assert orders[0].delivery_address == "Addr"