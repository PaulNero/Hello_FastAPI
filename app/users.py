from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .schemas.schemas import User, oauth2_scheme
from .auth import get_current_user


router = APIRouter() 

users = {
    1: {'id': 1, 'username': "test 1", 'email': 'test1@test.test', "password": "hash1"},
    2: {'id': 2, 'username': "test 2", 'email': 'test2@test.test', "password": "hash2"},
    3: {'id': 3, 'username': "test 3", 'email': 'test3@test.test', "password": "hash3"}
}

@router.post('/users/me')
async def read_users_me(user: User=Depends(get_current_user)):
    return {'token': token}

@router.post('/users')
async def create_user(user: User):
    return {'username': user.username, "email": user.email}

@router.get('/users', 
            response_model=List[User], 
            summary='Просмотр информации о пользователе')

def get_users():
    return [User(**user) for user in users.values()]
    # return [
    #     {u: user[u] for u in ('id', "username", "email", "password")}
    #         for user in users.values()
    #         ]

@router.get('/users/{user_id}', 
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