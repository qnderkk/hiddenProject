from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..models.product import Product
from ..schemas.product import ProductCreate


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all(self):
        result = await self.db.execute(select(Product))
        return result.scalars().all()
    
    async def get_by_id(self, product_id: int):
        return await self.db.get(Product, product_id)
    
    async def create(self, product_data: ProductCreate):
        db_product = Product(**product_data.model_dump())
        self.db.add(db_product)
        await self.db.commit()
        await self.db.refresh(db_product)
        return db_product
    
    async def delete(self, product_id: int):
        product = await self.get_by_id(product_id)
        if product:
            await self.db.delete(product)
            await self.commit()
        return product

    async def commit(self):
        await self.db.commit()