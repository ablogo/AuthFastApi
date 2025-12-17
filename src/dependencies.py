from dotenv import dotenv_values
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

config = dotenv_values(".env")

client = AsyncMongoClient(config["MONGO_URL"], server_api= ServerApi(version='1', strict=True, deprecation_errors=True))
database = client.get_database(config["DB_NAME"])
        
async def get_db():
    try:
        yield database
    except Exception as e:
        print(e)
        raise e
        
async def close_db():
    try:
        await client.close()
    except Exception as e:
        print(e)
        raise e