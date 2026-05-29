from pydantic import BaseModel
from datetime import datetime

class TaskUpdateSchema(BaseModel):
    id: int
    description: str | None = None
    status: str | None = None
    exec_at: datetime | None = None

class TaskInsertSchemas(BaseModel):
    description: str | None = None
    status: str | None = None
    exec_at: datetime | None = None

class TaskDeleteSchemas(BaseModel):
    id: int