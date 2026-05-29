from database.Models import Base, TaskModel
from database.DataBase import engine, session_factory
from sqlalchemy import insert, text, select
from datetime import datetime


def create_model():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def delete_model():
    Base.metadata.drop_all(engine)



if __name__ == '__main__':
    create_model()
