from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)
    
    user = await service.register_user(user_data)
    if not user:
        raise HTTPException(status_code=400, detail="Email уже занят")
    return user

@router.post("/login")
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)
    
    user = await service.authenticate_user(login_data)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    token = service.create_access_token({"sub": str(user.id)})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "name": user.name,
        "email": user.email,
        "is_admin": user.is_admin
    }