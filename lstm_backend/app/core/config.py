from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Configuration settings for the application.
    """
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    PROJECT_NAME: str = "Finance App"
    SECRET: str
    KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = Settings() 