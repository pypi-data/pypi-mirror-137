from typing import Optional
from pymongo import MongoClient
import sqlite3

class BaseDatabaseContext(object):
    def __init__(self, connection_string: str, db_name: str):
        self.connection_string = connection_string
        self.db_name = db_name

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

class MongoContext(BaseDatabaseContext):
    def __init__(self, connection_string: str, db_name: str, column_name: Optional[str] = None):
        super().__init__(connection_string, db_name)
        
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]
        self.col = column_name

    def __enter__(self):
        return self.db[self.col] if self.col else self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()

class SQLite3Context(BaseDatabaseContext):
    def __init__(self, connection_string: str, db_name: str):
        super().__init__(connection_string, db_name)

        self.client = sqlite3.connect(self.connection_string)
        
    def __enter__(self):
        return self.client.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        self.client.commit()
        self.client.close()