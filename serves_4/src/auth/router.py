import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends
from src.auth.services import user_db
from fastapi.responses import JSONResponse, RedirectResponse
from src.auth.schemas import UserLoginScheme, UserCreateScheme

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post('/login', summary='Логирование пользователя')
def login(data: UserLoginScheme):
    user = user_db.login_user(
        login= data.username,
        password= data.password
    )
    return user

@router.post('/signin', summary='Регистрация пользователя')
def sigin(data: UserCreateScheme):
    user = user_db.register_user(
        login= data.username,
        email=data.email,
        password=data.password
    )    
    return f'Здравствуйте, {user.login}'

@router.post('/change_pass')
def change_pass(new_pass:str, old_pass:str, current_user: dict = Depends(user_db.get_current_user_from_token)):
    
    change = user_db.change_pass(user_login=current_user['login'] ,new_password=new_pass, old_password=old_pass, user_id=current_user['id'])
    return change
