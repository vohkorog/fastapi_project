from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text
from typing import Annotated

create_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class Base(DeclarativeBase):
    pass

class TaskModel(Base):

    __tablename__= 'Album'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    create_at: Mapped[create_at]
    exec_at: Mapped[datetime] = mapped_column(nullable=True)





