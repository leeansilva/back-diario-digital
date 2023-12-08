from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

env = Settings()