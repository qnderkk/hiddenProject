# import pytest
# from pydantic import ValidationError
# from app.schemas.order_item import OrderCreate, OrderItemCreaete

# """
# Тестирование схем создания заказов и их позиций:
# - OrderCreate: проверка вложенной структуры данных (список позиций внутри заказа).
# - OrderItemCreate: валидация количества товара (количество не может быть нулевым или отрицательным).
# """

# def test_order_create_valid():
#     data = {
#         "delivery_address": "Moscow, Red Square 1",
#         "items": [
#             {"product_id": 1, "quantity": 2},
#             {"product_id": 2, "quantity": 1}
#         ]
#     }
#     order = OrderCreate(**data)
#     assert len(order.items) == 2
#     assert order.items[0].quantity == 2

# def test_order_item_invalid_quantity():
#     with pytest.raises(ValidationError):
#         OrderItemCreaete(product_id=1, quantity=0)