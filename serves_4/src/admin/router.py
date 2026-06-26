import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Depends
from src.admin.services import db, admin

router = APIRouter(prefix='/admin', tags = ['DEBUG'])

@router.post('/drop_all', summary='Пересоздание БД')
def drop_all():
    """Пересоздание БД с удалением старых записей"""
    db.delete_model()
    db.create_model()
    return f'Таблицы пересозданы'

@router.get('/users/all_users', summary='Вывод всех пользователей')
def all_users():
    """Вывод всех пользователей"""
    users = admin.get_all_users()
    return users

@router.get('/users/{users_login}', summary= 'Получение пользователя по логину')
def get_user_by_login(users_login: str):
    user = admin.get_user_by_login(login=users_login)
    return user

@router.delete('/users/{users_id}', summary='Удалить пользователя по id')
def delete_acc_by_id(users_id: int):
    """Удаление аккаунта пользователя по id"""

    user = admin.delete_acc_by_id(id = users_id)
    return user