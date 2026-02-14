from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.category import Category
from app.models.product import Product


def test_create_order(db):
    # Подготовка данных (User)
    user = User(name="Buyer", email="buyer@test.com", hashed_password="pw")
    db.add(user)
    db.commit()

    # Создание заказа
    order = Order(
        user_id=user.id,
        delivery_address="123 Test St",
        total_amount=100.0
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    assert order.id is not None
    assert order.status == "new"  # Проверка default значения
    assert order.created_at is not None
    assert order.user.email == "buyer@test.com"


def test_order_items_relationship(db):
    # 1. Создаем пользователя
    user = User(name="Buyer2", email="buyer2@test.com", hashed_password="pw")
    db.add(user)

    # 2. Создаем категорию и продукт
    cat = Category(name="Food")
    db.add(cat)
    db.commit()  # Коммит нужен, чтобы получить ID

    prod = Product(name="Apple", price=1.5, category_id=cat.id)
    db.add(prod)
    db.commit()

    # 3. Создаем заказ
    order = Order(user_id=user.id, delivery_address="Home", total_amount=15.0)
    db.add(order)
    db.commit()

    # 4. Добавляем позицию в заказ (OrderItem)
    item = OrderItem(
        order_id=order.id,
        product_id=prod.id,
        quantity=10,
        price=1.5
    )
    db.add(item)
    db.commit()

    # Обновляем данные из БД
    db.refresh(order)
    db.refresh(item)

    # Проверки
    assert len(order.items) == 1
    assert order.items[0].product.name == "Apple"
    assert item.order.delivery_address == "Home"