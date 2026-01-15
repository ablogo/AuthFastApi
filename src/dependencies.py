from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()
client = AsyncMongoClient(os.environ["DB_URL"], server_api= ServerApi(version='1', strict=True, deprecation_errors=True))
database = client.get_database(os.environ["DB_NAME"])

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