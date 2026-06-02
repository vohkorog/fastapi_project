from datetime import datetime
from typing import Dict
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

users_db: Dict[int, UserScheme] = {}
users_by_username: Dict[str, UserScheme] = {}
users_by_email: Dict[str, UserScheme] = {}