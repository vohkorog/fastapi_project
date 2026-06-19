
from src.models import AlbumModel, PhotoModel
from src.database import session_factory
from sqlalchemy import select
from fastapi import UploadFile, HTTPException
import uuid
import shutil
from pathlib import Path

# Папка для загрузки фото
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent  # на уровень выше
UPLOAD_DIR = BASE_DIR / "uploads" / "photos"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class photo_db:

    ALLOWED_TYPES = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp"}
    

    @staticmethod 
    def generate_filename(extension: str) -> str:
        return f"{uuid.uuid4()}{extension}"

    @staticmethod
    def upload_photo(user_id: int, album_id:int, file: UploadFile):
        album = album_db.get_album(user_id=user_id, album_id=album_id)
        
        if album is None:
            raise HTTPException(status_code=404, detail="Альбом не найден")
        
        if file.content_type not in photo_db.ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="Неверный тип файла")

        extension = photo_db.ALLOWED_TYPES[file.content_type]
        safe_filename = photo_db.generate_filename(extension)
        file_path = UPLOAD_DIR / safe_filename

        try:

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except OSError as e:
            raise HTTPException(status_code=500, detail='Не удалось сохранить файл')
        
        try:
            with session_factory() as session:
                photo = PhotoModel(
                    filename=safe_filename,
                    file_path=str(file_path),
                    file_size=file_path.stat().st_size,
                    content_type=file.content_type,
                    album_id=album.id
                )
                session.add(photo)
                session.commit()
                session.refresh(photo)
                return photo
        except Exception:
            file_path.unlink(missing_ok=True)  # откатываем файл с диска при ошибке БД
            raise

    @staticmethod
    def delete_photo(photo_id: int, user_id: int):
        photo = album_db.get_photo(photo_id =photo_id, user_id=user_id)
        # Удаляем файл
        photo_path = Path(photo.file_path)
        if photo_path.exists():
            photo_path.unlink()
        with session_factory() as session:        
            session.delete(photo)
            session.commit()

    @staticmethod
    def get_photo(photo_id: int, user_id: int):
        with session_factory() as session:
            # Получаем фото с проверкой прав через альбом
            query = select(PhotoModel).join(AlbumModel).where(
                PhotoModel.id == photo_id,
                AlbumModel.user_id == user_id
            )
            result = session.execute(query)
            photo = result.scalar_one_or_none()
            if photo is None:
                raise HTTPException(status_code=404, detail="Фото не найдено")
            return photo
        
    @staticmethod
    def get_album_photo(album_id: int, user_id: int):
        album = album_db.get_album(album_id=album_id, user_id=user_id)
        if album is None:
            raise HTTPException(status_code=404, detail="Альбом не найден")

        with session_factory() as session:
            query = select(PhotoModel).where(PhotoModel.album_id == album_id)
            photos = session.execute(query).scalars().all()
            return photos



class album_db:
    
 
    @staticmethod
    def create_album(title: str,
                     user_id: int,  
                     description: str | None = None, 
                     ):

        album = AlbumModel(
        title = title, 
        description = description,
        user_id = user_id
        )
        with session_factory() as session:
            session.add_all([album])
            session.commit()
            session.refresh(album)
        return album
    
    @staticmethod
    def get_album(user_id: int, album_id: int):
        with session_factory() as session:
            query = select(AlbumModel).where(AlbumModel.id == album_id, AlbumModel.user_id == user_id)
            result = session.execute(query)
            album = result.scalar_one_or_none()
            return album
    
    @staticmethod
    def delete_user_album(user_id: int, id: int):
        album = album_db.get_album(user_id=user_id, album_id= id)
        
        if album is None:
            raise HTTPException(status_code=404, detail="Альбом не найден")
        
        with session_factory() as session:
            session.delete(album)
            session.commit()
            return album

    @staticmethod        
    def get_user_albums(user_id: int):
        
        with session_factory() as session:
            query = (select(AlbumModel).where(AlbumModel.user_id == user_id))
            result = session.execute(query)
            album = result.scalars().all()
            return album
        
   