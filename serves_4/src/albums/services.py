
from src.models import AlbumModel
from src.database import session_factory
from sqlalchemy import select
    
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
        
        with session_factory() as session:
            session.delete(album)
            session.commit()
            return album

    @staticmethod        
    def get_user_albums(user_id: int):
        
        with session_factory() as session:
            query = (select(AlbumModel).where(AlbumModel.id == user_id))
            result = session.execute(query)
            album = result.scalars().all()
            return album

    
