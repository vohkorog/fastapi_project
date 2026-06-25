import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Depends
from src.admin.services import db, user
from src.auth.services import user_db

router = APIRouter(prefix='/admin', tags = ['DEBUG'])

@router.post('/drop_all', summary='Пересоздание БД')
def drop_all():
    """Пересоздание БД с удалением старых записей"""
    db.delete_model()
    db.create_model()
    return f'Таблицы пересозданы'

@router.get('/all_users', summary='Вывод всех пользователей')
def all_users():
    """Вывод всех пользователей"""
    users = user_db.get_all_users()
    return users


@router.post('/change_pass')
def change_pass(new_pass:str, old_pass:str, current_user: dict = Depends(user_db.get_current_user_from_token)):
    
    change = user.change_pass(user_login=current_user['login'] ,new_password=new_pass, old_password=old_pass, user_id=current_user['id'])
    return change
