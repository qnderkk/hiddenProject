import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import auth, products, orders, contact
from app.config import settings
from contextlib import asynccontextmanager
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем папку static/images, если её нет
    base_static = os.path.abspath(settings.static_dir) # это "static"
    img_path = os.path.join(base_static, "images")
    os.makedirs(img_path, exist_ok=True)

    await init_db()
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Разрешаем вашему фронтенду на 8081
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# МОНТИРУЕМ ПРАВИЛЬНО:
# Теперь файл на диске "static/images/1.jpg"
# будет доступен как "http://127.0.0.1:8000/static/images/1.jpg"
app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(contact.router)

@app.get("/")
async def root():
    return {"message": "API is running"}