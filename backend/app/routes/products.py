import os
import shutil
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.product import ProductResponse, ProductCreate
from app.repositories.product_repo import ProductRepository
from app.config import settings

router = APIRouter(prefix="/products", tags=["Products"])

UPLOAD_DIR = settings.image_dir
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[ProductResponse])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    return await repo.get_all()

@router.post("/", response_model=ProductResponse)
async def create_product(
    name: str = Form(..., description="Название товара"),
    price: float = Form(..., description="Цена товара"),
    category_id: int = Form(..., description="ID категории"),
    description: Optional[str] = Form(None, description="Описание"),
    file: Optional[UploadFile] = File(None, description="Изображение товара"),
    db: AsyncSession = Depends(get_db)
):
    image_url = None

    if file:
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        image_url = f"/static/images/{unique_filename}"

    product_data = ProductCreate(
        name=name,
        price=price,
        category_id=category_id,
        description=description,
        image_url=image_url
    )

    repo = ProductRepository(db)
    return await repo.create(product_data)

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    success = await repo.delete(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return {"message": "Удалено", "id": product_id}
