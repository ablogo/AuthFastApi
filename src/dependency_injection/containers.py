from dependency_injector import containers, providers
import os
from dotenv import load_dotenv

from src.services import mongodb_service
from src.services.crypto_service import CryptoService
from src.logging.mongo_logging import MongoLogger

load_dotenv()

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.routers.auth_router",
            "src.routers.users_router",
            "src.routers.admin.users_router",
            "src.services.user_service",
            "src.services.chat_service",
            "src.services.jwt_service",
            "src.routers.products_router"
            ])

    #config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Singleton(
        MongoLogger,
        os.environ["LOG_DB_URL"], #config.log.db_url,
        os.environ["LOG_DATABASE_NAME"], #config.log.db_database,
        "",
        os.environ["LOG_LEVEL"], #config.log.level
    )

    database_client = providers.Singleton(
        mongodb_service.MongoAsyncService,
        os.environ["DB_URL"], #config.database.url,
        os.environ["DB_NAME"], #config.database.name
    )

    crypto_service = providers.Singleton(
        CryptoService,
        logging
    )