from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # DB setting
    DB_HOST: str
    DB_PORT:int
    DB_USER:str
    DB_PASS:str
    DB_NAME:str

    # jwt setting
    JWT_SECRETS:str
    JWT_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str
    model_config = SettingsConfigDict(env_file='.env')


    @property
    def DATABASE_URL(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    

config = Config()
