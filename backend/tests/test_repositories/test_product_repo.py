import pytest
from app.repositories.product_repo import ProductRepository
from app.repositories.category_repo import CategoryRepository
from pydantic import BaseModel


# Заглушки для схем
class MockCategoryCreate(BaseModel):
    name: str


class MockProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    category_id: int
    image_url: str | None = None


@pytest.mark.asyncio
async def test_create_product(async_db):
    # Сначала создаем категорию
    cat_repo = CategoryRepository(async_db)
    cat = await cat_repo.create(MockCategoryCreate(name="Test Cat"))

    # Создаем продукт
    prod_repo = ProductRepository(async_db)
    prod_data = MockProductCreate(
        name="Smartphone",
        description="New phone",
        price=999.99,
        category_id=cat.id
    )

    product = await prod_repo.create(prod_data)

    assert product.id is not None
    assert product.price == 999.99
    assert product.category_id == cat.id


@pytest.mark.asyncio
async def test_delete_product(async_db):
    # Setup
    cat_repo = CategoryRepository(async_db)
    cat = await cat_repo.create(MockCategoryCreate(name="Temp"))

    prod_repo = ProductRepository(async_db)
    prod = await prod_repo.create(MockProductCreate(name="P1", price=10, category_id=cat.id))

    # Delete
    await prod_repo.delete(prod.id)

    # Verify
    found = await prod_repo.get_by_id(prod.id)
    assert found is None