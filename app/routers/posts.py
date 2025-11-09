from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.database import DBSession
from sqlalchemy.exc import IntegrityError
from app.schemas.posts import PostIn
from app.crud import posts

router = APIRouter()

@router.get('/posts/')
async def get_posts(session: DBSession):
    # В 'session' теперь находится готовая к работе асинхронная сессии
    return await posts.get_posts(session)

@router.post('/posts/', response_model=PostIn)
async def create_post(post: PostIn, session: DBSession):
    post = await posts.create_post(session, post.title, post.content, post.author_id)
    return post
    
@router.get('/posts/title={title}')
async def get_post_by_title(title: str, session: DBSession):
    post = await posts.get_post_by_title(session, title)
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    return post

@router.get('/posts/post_id={post_id}')
async def get_user_by_post_id(post_id: int, session: DBSession):
    post = await posts.get_post_by_post_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail='Post not found')
    return post
