from fastapi import APIRouter, Depends
from src.albums.schemas import AlbumsCreateScheme, AlbumsDeleteScheme
from src.auth.services import user_db
from src.albums.services import album_db


router = APIRouter(prefix="/albums", tags=["albums"])


@router.get('/')
def root():
    return f'root album'

@router.post('/create_albums')
def create_albums(data: AlbumsCreateScheme, current_user: dict = Depends(user_db.get_current_user_from_token)):
    album = album_db.create_album(
        title = data.title,
        description= data.description,
        user_id=current_user['id']
    )
    return album

@router.get('/get_albums')
def get_albums(current_user: dict = Depends(user_db.get_current_user_from_token)):
    try:
        albums = list(album_db.get_user_albums(current_user['id']))
        return albums
    except:
        return f'неправельный токен'
    
@router.delete('/delete_album')
def delete_album(data: AlbumsDeleteScheme, current_user: dict = Depends(user_db.get_current_user_from_token)):
    album = album_db.delete_user_album(user_id = current_user['id'], id= data.id)
    return f'Альбом успешно удален {album}'
