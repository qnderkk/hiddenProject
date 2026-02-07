# hiddenProject

Перед запуском проекта создать бд hidden_db и поменять DATABASE_URL в hiddenProject\backend\main на свои данные

## в директории hiddenProject\backend

bash: uvicorn main:app --reload

## в директории hiddenProject

bash: npm run serve

## бдшка

чтобы добавлять товары сначало надо создать категорию которой товары буду принадлежать
INSERT INTO categories (name) VALUES ('Общее');
это в общем случае.
