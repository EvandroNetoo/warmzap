from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    SECRET_KEY: str
    DEBUG: bool
    HOST: str
    ALLOWED_HOSTS: Optional[list[str]] = ['*']

    ASAAS_ACCESS_TOKEN: Optional[str]

    DB_NAME: Optional[str]
    DB_HOST: Optional[str]
    DB_PORT: Optional[int]
    DB_USER: Optional[str]
    DB_PASSWORD: Optional[str]

    REDIS_URL: Optional[str] = 'redis://localhost:6379'


env_settings = Settings()
