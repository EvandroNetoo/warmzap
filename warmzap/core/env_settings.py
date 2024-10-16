from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool
    ASAAS_ACCESS_TOKEN: Optional[str]


env_settings = Settings()
