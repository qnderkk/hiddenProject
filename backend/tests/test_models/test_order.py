from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.category import Category
from app.models.product import Product

"""
Комплексные тесты заказов и их состава:
- Создание заказа пользователем и проверка его атрибутов (адрес, сумма, статус).
- Проверка связей Many-to-Many / One-to-Many: Order -> OrderItem -> Product.
- Тестирование навигации по объектам (например, получение email заказчика через объект заказа).
"""

def test_create_order(db):
    user = User(name="Buyer", email="buyer@test.com", hashed_password="pw")
    db.add(user)
    db.commit()

    order = Order(
        user_id=user.id,
        delivery_address="123 Test St",
        total_amount=100.0
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    assert order.id is not None
    assert order.status == "new"
    assert order.created_at is not None
    assert order.user.email == "buyer@test.com"


def test_order_items_relationship(db):
    user = User(name="Buyer2", email="buyer2@test.com", hashed_password="pw")
    db.add(user)

    cat = Category(name="Food")
    db.add(cat)
    db.commit()

    prod = Product(name="Apple", price=1.5, category_id=cat.id)
    db.add(prod)
    db.commit()

    order = Order(user_id=user.id, delivery_address="Home", total_amount=15.0)
    db.add(order)
    db.commit()

    item = OrderItem(
        order_id=order.id,
        product_id=prod.id,
        quantity=10,
        price=1.5
    )
    db.add(item)
    db.commit()

    db.refresh(order)
    db.refresh(item)

    assert len(order.items) == 1
    assert order.items[0].product.name == "Apple"
    assert item.order.delivery_address == "Home"