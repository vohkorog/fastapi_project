import sys
from src.models import AlbumModel, PhotoModel, MemberModel, UserModel
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
    def delete_photo(photo_id: int, album_id, user_id: int):
        photo = photo_db.get_photo(photo_id =photo_id, album_id=album_id, user_id=user_id)
        # Удаляем файл
        photo_path = Path(photo.file_path)
        if photo_path.exists():
            photo_path.unlink()
        with session_factory() as session:        
            session.delete(photo)
            session.commit()

    @staticmethod
    def get_photo(photo_id: int, album_id:int, user_id: int):
        album = album_db.get_album(album_id=album_id, user_id=user_id)
        if album is None:
            raise HTTPException(status_code=404, detail="Альбом не найден")
        else:
            with session_factory() as session:
                # Получаем фото с проверкой прав через альбом
                photo = session.execute(select(PhotoModel).where(
                    PhotoModel.id == photo_id,
                )).scalar_one_or_none()
                if photo is None:
                    raise HTTPException(status_code=404, detail="Фото не найдено")
                else: 
                    return photo


    @staticmethod
    def get_album_photo(album_id: int, user_id: int):
        album = album_db.get_album(album_id=album_id, user_id=user_id)
        if album is None:
            raise HTTPException(status_code=404, detail="Альбом не найден")

        with session_factory() as session:
            photos = session.execute(select(PhotoModel).where(PhotoModel.album_id == album_id)).scalars().all()
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
            album = session.execute(
                select(AlbumModel).where(
                    AlbumModel.id == album_id, AlbumModel.user_id == user_id))
            
            if album:
                return session.get(AlbumModel, album_id)
            else: None

            member = session.execute(
            select(MemberModel).where(
                MemberModel.album_id == album_id,
                MemberModel.user_id == user_id
                )).scalar_one_or_none()
        
            if member:
                return session.get(AlbumModel, album_id)   
            return None
            
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
            album = session.execute(select(AlbumModel).where(AlbumModel.user_id == user_id)).scalars().all()
            return album
        
    @staticmethod
    def shared_album(shared_album_id: int, shared_user_id: int, ownre_id: int):
        album = album_db.get_album(user_id=ownre_id, album_id= shared_album_id)

        if album is None:
            raise HTTPException(status_code=404, detail="Альбом не найден")
        
        with session_factory() as session:
            existing = session.execute(
            select(MemberModel).where(
                MemberModel.album_id == shared_album_id,
                MemberModel.user_id == shared_user_id
                )).scalar_one_or_none()
        
            if existing:
                raise HTTPException(status_code=400, detail="Пользователь уже имеет доступ")
            
            member = MemberModel(
                user_id = shared_user_id,
                album_id = shared_album_id
            )

            session.add(member)
            session.commit()
            return member
        
    @staticmethod
    def get_shared_album(shared_album_id: int, shared_user_id: int):
        
        with session_factory() as session:
            members = session.execute(
            select(MemberModel).where(MemberModel.album_id == shared_album_id, MemberModel.user_id == shared_user_id)
        ).scalars().all()
            if members:
                albums = session.execute(select(AlbumModel).where(AlbumModel.id == shared_album_id)).scalar_one_or_none()
                return albums
            else: raise HTTPException(status_code=404, detail="Пользователь не имеет доступ к альбому")

    @staticmethod
    def get_all_shared_album(shared_user_id: int):
        with session_factory() as session:
            members = session.execute(
            select(MemberModel).where(MemberModel.user_id == shared_user_id)).scalars().all()

            if not members:
                raise HTTPException(status_code=404, detail="Пользователь не имеет доступ к альбому")

            else: 
                album_ids = [member.album_id for member in members]
                albums = session.execute(select(AlbumModel).where(AlbumModel.id.in_(album_ids))).scalars().all()
                return albums           
            
    @staticmethod
    def delete_shared_user_from_album(album_id: int, owner_id: int, shared_user_id: int):
        with session_factory() as session:
            album = album_db.get_album(album_id=album_id, user_id=owner_id)
            if not album:
                return f'Такого альбома не существует'
            else:
                member = session.execute(select(MemberModel).where(MemberModel.album_id == album_id, MemberModel.user_id == shared_user_id)).scalar_one_or_none()
                session.delete(member)
                session.commit()
                return member
            
    @staticmethod
    def get_shared_users(album_id: int, owner_id: int):
        album = album_db.get_album(user_id=owner_id, album_id=album_id)

        if not album: 
            raise HTTPException(status_code=404, detail="Пользователь не имеет доступ к альбому")
        else: 
            with session_factory() as session:
                members = session.execute(select(MemberModel).where(MemberModel.album_id == album_id)).scalars().all()

                if not members: 
                    return []
                
                user_ids = [member.user_id for member in members]
                users = session.execute(select(UserModel).where(UserModel.id.in_(user_ids))).scalars().all()

                return [
                    {
                        "id": user.id,
                        "login": user.login,
                        "email": user.email
                    }
                    for user in users
                ]
            
    @staticmethod
    def changing_albums(album_id: int, owner_id: int, new_title: str | None = None, new_desc: str | None = None):
        album = album_db.get_album(user_id=owner_id, album_id=album_id)
        if not album:
            return f'Альбом не найден'
        
        with session_factory() as session:
            album = session.get(AlbumModel, album_id)
            if new_title is not None:
                album.title = new_title
            if new_desc is not None: 
                album.description = new_desc
            session.commit()

            result =  {"title" : album.title,
                    "description" : album.description}
            
        return result