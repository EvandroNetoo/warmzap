from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    SECRET_KEY: str
    DEBUG: bool
    ASAAS_ACCESS_TOKEN: Optional[str]
    ALLOWED_HOSTS: Optional[list[str]] = ['*']

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str


env_settings = Settings()
