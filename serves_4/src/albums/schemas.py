
from pydantic import BaseModel
from datetime import datetime

class AlbumsCreateScheme(BaseModel):
    title: str
    description: str | None = None

class AlbumsDeleteScheme(BaseModel):
    id: int

class PhotoScheme(BaseModel):
    id: int
    album_id: int
    uploaded_at: datetime
    filename: str
    file_path: str
    file_size: int
    content_type: str
    
    class Config:
        from_attributes = True


class PhotoDeleteScheme(BaseModel):
    id: int 

