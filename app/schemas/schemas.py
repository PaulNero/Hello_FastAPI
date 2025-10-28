from pydantic import BaseModel, SecretStr, model_validator
from typing import List
from typing_extensions import Self
from fastapi.security import OAuth2PasswordBearer

from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

class Item(BaseModel):
    id: int
    name: str
    is_availabel: bool = False # по умолчанию False
    price: float
    description: Optional[str] = None #Опциональное поле 
    
    
class User(BaseModel):
    id: int
    username: str
    email: str | None = None
    roles: List[str]
    password: SecretStr
    password_repeat: SecretStr
    
    @model_validator(mode='after')
    def validate(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Password do not match')
        return self