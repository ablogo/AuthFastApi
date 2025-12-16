from dependency_injector import containers, providers

from src.services import mongodb_service
from src.services.crypto_service import CryptoService
from src.logging.mongo_logging import MongoLogger


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.routers.auth_router",
            "src.routers.products_router",
            "src.routers.users_router",
            "src.routers.admin.users_router",
            "src.services.user_service",
            "src.services.chat_service",
            "src.services.jwt_service"
            ])

    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Singleton(
        MongoLogger,
        config.log.db_url,
        config.log.db_database,
        "",
        config.log.level
    )

    database_client = providers.Singleton(
        mongodb_service.MongoAsyncService,
        config.database.url,
        config.database.name
    )

    crypto_service = providers.Singleton(
        CryptoService,
        logging
    )