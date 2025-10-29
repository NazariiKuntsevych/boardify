import os

DB_DRIVER = "mysql+aiomysql"
DB_NAME = "boardify"
DB_HOST = "0.0.0.0"
DB_PORT = 3387
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PORT")
