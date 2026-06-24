import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserScheme():
    id: int
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = datetime.now()
    refresh_token: str | None = None

class UserCreateScheme(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLoginScheme(BaseModel):
    username: str
    password: str

class UserInDBScheme(UserScheme):
    pass

class TokenScheme(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenDataScheme(BaseModel):
    username: str
    token_type: str  # "access" or "refresh"