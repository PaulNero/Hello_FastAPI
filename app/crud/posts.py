from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.models import Post

async def create_post(session: AsyncSession, title: str, content: str, author_id: int) -> Post:
    new_post = Post(title=title, content=content, author_id=author_id)
    session.add(new_post)
    await session.commit() # Сохраняем изменения в БД, так как в настройка сессии, в database, прописали "expire_on_commit=False"
    await session.refresh(new_post) # Обновляем объект, что бы получить ID из БД
    return new_post

async def get_post_by_title(session: AsyncSession, title: str) -> Post | None:
    statement = select(Post).where(Post.title == title)
    result = await session.execute(statement)
    post = result.scalar_one_or_none() # Получить один объект или None
    return post

async def get_post_by_post_id(session: AsyncSession, post_id: int) -> Post | None:
    statement = select(Post).where(Post.id == post_id)
    result = await session.execute(statement)
    post = result.scalar_one_or_none() # Получить один объект или None
    return post

async def get_post_by_author_id(session: AsyncSession, author_id: int) -> List[Post]:
    statement = select(Post).where(Post.author_id == author_id)
    result = await session.execute(statement)
    posts = result.scalars().all()
    return posts

async def get_posts(session: AsyncSession) -> List[Post]:
    result = await session.execute(select(Post))
    posts = result.scalars().all()
    return posts
    

async def update_title(session: AsyncSession, post_id: int, new_title: str) -> Post | None:
    post = await session.get(Post, post_id) # .get() - Быстрый поиск по PK
    if post:
        post.title = new_title
        await session.commit()
    return post

async def delete_post(session: AsyncSession, post_id: int) -> Post | None:
    post = await session.get(Post, post_id)
    if post:
        await session.delete(post)
        await session.commit()
    return post