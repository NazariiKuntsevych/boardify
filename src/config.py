import os

DB_DRIVER = "mysql+aiomysql"
DB_NAME = "boardify"
DB_HOST = "0.0.0.0"
DB_PORT = 3387
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PORT")

TOKEN_DURATION: int = 4 * 60 * 60  # 4 hours
SECRET_KEY = os.environ.get("SECRET_KEY")
