import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, MagicMock
from app.services.order_service import OrderService
from app.schemas.order_item import OrderCreate

"""
Тестирование логики оформления заказов (OrderService):
- Валидация корзины: проверка выброса ошибки 400 (HTTPException), если список товаров пуст.
- Проверка наличия товаров: выброс ошибки 404, если запрашиваемого продукта не существует в базе.
- Процесс оформления: проверка успешного вызова метода создания заказа в репозитории при корректных входных данных.
- Изоляция: использование Mock для разделения логики заказов и товаров.
"""

@pytest.fixture
def order_repo_mock():
    return MagicMock()


@pytest.fixture
def product_repo_mock():
    return MagicMock()


@pytest.fixture
def order_service(order_repo_mock, product_repo_mock):
    return OrderService(order_repo_mock, product_repo_mock)


@pytest.mark.asyncio
async def test_place_order_empty_items(order_service):
    order_data = OrderCreate(delivery_address="Address", items=[])

    with pytest.raises(HTTPException) as exc:
        await order_service.place_order(user_id=1, order_data=order_data)

    assert exc.value.status_code == 400
    assert "Корзина пуста" in exc.value.detail


@pytest.mark.asyncio
async def test_place_order_product_not_found(order_service, product_repo_mock):
    product_repo_mock.get_by_id = AsyncMock(return_value=None)

    order_data = OrderCreate(
        delivery_address="Address",
        items=[{"product_id": 999, "quantity": 1}]
    )

    with pytest.raises(HTTPException) as exc:
        await order_service.place_order(user_id=1, order_data=order_data)

    assert exc.value.status_code == 404
    assert "не найден" in exc.value.detail


@pytest.mark.asyncio
async def test_place_order_success(order_service, order_repo_mock, product_repo_mock):
    product_repo_mock.get_by_id = AsyncMock(return_value=MagicMock(id=1))
    order_repo_mock.create = AsyncMock(return_value=MagicMock(id=101))

    order_data = OrderCreate(
        delivery_address="Street 1",
        items=[{"product_id": 1, "quantity": 2}]
    )

    result = await order_service.place_order(user_id=1, order_data=order_data)

    assert result.id == 101
    order_repo_mock.create.assert_called_once()