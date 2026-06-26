import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base, UserModel
from database import engine, session_factory
from sqlalchemy import select

class db:
    @staticmethod
    def create_model():
        Base.metadata.create_all(engine)

    @staticmethod
    def delete_model():
        Base.metadata.drop_all(engine)

class admin:

    @staticmethod
    def get_user_by_login(login: str):
        with session_factory() as session:
            return session.query(UserModel).filter(UserModel.login == login).first()
            
    @staticmethod
    def get_all_users():
        with session_factory() as session:
            users = session.execute(select(UserModel)).scalars().all()
            if not users:
                return f'Пользователей нет'
            else:
                return users

    @staticmethod
    def delete_acc_by_id(id: int):
        with session_factory() as session:
            user = session.get(UserModel, id)
            if not user: 
                return f'Пользователь не найден'
            
            session.delete(user)
            session.commit()
            return {
                "message": "Пользователь успешно удален",
                "id" : "{id}"
            }