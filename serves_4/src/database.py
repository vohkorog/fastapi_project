from sqlalchemy import create_engine
from src.config import config
from sqlalchemy.orm import sessionmaker
from models import Base


engine = create_engine(
    url = config.DATABASE_URL,
    echo = True
)

session_factory = sessionmaker(engine)

def get_session():
    with session_factory() as session:
        yield session


class db:
    @staticmethod
    def create_model():
        Base.metadata.create_all(engine)

    @staticmethod
    def delete_model():
        Base.metadata.drop_all(engine)