from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.models import User

async def create_user(session: AsyncSession, username: str, email: str) -> User:
    new_user = User(username=username, email=email)
    session.add(new_user)
    await session.commit() # Сохраняем изменения в БД, так как в настройка сессии, в database, прописали "expire_on_commit=False"
    await session.refresh(new_user) # Обновляем объект, что бы получить ID из БД
    return new_user

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    result = await session.execute(statement)
    user = result.scalar_one_or_none() # Получить один объект или None
    return user

async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none() # Получить один объект или None
    return user

async def get_user_by_id(session: AsyncSession, id: int) -> User | None:
    statement = select(User).where(User.id == id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none() # Получить один объект или None
    return user

async def get_users(session: AsyncSession) -> List[User]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users
    

async def update_username(session: AsyncSession, user_id: int, new_username: str) -> User | None:
    user = await session.get(User, user_id) # .get() - Быстрый поиск по PK
    if user:
        user.username = new_username
        await session.commit()
    return user

async def delete_user(session: AsyncSession, user_id: int) -> User | None:
    user = await session.get(User, user_id)
    if user:
        await session.delete(user)
        await session.commit()
    return user