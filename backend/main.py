from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database
import bcrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.get("/products")
def get_products(db: Session = Depends(database.get_db)):
    return db.query(models.Product).all()

@app.post("/products")
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    new_prod = models.Product(**product.dict())
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)
    return new_prod

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    db_item = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Товар не найден")
    db.delete(db_item)
    db.commit()
    return {"message": "Удалено"}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные данные")
    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "is_admin": db_user.is_admin
    }

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email занят")
    new_user = models.User(name=user.name, email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "OK"}