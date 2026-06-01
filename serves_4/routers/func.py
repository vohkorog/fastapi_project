import sys
import os

# Добавляем родительскую папку (serves_4) в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from models.user import Base, User
from core.database import engine, session_factory
from sqlalchemy import insert, text, select
from datetime import datetime
from auth import get_password_hash
from pydantic import EmailStr

def create_model():
    Base.metadata.create_all(engine)

def delete_model():
    Base.metadata.drop_all(engine)

def create_user(username: str, email: str, password: str):
    hashed_password = get_password_hash(password)
    user = User(email = email,
                name = username,
                password_hash = hashed_password)
    
    with session_factory() as session:
        session.add_all([user])
        session.commit()
        session.refresh(user)
        return user

        
if __name__ == '__main__':
    create_user(username='kirill', email='asdsad@yandex.ru', password='admin123')
