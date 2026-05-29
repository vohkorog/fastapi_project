from func import insert_data_model, select_all_data_model, update_data_model, delete_data_model
from fastapi import FastAPI, Depends
import uvicorn
from typing import Annotated
from database.DataBase import get_session
from sqlalchemy.orm import Session
from Schemas import TaskDeleteSchemas, TaskInsertSchemas, TaskUpdateSchema

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_session)]

@app.get('/')
def root():
    tasks = select_all_data_model()
    return tasks

@app.post('/insert')
def insert_data_schemas(data: TaskInsertSchemas): 
    task = insert_data_model(
        description=data.description,
        status= data.status,
        exec_at= data.exec_at
    )
    return task

@app.patch('/update')
def update_data_schemas(data: TaskUpdateSchema):
    task = update_data_model(
        id=data.id,
        desc=data.description,  
        status=data.status,      
        exec_at=data.exec_at     
    )
    return task


@app.delete('/delete')
def delete_data_schemas(data: TaskDeleteSchemas):
    task = delete_data_model(id= data.id)
    return task
 
if __name__ == '__main__':
    uvicorn.run('main:app', host= '127.0.0.1', port= 8000, reload= True)
   