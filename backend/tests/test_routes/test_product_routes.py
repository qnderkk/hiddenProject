import pytest
import io


@pytest.mark.asyncio
async def test_get_products_empty(client):
    response = await client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_product_route(client, async_db):
    # Для создания товара нужна категория (создаем напрямую в БД через репозиторий или роут)
    # Предположим, категория с ID=1 уже создана или создадим её здесь
    from app.models.category import Category
    cat = Category(name="Electronics")
    async_db.add(cat)
    await async_db.commit()

    # Имитируем отправку формы с файлом
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