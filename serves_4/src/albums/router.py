from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from src.albums.schemas import AlbumsCreateScheme, AlbumsDeleteScheme, PhotoScheme, PhotoDeleteScheme
from src.auth.services import user_db
from src.albums.services import album_db, photo_db


router = APIRouter(prefix="/albums", tags=["albums"])


@router.get('/')
def root():

    return f'root album'

@router.post('/create_albums', response_model = AlbumsCreateScheme)
def create_albums(data: AlbumsCreateScheme, 
                  current_user: dict = Depends(user_db.get_current_user_from_token)):
    
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
def delete_album(data: AlbumsDeleteScheme, 
                current_user: dict = Depends(user_db.get_current_user_from_token)):
    
    album = album_db.delete_user_album(user_id = current_user['id'], id= data.id)
    return f'Альбом успешно удален {album}'

@router.post('/{album_id}/photos', response_model=PhotoScheme)
def add_photo(albums_id: int, 
              current_user: dict = Depends(user_db.get_current_user_from_token), 
              file: UploadFile = File(...)):
    
    photo = photo_db.upload_photo(user_id=current_user['id'], album_id=albums_id, file = file)
    return photo

@router.delete('/delete_photos', response_model=PhotoDeleteScheme)
def delete_photo(data: PhotoDeleteScheme,
                 current_user: dict = Depends(user_db.get_current_user_from_token)):
    photo_db.delete_photo(photo_id=data.id, user_id=current_user['id'])
    return f'Фото с id {data.id} удалено'


@router.get('/get_photos_alum')
def get_photos_alum(album_id: int, 
                    current_user: dict = Depends(user_db.get_current_user_from_token)):
    photos = photo_db.get_album_photo(album_id=album_id, user_id=current_user['id'])
    return photos

@router.get('/photos/{photo_id}/file')
def get_photo_file(photo_id: int, current_user: dict = Depends(user_db.get_current_user_from_token)):
    photo = photo_db.get_photo(photo_id=photo_id, user_id=current_user['id'])
    
    return FileResponse(
        path=photo.file_path,
        media_type=photo.content_type,
        filename=photo.filename
    )