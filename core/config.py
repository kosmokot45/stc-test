from pydantic_settings import BaseSettings
# from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# DB_HOST = os.environ.get("DB_HOST")
# DB_PORT = os.environ.get("DB_PORT")
# DB_NAME = os.environ.get("DB_NAME")
# DB_USER = os.environ.get("DB_USER")
DB_URL = os.environ.get("DB_URL")


# BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    api_prefix: str = "/api"

    db_url: str = f"{DB_URL}"
    db_echo: bool = True

    class Config:
        env_file = '../..env'


settings = Settings()
