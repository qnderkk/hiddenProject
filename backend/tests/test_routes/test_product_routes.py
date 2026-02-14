import pytest
import io

"""
Тестирование каталога товаров:
- GET /products/: Проверка получения списка товаров (включая сценарий с пустым списком).
- POST /products/: Тестирование создания товара с загрузкой файла (Multipart/form-data). 
  Проверяется корректная обработка текстовых полей вместе с бинарным контентом изображения.
"""

@pytest.mark.asyncio
async def test_get_products_empty(client):
    response = await client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_product_route(client, async_db):
    from app.models.category import Category
    cat = Category(name="Electronics")
    async_db.add(cat)
    await async_db.commit()

    file_content = b"fake-image-binary-content"
    file = io.BytesIO(file_content)

    form_data = {
        "name": "iPhone 15",
        "price": "999.99",
        "category_id": str(cat.id),
        "description": "Latest Apple phone"
    }

    response = await client.post(
        "/products/",
        data=form_data,
        files={"file": ("test.png", file, "image/png")}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "iPhone 15"
    assert "image_url" in data