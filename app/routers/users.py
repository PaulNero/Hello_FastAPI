from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import DBSession
from sqlalchemy.exc import IntegrityError
from app.db.users import UserIn
from app.crud import users
from app.crud.posts import get_post_by_author_id

router = APIRouter()

@router.get('/users/')
async def get_users(session: DBSession):
    # В 'session' теперь находится готовая к работе асинхронная сессии
    return await users.get_users(session)

@router.post('/users/', response_model=UserIn)
async def create_user(user: UserIn, session: DBSession):
    try:
        user = await users.create_user(session, user.username, user.email)
        return user
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f'Email already exists, ERROR: {e}')
    
@router.get('/users/email={email}')
async def get_user_by_email(email: str, session: DBSession):
    user = await users.get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router.get('/users/username={username}')
async def get_user_by_username(username: str, session: DBSession):
    user = await users.get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router.get('/users/{author_id}/posts')
async def get_user_by_author_id(author_id: int, session: DBSession):
    user = await users.get_user_by_id(session, author_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    posts = await get_post_by_author_id(session, author_id)
    if not posts:
        raise HTTPException(status_code=404, detail='Posts not found')
    return posts