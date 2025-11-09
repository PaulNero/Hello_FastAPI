from typing import Any

from jose import JWTError, jwt
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from http.client import HTTPException
from starlette import status
from datetime import datetime, timedelta, timezone
from ..schemas.users import oauth2_scheme, User, fake_db

from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter() 

# Настройки
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60))

# Функции


router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
        )
    access_token = create_access_token(
        data={'sub': user.username, 'roles': [ user.roles]}
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

    
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    creds_ex = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    payload = decode_token(token)
    if payload is None:
        raise creds_ex
    user = next(filter(lambda u: u.username == payload['sub'], fake_db))[0]
    # if user.password != payload['password']:
    #     raise creds_ex
        
    return user
    # username: str = payload.get('sub')
    # if username is None:
    #     raise credentials_exception
    # return {'username': username} # Возвращаем данные пользователя из токена
    
    def authenticate_user(username: str, password: str):
        for user in fake_db:
            if user.username == username and user.password == password:
                return user
            
            
def authenticate_user(username: str, password: str) -> User:
    for user in fake_db:
        if user.username == username and user.password == password:
            return user
    return None

def require_role(required_role: str):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        roles = current_user.get("roles", [])
        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detatil="You do not have permission to access this resource"
            )
        return current_user
    return Depends(role_checker)