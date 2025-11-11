from fastapi import FastAPI
from ..archive import _users, items, async_example, auth
from ..routers import users, posts
from .app.db.database import engine, Base
import logging

logger = logging.getLogger(__name__)

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

app.include_router(_users.router)
app.include_router(items.router)
app.include_router(async_example.router)
app.include_router(auth.router)

app.include_router(users.router)
app.include_router(posts.router)

@app.on_event("startup")
async def startup():
    # Отключено из за подключения алембика
    # async with engine.begin() as connect:
    #     await connect.run_sync(Base.metadata.create_all)
    # logger.info("Все таблицы созданы (или уже существовали)")
    pass


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose() # Отключение движка БД
    logger.info("Приложение успешно потушено")

# Определяем эндпоинт для GET запроса по корневому URL
@app.get("/",
        summary='Корневой URL')
def read_root():
    return {'message': 'Добро пожаловать в FastAPI'}
