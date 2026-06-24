
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Text, String, ForeignKey, Integer, text, UniqueConstraint
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
    albums: Mapped[list["AlbumModel"]] = relationship("AlbumModel", back_populates="user", cascade="all, delete-orphan")
    
class AlbumModel(Base):
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    create_at: Mapped[time_now]
    
    #связи
    members: Mapped[list["MemberModel"]] = relationship("MemberModel", back_populates="share_albums", cascade="all, delete-orphan")
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="albums")
    photos: Mapped[list["PhotoModel"]] = relationship("PhotoModel", back_populates="album", cascade="all, delete-orphan")


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


class MemberModel(Base):
    __tablename__ = "members"
    __table_args__ = (
        UniqueConstraint("user_id", "album_id", name = "uq_user_album"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.id", ondelete="CASCADE"))
    share_albums: Mapped["AlbumModel"] = relationship("AlbumModel", back_populates="members")
