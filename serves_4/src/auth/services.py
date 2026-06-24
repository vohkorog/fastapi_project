import sys
import os

# Добавляем родительскую папку (serves_4) в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.models import Base, UserModel
from src.database import engine, session_factory
from src.security import get_password_hash, verify_password, create_access_token, decode_token
from sqlalchemy import select


security = HTTPBearer()


class user_db:

    @staticmethod
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
    
    @staticmethod
    def get_user_by_login(login: str):
        with session_factory() as session:
            return session.query(UserModel).filter(UserModel.login == login).first()
    
    
    @staticmethod
    def authenticate_user(login: str, password: str) -> UserModel | None:
        user = user_db.get_user_by_login(login)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    
    
    @staticmethod
    def login_user(login: str, password: str):
        user = user_db.authenticate_user(login, password)
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
    
    
    @staticmethod
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
    
    @staticmethod
    def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials  # Токен из заголовка Authorization
        
        result = user_db.verify_token(token)
        if not result["success"]:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        with session_factory() as session:
            user = session.query(UserModel).filter(UserModel.id == result["user_id"]).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {"id": user.id, "login": user.login}  

    @staticmethod
    def delete_acc_by_id(id: int):
        with session_factory() as session:
            user = session.get(UserModel, id)
            session.delete(user)
            session.commit()
            return user
            
    
    @staticmethod        
    def cahnge_mark(user_id: int):
        with session_factory() as session:
            result = session.get(UserModel, user_id)
            result.mark = 'No active'
            session.commit()
            return result
        
    @staticmethod
    def get_all_users():
        with session_factory() as session:
            users = session.execute(select(UserModel)).scalars().all()
            if not users:
                return f'Пользователей нет'
            else:
                return users