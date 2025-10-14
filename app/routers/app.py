from fastapi import FastAPI
from .. import users, items 

# Создаём экземпляр FastAPI
app = FastAPI(
    title = "Моё первое API",
    description = "Это демонстрационный API на FastAPI",
    version = "0.0.1"
)

# Подключаемся в дальнейшем через Uvicorn
# на локалхосте
# Запуск uvicorn app.routes.app:app путь.название файла:название переменной
# Ключ --reload для автоматичексого перезапуска при внесении изменений
# /docs - для доступа к документации АПИ

app.include_router(users.router)
app.include_router(items.router)

# Определяем эндпоинт для GET запроса по корневому URL
@app.get("/",
        summary='Корневой URL')
def read_root():
    return {'message': 'Добро пожаловать в FastAPI'}