from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
name = os.getenv('POSTGRES_NAME')
port = os.getenv('POSTGRES_PORT')

# driver => engine => session maker => session

# URL подключения для PostgreSQL с драйвером asyncpg
DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

# Создаём асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True, future=True, pool_size=10, max_overflow=20)

# Фабрика для создания асинхронных сессий
# Сессия создаётся под каждый запрос и закрывается после выполнения запроса
Session = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncSession:
    async with Session() as session:
        yield session
        
DBSession = Annotated[AsyncSession, Depends(get_async_session)]
