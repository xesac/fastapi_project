from typing import Literal
from secrets import token_bytes
from base64 import b64encode
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGHORITM: str

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASS:str 

    REDIS_HOST: str
    REDIS_PORT: str



    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Со 2 версии Pydantic, class Config был заменен на атрибут model_config
    # class Config:
    #     env_file = ".env"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
