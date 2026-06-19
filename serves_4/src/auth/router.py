import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from src.auth.services import user_db
from fastapi.responses import JSONResponse, RedirectResponse
from src.auth.schemas import UserLoginScheme, UserCreateScheme

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get('/')
def main_root():
    return f'auth root'


@router.post('/login')
def login(data: UserLoginScheme):
    user = user_db.login_user(
        login= data.username,
        password= data.password
    )

    return user

@router.post('/signin')
def sigin(data: UserCreateScheme):
    user = user_db.register_user(
        login= data.username,
        email=data.email,
        password=data.password
    )    
    return f'Здравствуйте, {user.login}'


    
   

