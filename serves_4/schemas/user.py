from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel, EmailStr

class User():
    id: int
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = datetime.now()
    refresh_token: str | None = None

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserInDB(User):
    pass

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str
    token_type: str  # "access" or "refresh"

users_db: Dict[int, User] = {}
users_by_username: Dict[str, User] = {}
users_by_email: Dict[str, User] = {}