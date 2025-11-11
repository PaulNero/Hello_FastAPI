from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .app.db.users import User, oauth2_scheme, users
from .auth import get_current_user


router = APIRouter() 

@router.post('/a/users/me')
async def read_users_me(user: User=Depends(get_current_user)):
    return {'data': user}

@router.post('/a/users')
async def create_user(user: User):
    return {'username': user.username, "email": user.email}

@router.get('/a/users', 
            response_model=List[User], 
            summary='Просмотр информации о пользователе')

def get_users():
    return [User(**user) for user in users.values()]
    # return [
    #     {u: user[u] for u in ('id', "username", "email", "password")}
    #         for user in users.values()
    #         ]

@router.get('/a/users/{user_id}', 
            response_model=User,
            summary='Получение информации о пользователе')
def get_user(user_id: int):
    user = users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return {
        "id": user['id'],
        "username": user['username'],
        "email": user['email'],
        "password": user["password"]
    }