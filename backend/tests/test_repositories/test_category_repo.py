import pytest
from app.repositories.category_repo import CategoryRepository
from pydantic import BaseModel


class MockCategoryCreate(BaseModel):
    name: str


@pytest.mark.asyncio
async def test_create_category(async_db):
    repo = CategoryRepository(async_db)
    data = MockCategoryCreate(name="Gadgets")

    cat = await repo.create(data)
    assert cat.id is not None
    assert cat.name == "Gadgets"


@pytest.mark.asyncio
async def test_get_all_categories(async_db):
    repo = CategoryRepository(async_db)
    await repo.create(MockCategoryCreate(name="Cat1"))
    await repo.create(MockCategoryCreate(name="Cat2"))

    all_cats = await repo.get_all()
    assert len(all_cats) == 2


@pytest.mark.asyncio
async def test_get_by_name(async_db):
    repo = CategoryRepository(async_db)
    await repo.create(MockCategoryCreate(name="UniqueName"))

    cat = await repo.get_by_name("UniqueName")
    assert cat is not None
    assert cat.name == "UniqueName"


@pytest.mark.asyncio
async def test_delete_category(async_db):
    repo = CategoryRepository(async_db)
    cat = await repo.create(MockCategoryCreate(name="To Delete"))

    # Удаляем
    deleted_cat = await repo.delete(cat.id)
    assert deleted_cat.id == cat.id

    # Проверяем, что в базе больше нет
    check = await repo.get_by_id(cat.id)
    assert check is None