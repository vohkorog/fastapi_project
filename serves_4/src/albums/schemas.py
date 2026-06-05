
from pydantic import BaseModel

class AlbumsCreateScheme(BaseModel):
    title: str
    description: str | None = None

class AlbumsDeleteScheme(BaseModel):
    id: int
