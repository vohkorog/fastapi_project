from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from task import Task, TaskUpdate, read_file, write_file, get_max_id
import uvicorn
from typing import Optional


app = FastAPI()

data = read_file('data.json')

@app.get("/")
def root():
    return RedirectResponse("/tasks")

@app.get("/tasks")
def all_tasks():
    return JSONResponse(content=data) 


@app.delete('/delete/{id}')
def del_obj(id: int ):
    index_to_delite = None
    global data
    for i, task in enumerate(data):
        if task.get('id') == id:
            index_to_delite = i
            break

    if index_to_delite is None:
        raise HTTPException(status_code=404, detail=f"Объект с id={id} не найден")
        
    delite_task = data.pop(index_to_delite)
    write_file('data.json',data)
    
    return {
        "message": f"Объект с id={id} успешно удалён",
        "deleted_task": delite_task
    }



@app.post("/post")
def post(
        description: str = Body(...),
        status: str = Body(...),
        create_date: str = Body(...),
        clouse_date: Optional[str] = Body(None)):

    global data

    max_id = get_max_id(data)

    new_id = max_id + 1
    new_task = Task(
                    id = new_id, 
                    description=description, 
                    status=status,
                    create_date=create_date,
                    clouse_date=clouse_date )

    data.append(new_task.task_json())

    write_file('data.json',data) 

    return JSONResponse(content=new_task.task_json())
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)