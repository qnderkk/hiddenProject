from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0,
                         description="Product price")
    category_id: int = Field(..., description="Category ID")
    image_url: Optional[str] = Field(None, description="Product image URL")


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int = Field(..., description="Product ID")

    class Config:
        from_attributes = True