from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DB_DRIVER: str = "mysql+aiomysql"
    DB_NAME: str = "boardify"
    DB_HOST: str = "0.0.0.0"
    DB_PORT: int = "3387"
    DB_USER: str
    DB_PASSWORD: SecretStr

    DEBUG: bool = True
    TOKEN_DURATION: int = 4 * 60 * 60  # 4 hours
    SECRET_KEY: SecretStr


settings = Settings()
