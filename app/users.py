from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter() 

users = {
    1: {'id': 1, 'username': "test 1", 'email': 'test1@test.test', "password": "hash1"},
    2: {'id': 2, 'username': "test 2", 'email': 'test2@test.test', "password": "hash2"},
    3: {'id': 3, 'username': "test 3", 'email': 'test3@test.test', "password": "hash3"}
}

# Pydantic модель для ответа 
class UserOut(BaseModel):
    id: int
    username: str
    email: str | None = None
    password: str | None = None

@router.get('/users', 
            response_model=List[UserOut], 
            summary='Просмотр информации о пользователе')
def get_users():
    return [UserOut(**user) for user in users.values()]
    # return [
    #     {u: user[u] for u in ('id', "username", "email", "password")}
    #         for user in users.values()
    #         ]

@router.get('/users/{user_id}', 
            response_model=UserOut,
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