from pydantic_settings import BaseSettings
from pydantic import validator
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    database_async_url: str  
    database_sync_url: str    
    default_timezone: str = "UTC"  
    media_dir_name: str = "media"   
    file_name_length: int = 20       
    environment: str = "local"       
    log_level: str = "info"          
    test_attempt_time_mins: int = 30  
    ssl: bool = False                 
    current_domain: str = "http://localhost:8000"  
    secret_key: str
    algorithm: str = "HS256"         
    access_token_expire_minutes: int = 30  
    POSTGRES_PASSWORD: str            

    class Config:
        env_file = ".env"  
        env_file_encoding = "utf-8"


    @validator("secret_key")
    def validate_secret_key(cls, v):
        if not v:
            logger.error("SECRET_KEY cannot be empty.")
            raise ValueError("SECRET_KEY cannot be empty.")
        logger.info("SECRET_KEY validated successfully.")
        return v


# Создаём объект настроек
settings = Settings()
