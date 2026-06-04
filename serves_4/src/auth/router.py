import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from fastapi import FastAPI, Cookie
from src.auth.services import db, user_db
from fastapi.responses import JSONResponse, RedirectResponse
from src.auth.schemas import UserLoginScheme

app = FastAPI()

@app.get('/')
def main_root():
    return f'root'

@app.post('/login')
def login(data: UserLoginScheme):
    user = user_db.login_user(
        login= data.username,
        password= data.password
    )

    response = RedirectResponse(url='/root')
    response.set_cookie(
        key="access_token",
        value=user["access_token"],
        httponly=True,  # Защита от XSS
        max_age=1800,   # 30 минут
        secure=False,   # True для HTTPS
        samesite="lax"
    )
    response.set_cookie(key="user_id", value=str(user["user_id"]))
    response.set_cookie(key="login", value=user["login"])
    
    return response
   

