
import sys
import os
# Добавляем родительскую папку (serves_4) в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.auth.services import db, user_db

if __name__ == "__main__":
    db.create_model()