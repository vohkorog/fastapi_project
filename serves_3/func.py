from database.Models import Base, TaskModel
from database.DataBase import engine, session_factory
from sqlalchemy import insert, text, select
from datetime import datetime

def create_model():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def delete_model():
    Base.metadata.drop_all(engine)

"""
# императивный стиль 
def insert_val():
    with engine.connect() as conn:
        stmt = insert(task_table).values(
            [
                {
                    "status" : "133"
                },
                {
                    "status" : "233"
                }
            ]
        )
        conn.execute(stmt)
        conn.commit()
"""

# дкларативный стиль
def insert_data_model(description: str, status: str, exec_at: datetime | None = None):

    task = TaskModel(
        description = description,
        status = status,
        exec_at = exec_at)
    
    with session_factory() as session:
        session.add_all([task])
        session.commit()
        session.refresh(task)
        return task

def select_all_data_model():
    
    with session_factory() as session:
        query = (select(TaskModel))
        result = session.execute(query)
        tasks = result.scalars().all()        
        return tasks
    
def update_data_model(id: int, 
                      desc: str| None = None, 
                      status: str| None = None, 
                      exec_at: datetime | None = None):
    
    with session_factory() as session:
        task = session.get(TaskModel, id)

        if status is not None:
            task.status = status

        if desc is not None:
            task.description = desc
        
        if exec_at is not None:
            task.exec_at = exec_at
        
        session.commit()
        return task

def delete_data_model(id: int):

    with session_factory() as session:
        task = session.get(TaskModel, id)
        session.delete(task)
        session.commit()
        return task

""" if __name__ == '__main__':
    #update_data_model(6, desc = 'change desc 3 nananan')

    delete_data_model(10) """
