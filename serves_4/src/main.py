
import sys
import os
# Добавляем родительскую папку (serves_4) в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from src.albums.router import router as router_albums
from src.auth.router import router as router_auth
from database import db
import uvicorn


app = FastAPI()

app.include_router(router_albums)
app.include_router(router_auth)

@app.get('/')
def root():
    return {
        "message": "Photo Album API",
        "docs": "/docs",
        "endpoints": 
            {
            "auth": "/api/v1/auth",
            "albums": "/api/v1/albums"
            }
    }

@app.post('/drop_all', description='drop and recreate all table')
def drop_all():
    db.delete_model()
    db.create_model()

    return f'Таблицы пересозданы'

if __name__ == "__main__":
    uvicorn.run('main:app', host = '127.0.0.1', port=8000, reload=True)