import sys
import os

# Добавляем родительскую папку (serves_4) в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.models import Base, UserModel
from src.database import engine, session_factory
from src.security import get_password_hash, verify_password, create_access_token, decode_token
from src.admin.services import admin

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
    def authenticate_user(login: str, password: str) -> UserModel | None:
        user = admin.get_user_by_login(login)
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
    def change_pass(user_login:str, user_id: int, old_password: str, new_password: str):
        user = user_db.authenticate_user(login=user_login, password= old_password)
        if not user:
            return f'Неверный логин'
        else:
            with session_factory() as session:
                new_password_hash = get_password_hash(new_password)
                user = session.get(UserModel, user_id)
                user.password_hash = new_password_hash
                session.commit()
                return {"id" : user.id,
                        "login" : user.login,
                        "email": user.email}

        
