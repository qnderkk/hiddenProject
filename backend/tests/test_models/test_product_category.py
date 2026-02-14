from sqlalchemy.exc import IntegrityError
import pytest
from app.models.category import Category
from app.models.product import Product


@pytest.mark.asyncio
async def test_product_price_required(db_session):
    # 1. Создаем категорию (тут все ок)
    category = Category(name="Тест")
    db_session.add(category)
    await db_session.flush()

    # 2. Пытаемся добавить продукт без цены
    product = Product(name="No Price", price=None, category_id=category.id)
    db_session.add(product)

    # 3. Ожидаем ошибку именно на этапе отправки в базу (flush)
    with pytest.raises(IntegrityError):
        await db_session.flush()

    # Больше ничего делать не нужно, фикстура сама сделает rollback