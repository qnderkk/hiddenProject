from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity")


class OrderItemCreate(OrderItemBase): # Убрал лишнюю 'e'
    pass


class OrderItemUpdate(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity")


class OrderItemResponse(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity")
    price: int = Field(..., description="Product price")

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    delivery_address: str = Field(..., min_length=1, description="Order address")
    items: List[OrderItemCreate] # И тут соответственно тоже

class OrderCreate(OrderBase):
    pass


class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: float
    delivery_address: str
    created_at: datetime
    
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True