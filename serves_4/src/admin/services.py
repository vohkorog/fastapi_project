import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base, UserModel
from database import engine, session_factory
from ..security import verify_password, get_password_hash
from ..auth.services import user_db

class db:
    @staticmethod
    def create_model():
        Base.metadata.create_all(engine)

    @staticmethod
    def delete_model():
        Base.metadata.drop_all(engine)

class user:

    @staticmethod
    def change_pass(user_login:str, user_id: int, old_password: str, new_password: str):
        user = user_db.get_user_by_login(user_login)
        if not user:
            return f'Неверный логин'
        
        if not verify_password(old_password, user.password_hash):
            return 'Неверный пароль'
        else:
            with session_factory() as session:
                new_password_hash = get_password_hash(new_password)
                user = session.get(UserModel, user_id)
                user.password_hash = new_password_hash
                session.commit()
                return {"id" : user.id,
                        "login" : user.login,
                        "email": user.email}
