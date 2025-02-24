from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "System Info Microservice"
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
