from dependency_injector import containers, providers
from log2mongo import log2mongo

from src.settings_validator import Settings
from src.services import mongodb_service
from src.services.crypto_service import CryptoService
from src.services.totp_service import TOTP

#settings = Settings()

#def get_settings():
#    return settings

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.routers.auth_router",
            "src.routers.users_router",
            "src.routers.admin.users_router",
            "src.routers.admin.security_router",
            "src.routers.oauth2_router",
            "src.services.user_service",
            "src.services.login_service",
            "src.services.jwt_service",
            "src.routers.products_router",
            "src.services.totp_service",
            ])

    #get_settings = providers.Callable(get_settings)
    config = providers.Configuration(default={ "d": Settings().__dict__ })

    logging = providers.Singleton(
        log2mongo,
        config.d.LOG_DB_URL,
        config.d.LOG_DATABASE_NAME,
        level = config.d.LOG_LEVEL,
    )

    database_client = providers.Singleton(
        mongodb_service.MongoAsyncService,
        config.d.DB_URL,
        config.d.DB_NAME,
    )

    crypto_service = providers.Singleton(
        CryptoService,
        logging
    )

    totp = providers.Singleton(
        TOTP,
        config.d.TOTP_SECRET,
        config.d.TOTP_DIGEST,
        config.d.TOTP_TIME_STEP,
        config.d.TOTP_RETURN_DIGITS,
        logging
    )