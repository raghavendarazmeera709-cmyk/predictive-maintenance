from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FactoryOps AI"
    API_VERSION: str = "v1"

    DATABASE_URL: str = "sqlite:///factoryops.db"

    DEBUG: bool = True


settings = Settings()
