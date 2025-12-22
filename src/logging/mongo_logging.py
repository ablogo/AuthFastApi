import logging, time

from src.services.mongodb_service import MongoService

class MongoLoggerHandler(logging.Handler):

    def __init__(self, db_url: str, db_name: str, db_collection: str, collection_name_lower_case: bool = True, level: int | str = 0) -> None:
        super().__init__(level)
        self._mongo = MongoService(db_url, db_name)
        self.db = self._mongo.database
        self.db_collection = db_collection
        self.collection_lower_case = collection_name_lower_case
        
    def emit(self, record):
        try:
            log_obj = {
                "timestamp": time.gmtime(record.created),
                "name": record.name,
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "path": record.pathname
            }
            formatted_message = self.format(record)
            db_collection = self.db_collection if self.db_collection != "" else record.levelname
            db_collection = db_collection.lower() if self.collection_lower_case else db_collection
            e = self.db[db_collection].insert_one(log_obj)
            print(formatted_message)
        except Exception as e:
            print(f"Error printing custom log: { e }")

    def __del__(self) -> None:
        self._mongo.close_db()

class MongoLogger():

    def __init__(self, db_url: str, db_name: str, db_collection: str, level: int | str = 0) -> None:
        self.logger = logging.getLogger(f"{__name__}")
        self.logger.handlers.clear()
        self.logger.setLevel(level)
        handler = MongoLoggerHandler(db_url, db_name, db_collection, level= level)
        format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s")
        handler.setFormatter(format)
        self.logger.addHandler(handler)
        #logging.basicConfig(
            #level=logging.INFO,
            #format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s"
        #)