from dependency_injector.wiring import Provide, inject

from src.services.user_service import get_user
from src.services.jwt_service import create_token
from src.models.token_model import Token
from src.services.crypto_service import CryptoService
from src.logging.mongo_logging import MongoLogger
from src.dependency_injection.containers import Container

crypto_service: CryptoService = Provide[Container.crypto_service]
logger: MongoLogger = Provide[Container.logging]

@inject
async def login(username, password, db, crypto = crypto_service, log = logger):
    try:
        user = await get_user(username, db)
        if user is not None:
            is_password_valid = await crypto.verify_password(password, user.password)
            if is_password_valid or user.disabled:
                token = await create_token({ "sub": user.email, "name": user.name })
                return Token(access_token=token, token_type="bearer")
        return None
    except Exception as e:
        log.logger.error(e)
        return None
