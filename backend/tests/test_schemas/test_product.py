import pytest
from pydantic import ValidationError
from app.schemas.product import ProductCreate

"""
Тестирование схем валидации товаров (ProductCreate):
- Проверка корректности типов данных (названия, цены, ID категории).
- Бизнес-валидация: проверка того, что цена не может быть отрицательной (ожидание ValidationError).
"""

def test_product_create_valid():
    data = {
        "name": "Handmade Soap",
        "price": 250.50,
        "category_id": 1,
        "description": "Natural ingredients"
    }
    product = ProductCreate(**data)
    assert product.price == 250.50

def test_product_create_invalid_price():
    data = {"name": "Soap", "price": -10, "category_id": 1}
    with pytest.raises(ValidationError):
        ProductCreate(**data)