from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-very-secret-key"
ALGORITHM = "HS256"

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=24)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def register_user(self, user_data: UserCreate):
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            return None
        
        hashed_pwd = self.hash_password(user_data.password)
        
        return await self.user_repo.create(user_data, hashed_pwd)

    async def authenticate_user(self, login_data: UserLogin):
        user = await self.user_repo.get_by_email(login_data.email)
        if not user:
            return False
        
        if not self.verify_password(login_data.password, user.hashed_password):
            return False
        
        return user