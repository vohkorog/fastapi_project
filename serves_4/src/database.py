from sqlalchemy import create_engine
from src.config import config
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    url = config.DATABASE_URL,
    echo = True
)

session_factory = sessionmaker(engine)

def get_session():
    with session_factory() as session:
        yield session

