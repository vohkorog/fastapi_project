
from pydantic import BaseModel
from datetime import datetime

class AlbumsCreateScheme(BaseModel):
    title: str
    description: str | None = None


class AlbumChangingScheme(BaseModel):
    id: int
    title: str | None = None
    description: str | None = None


class GetAlbums(BaseModel):
    id: int
    title: str 
    description: str | None = None
    create_at: datetime
    user_id: int

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
    album_id: int

