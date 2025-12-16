from pymongo import AsyncMongoClient
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.database import Database
import uuid

class MongoAsyncService:

    def __init__(self, mongo_url: str, db_name: str) -> None:
        try:
            self.client = AsyncMongoClient(mongo_url, server_api= ServerApi(version='1', strict=True, deprecation_errors=True))
            self.database = self.client.get_database(db_name)
            self.id = uuid.uuid4()
        except Exception as e:
            raise e
        
    def get_db(self) -> AsyncDatabase:
        return self.database
                
    async def close_db(self):
        try:
            await self.client.close()
        except Exception as e:
            raise e

class MongoService:

    def __init__(self, mongo_url: str, db_name: str) -> None:
        try:
            self.client = MongoClient(mongo_url, server_api= ServerApi(version='1', strict=True, deprecation_errors=True))
            self.database = self.client.get_database(db_name)
        except Exception as e:
            raise e
        
    def get_db(self) -> Database:
        return self.database
                
    def close_db(self):
        try:
            self.client.close()
        except Exception as e:
            raise e