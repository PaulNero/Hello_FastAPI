from pydantic import BaseModel, SecretStr, model_validator, EmailStr
from typing import List
from typing_extensions import Self
from fastapi.security import OAuth2PasswordBearer
from datetime import date

from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

class Item(BaseModel):
    id: int
    name: str
    is_availabel: bool = False # по умолчанию False
    price: float
    description: Optional[str] = None #Опциональное поле 
    
class UserIn(BaseModel):
    username: str
    email: EmailStr
    
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    
    class Config:
        from_attributes = True
    
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    roles: List[str]
    password: SecretStr
    # password_repeat: SecretStr
    
    # @model_validator(mode='after')
    # def validate(self) -> Self:
    #     if self.password != self.password_repeat:
    #         raise ValueError('Password do not match')
    #     return self
    
fake_db = [
    User(id=1, username='user1', email='email1@test.ru', roles=['admin', 'user'], password='password'),
    User(id=2, username='user2', email='email1@test.ru', roles=['user'], password='password')
]

users = {
    1: {'id': 1, 'username': "test 1", 'email': 'test1@test.test', "password": "hash1"},
    2: {'id': 2, 'username': "test 2", 'email': 'test2@test.test', "password": "hash2"},
    3: {'id': 3, 'username': "test 3", 'email': 'test3@test.test', "password": "hash3"}
}

class PostIn(BaseModel):
    title: str
    content: str
    author_id: int
    
class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    publish_date: date
    
    class Config:
        from_attributes = True