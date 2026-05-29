import uvicorn
from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    age: Optional[int] = None

id = 0
list: List[User] = []

@app.get('/')
def root():
    result = []
    id = 1 
    for user in list:
        result.append(f'id = {user.id} name = {user.name} age = {user.age}')
        id += 1
    return result

@app.post('/post')
def post(user_add: User):
    global id
    id += 1
    user = User(id=id ,name=user_add.name, age=user_add.age)
   
    list.append(user)
    return f'id = {id}, name = {user.name}, age = {user.age}'

@app.get('/{id}')
def search_id(id: int):
    for i in list:
        if i.id == id:
            return  i
        
@app.post('/{id}')
def delete_id(id: int):
    global list
    delite_item = list.pop(id-1)      
    return f'{delite_item}'

@app.patch('/{id}')
def update_fields(id: int, user_update: User):
    user =  list[id-1]
    
    if user_update is not None:
        user.name = user_update.name
    if user_update is not None:
        user.age = user_update.age
    return user


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host = '127.0.0.1', reload=True)