from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_DRIVER: str = "mysql+aiomysql"
    DB_NAME: str = "boardify"
    DB_HOST: str = "db"
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: SecretStr

    DEBUG: bool = False
    TOKEN_DURATION: int = 4 * 60 * 60  # 4 hours
    SECRET_KEY: SecretStr


settings = Settings()
