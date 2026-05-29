from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
import json
from typing import Optional



class Task(BaseModel):
        id: int = None
        description: str = Field(..., min_length=1)
        status: str = 'Новая'
        create_date: date = Field(default_factory=datetime.now)
        clouse_date: Optional[date] = None
        

        @field_validator('create_date', 'clouse_date', mode='before')
        @classmethod
        def parse_date(cls, v):
            if v is None:
                return v
            if isinstance(v, str):
                for fmt in ('%d-%m-%Y', '%Y-%m-%d', '%d.%m.%Y'):
                    return datetime.strptime(v, fmt).date()
            return v


        def get_date(self):
            return self.create_date.strftime("%d.%m.%Y")
        
        def get_time(self):   
            return self.create_date.strftime("%H:%M:%S")

        def task_json(self):
            
            task = {
                "id": self.id,
                "description": self.description,
                "status": self.status,
                "create_date": self.create_date.strftime("%d-%m-%Y") if self.create_date else None,
                "clouse_date": self.clouse_date.strftime("%d-%m-%Y") if self.clouse_date else None
            }
            
            return task


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    create_date: Optional[date] = None
    clouse_date: Optional[date] = None



def read_file(path_file: str):
    with open(path_file, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def write_file(path_file: str, data):
    with open(path_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def get_max_id(data):
    _id = 0
    
    for book in data:
        current_id = book.get('id', 0)
        if _id < current_id:
            _id = current_id
    return _id