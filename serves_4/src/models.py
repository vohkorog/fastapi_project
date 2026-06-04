import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Text, String, ForeignKey, Integer, text
from typing import Annotated

time_now = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class Base(DeclarativeBase):
    pass

class UserModel(Base):

    __tablename__= 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    login: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    create_at: Mapped[time_now]
    mark: Mapped[str] = mapped_column(String(10), default='Active')

    albums: Mapped[list["AlbumModel"]] = relationship(
    "AlbumModel",
    back_populates="user",
    cascade="all, delete-orphan"
)
    
class AlbumModel(Base):
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    create_at: Mapped[time_now]

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="albums")
    photos: Mapped[list["PhotoModel"]] = relationship("Photo", back_populates="album")


class PhotoModel(Base):
    __tablename__ = "photos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(100))
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.id", ondelete="CASCADE"))
    uploaded_at: Mapped[time_now]
    
    # Связи
    album: Mapped["AlbumModel"] = relationship(back_populates="photos")

