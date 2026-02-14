import pytest
from sqlalchemy.exc import IntegrityError
from app.models.category import Category
from app.models.product import Product


def test_create_category(db):
    category = Category(name="Electronics")
    db.add(category)
    db.commit()
    db.refresh(category)

    assert category.id is not None
    assert category.name == "Electronics"


def test_create_product_with_category(db):
    # Сначала создаем категорию
    category = Category(name="Books")
    db.add(category)
    db.commit()

    # Создаем продукт, привязанный к категории
    product = Product(
        name="Python Guide",
        description="Learn Python",
        price=59.99,
        category_id=category.id
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    assert product.id is not None
    assert product.category_id == category.id
    # Проверяем работу relationship (SQLAlchemy сама подтянет объект)
    assert product.category.name == "Books"


def test_category_products_relationship(db):
    category = Category(name="Toys")
    db.add(category)
    db.commit()

    product1 = Product(name="Car", price=10.0, category_id=category.id)
    product2 = Product(name="Doll", price=15.0, category_id=category.id)
    db.add_all([product1, product2])
    db.commit()

    db.refresh(category)
    # Проверяем back_populates="products" со стороны категории
    assert len(category.products) == 2
    assert category.products[0].name in ["Car", "Doll"]