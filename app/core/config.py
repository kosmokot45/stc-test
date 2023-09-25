from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.environ.get("DB_URL")


class Settings(BaseSettings):
    api_prefix: str = "/api"

    db_url: str = f"{DB_URL}"
    db_echo: bool = True

    class Config:
        env_file = '../..env'


settings = Settings()
