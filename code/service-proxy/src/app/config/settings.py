from pydantic_settings import BaseSettings
import os

container_name = os.environ.get('HOSTNAME', 'default-instance')

class Settings(BaseSettings):
    app_name: str = "fastapi-proxy"
    app_host: str = container_name
    app_port: int = 8079
    eureka_url: str = "http://service-registry:8761/eureka"
    
    class Config:
        env_file = ".env"

settings = Settings()