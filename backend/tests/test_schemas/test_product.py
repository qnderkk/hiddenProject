import pytest
from pydantic import ValidationError

from app.schemas.product import ProductCreate

def test_product_create_valid():
    """Проверка создания товара с корректными данными"""
    data = {
        "name": "Handmade Soap",
        "price": 250.50,
        "category_id": 1,
        "description": "Natural ingredients"
    }
    product = ProductCreate(**data)
    assert product.price == 250.50

def test_product_create_invalid_price():
    """Цена должна быть больше 0 (gt=0)"""
    data = {"name": "Soap", "price": -10, "category_id": 1}
    with pytest.raises(ValidationError):
        ProductCreate(**data)