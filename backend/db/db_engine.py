from backend.settings import (
    SOURCE_DB_NAME,
    SOURCE_DB_HOST,
    SOURCE_DB_PASSWORD,
    SOURCE_DB_TYPE,
    SOURCE_DB_USER,
    SOURCE_DB_PORT,
)
from sqlalchemy import create_engine


class DbEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            self.engine = create_engine(
                f"{SOURCE_DB_TYPE}://{SOURCE_DB_USER}:{SOURCE_DB_PASSWORD}@{SOURCE_DB_HOST}:{SOURCE_DB_PORT}/{SOURCE_DB_NAME}"
            )
            print(
                f"{SOURCE_DB_TYPE}://{SOURCE_DB_USER}:{SOURCE_DB_PASSWORD}@{SOURCE_DB_HOST}/{SOURCE_DB_NAME}"
            )
            print("Connection Successful")
        except Exception as e:
            print(f"Db Connection failed {e}")
