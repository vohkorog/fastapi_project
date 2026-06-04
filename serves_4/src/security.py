# auth.py (новая версия без passlib)
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from dotenv import load_dotenv
from src.config import config

load_dotenv()

def get_password_hash(password: str) -> str:
    """
    Хэширует пароль с помощью bcrypt напрямую
    """
    # Конвертируем пароль в байты
    password_bytes = password.encode('utf-8')
    
    # Генерируем соль и хэшируем пароль
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Возвращаем как строку (декодируем из байтов)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:

    # Конвертируем в байты
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # Проверяем
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создает JWT токен"""
    to_encode = data.copy()
    
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        config.JWT_SECRETS, 
        algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token, 
            config.JWT_SECRETS, 
            algorithms=[config.JWT_ALGORITHM]
        )
        return payload
    except jwt.InvalidTokenError as e:
        print(f"Ошибка валидации токена: {e}")
        return None