import sys
import os

# Добавляем родительскую папку (serves_4) в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from models.user import Base, UserModel
from core.database import engine, session_factory
from sqlalchemy import insert, text, select
from datetime import datetime
from core.security import get_password_hash, verify_password, create_access_token, decode_token


def create_model():
    Base.metadata.create_all(engine)

def delete_model():
    Base.metadata.drop_all(engine)

def register_user(login: str, email: str, password: str) -> UserModel:
    hashed_password = get_password_hash(password)
    user = UserModel(email = email,
                login = login,
                password_hash = hashed_password)
    
    with session_factory() as session:
        session.add_all([user])
        session.commit()
        session.refresh(user)
        return user

def get_user_by_login(login: str):
    with session_factory() as session:
        return session.query(UserModel).filter(UserModel.login == login).first()

def authenticate_user(login: str, password: str) -> UserModel | None:
    user = get_user_by_login(login)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def login_user(login: str, password: str):
    user = authenticate_user(login, password)
    if not user:
        return {"success": False, "message": "Неверное имя пользователя или пароль"}
    if user.mark == 'No active':
        return {"success": False, "message": "Пользователь с такими данными удален"}
    
    token_data = {"sub": str(user.id), "login": user.login}
    access_token = create_access_token(token_data)
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "login": user.login
    }

def verify_token(token: str):
    payload = decode_token(token)
    if not payload:
        return {"success": False, "message": "Невалидный или просроченный токен"}
    
    user_id = payload.get("sub")
    if not user_id:
        return {"success": False, "message": "Невалидный токен"}
    
    with session_factory() as session:
        user = session.query(UserModel).filter(UserModel.id == int(user_id)).first()

        if not user:
            return {"success": False, "message": "Пользователь не найден"}
        
        return {
            "success": True,
            "user_id": user.id,
            "login": user.login,
            "email": user.email
        }

def get_current_user_from_token(token: str):

    result = verify_token(token)
    if not result["success"]:
        return None
    with session_factory() as session:
        user = session.query(UserModel).filter(UserModel.id == result["user_id"]).first()

        return user

def delete_acc_by_id(id: int):
    with session_factory() as session:
        user = session.get(UserModel, id)
        session.delete(user)
        session.commit()
        return user
    

def delete_acc_by_token(token: str):
    verify_user_token = verify_token(token)

    if not verify_user_token:
        print('Проблемы с удалением аккаунта')
    else:
        with session_factory() as session:
            user = session.query(UserModel).filter(UserModel.id == verify_user_token["user_id"]).first()
            session.delete(user)
            session.commit()
            return user
        
def cahnge_mark(token: str):
    verify_user_token = verify_token(token)
    if not verify_user_token:
        print('Проблемы с удалением аккаунта')
    else:
        with session_factory() as session:
            user = session.query(UserModel).filter(UserModel.id == verify_user_token["user_id"]).first()  
            result = session.get(UserModel, user.id)
            result.mark = 'No active'
            session.commit()
            return result


if __name__ == '__main__':
    
    ...

