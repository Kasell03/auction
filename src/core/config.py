import os
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

load_dotenv()


class Settings(BaseSettings):
    APP_MODE: Literal["dev", "prod", "test"] = os.environ.get("APP_MODE", "dev")

    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")

    ALLOW_ORIGINS: list[str] = ["*"]

settings = Settings()
