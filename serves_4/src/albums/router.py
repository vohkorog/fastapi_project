from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from src.albums.schemas import AlbumsCreateScheme, PhotoScheme
from src.auth.services import user_db
from src.albums.services import album_db, photo_db


router = APIRouter(prefix="/albums", tags=["albums"])

#Альбомы 
@router.post('/', response_model = AlbumsCreateScheme, summary="Создание альбома")
def create_albums(data: AlbumsCreateScheme, 
                  current_user: dict = Depends(user_db.get_current_user_from_token)):
    
    """Создание альбома у пользователя"""
    album = album_db.create_album(
        title = data.title,
        description= data.description,
        user_id=current_user['id']
    )
    return album

@router.get('/', summary="Получение альбомов")
def get_albums(current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Поулчение всех альбомов пользователей у авторезированного пользователя"""
    try:
        albums = list(album_db.get_user_albums(current_user['id']))
        return albums
    except:
        return f'неправельный токен'
    
@router.delete('/{albums_id}', summary="Удаление альбома")
def delete_album(albums_id: int, 
                current_user: dict = Depends(user_db.get_current_user_from_token)):
    
    """Удаление альбома оп id у авторезированно пользователя"""
    album = album_db.delete_user_album(user_id = current_user['id'], id= albums_id)
    return f'Альбом {album.title} успешно удален'
#Фото
@router.post('/{album_id}/photos', response_model=PhotoScheme, summary="Добавление фото к альбому")
def add_photo(album_id: int, 
              current_user: dict = Depends(user_db.get_current_user_from_token), 
              file: UploadFile = File(...)):
    
    """Добавление по id альбома у авторезированного пользователя"""
    photo = photo_db.upload_photo(user_id=current_user['id'], album_id=album_id, file = file)
    return photo

@router.delete('/{albums_id}/photo/{photo_id}', summary="Удаление фото у альбома")
def delete_photo(albums_id: int,
                 photo_id:int,
                 current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Удаление фото по id у авторезированного пользователя"""
    photo_db.delete_photo(photo_id=photo_id, album_id=albums_id, user_id=current_user['id'])
    return f'Фото с id {photo_id} удалено'


@router.get('/{album_id}', summary="Получение метаданных всех фото у абльбома")
def get_photos_alum(album_id: int, 
                    current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Получение метаданных всех фото по id альбома у авторезированного пользователя"""
    photos = photo_db.get_album_photo(album_id=album_id, user_id=current_user['id'])
    return photos

@router.get('/{album_id}/photos/{photo_id}/file', summary="Получение изображение фото")
def get_photo_file(photo_id: int, album_id: int, current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Получение изображения фото по id у авторезированного пользователя"""
    photo = photo_db.get_photo(photo_id=photo_id, album_id=album_id, user_id=current_user['id'])
    
    return FileResponse(
        path=photo.file_path,
        media_type=photo.content_type,
        filename=photo.filename
    )
@router.get('/share/{shared_album_id}', summary="Получение общего альбома")
def get_shared_albums(
    shared_album_id: int,
    current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Получение общего альбома по id у пользователя, с которым поделились альбомом"""
    album = album_db.get_shared_album(shared_album_id=shared_album_id, shared_user_id=current_user['id'])
    return album

@router.get('/share/', summary="Получение всех общих альбомов у пользователя")
def get_all_shared_albums(current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Получение всех общих альбомов пользователя"""
    albums = album_db.get_all_shared_album(shared_user_id=current_user['id'])
    return albums

@router.post('/{albums_id}/share', summary="Поделиться альбомом")
def set_share_album(shared_user_id: int, 
                albums_id: int, 
                current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Поделится альбомом с другим пользователем по id альбома и id пользователя"""
    album_db.shared_album(shared_album_id=albums_id, shared_user_id=shared_user_id, ownre_id=current_user['id'])
    return f'Альбом с id - {albums_id} для пользователя {shared_user_id} успешно присвоен'

