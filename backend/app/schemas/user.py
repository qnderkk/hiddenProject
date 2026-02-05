from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100,
                      description="Name of the user")
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=1, max_length=100,
                          description="User's password")


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=100,
                          description="User's password")


class UserResponse(UserBase):
    id: int = Field(..., description="Unique user identifier")
    is_admin: bool = False

    class Config:
        from_attributes = True
