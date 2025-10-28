from jose import JWTError, jwt
from fastapi import Depends
from http.client import HTTPException
from starlette import status
from datetime import datetime, timedelta, timezone
from .schemas.schemas import oauth2_scheme
from dotenv import load_dotenv
import os

load_dotenv()

# Настройки
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60)

# Функции

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
    
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        header={'WWW-Authenticate': 'Bearer'},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get('sub')
    if username is None:
        raise credentials_exception
    return {'username': username} # Возвращаем данные пользователя из токена