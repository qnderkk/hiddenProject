from pydantic import BaseModel, EmailStr

# Схемы для товаров
class ProductBase(BaseModel):
    name: str
    price: int
    image: str
    category: str = "standard"

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

# Схемы для пользователей
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserLogin):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    class Config:
        from_attributes = True