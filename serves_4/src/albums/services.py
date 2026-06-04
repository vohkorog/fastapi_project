
from src.models import Base, UserModel, AlbumModel
from src.database import engine, session_factory
from datetime import datetime
from src.security import get_password_hash, verify_password, create_access_token, decode_token
from sqlalchemy import select
from src.auth.services import user_db
    
class album_db:

    @staticmethod
    def create_almum(title: str, 
                     token: str, 
                     description: str | None = None):
        
        verify_user =  user_db.get_current_user_from_token(token)

        if not verify_user:
            print('Неверифицированный пользователь')
        else:

            album = AlbumModel(
            title = title, 
            description = description,
            user_id = verify_user.id
        )
            with session_factory() as session:
                session.add_all([album])
                session.commit()
                session.refresh(album)
                return album

    @staticmethod        
    def get_user_album(token: str):
        verify_user =  user_db.get_current_user_from_token(token)
        if not verify_user:
            print('Неверифицированный пользователь')
        else:
            with session_factory() as session:
                query = (select(AlbumModel).where(AlbumModel.id == verify_user.id))
                result = session.execute(query)
                album = result.scalars().all()
                return album

    
