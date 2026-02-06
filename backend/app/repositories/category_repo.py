from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.category import Category
from ..schemas.category import CategoryCreate


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Category))
        return result.scalars().all()
    
    async def get_by_id(self, category_id: int):
        return await self.db.get(Category, category_id)
    
    async def get_by_name(self, name: str):
        result = await self.db.execute(
            select(Category).where(Category.name == name)
        )
        return result.scalar_one_or_none()
    
    async def create(self, category_data: CategoryCreate):
        db_category =  Category(
            name=category_data.name
        )
        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        return db_category
    
    async def delete(self, category_id: int):
        category = await self.get_by_id(category_id)
        if category:
            await self.db.delete(category)
            await self.db.commit()
        return category
    

    