from pydantic import BaseSettings
import secrets


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "Market"
    STATIC_URL: str = "/static/"
    STATIC_PATH: str = "markup/static"
    UPLOADS_URL: str = "/uploads/"
    UPLOADS_PATH: str = "uploads/"


settings = Settings()
