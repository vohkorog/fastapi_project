from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text, String
from typing import Annotated

create_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class Base(DeclarativeBase):
    pass

class UserModel(Base):

    __tablename__= 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    login: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    create_at: Mapped[create_at]
    mark: Mapped[str] = mapped_column(String(10), default='Active')





