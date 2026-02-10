from dependency_injector.wiring import Provide, inject
from log2mongo import log2mongo

from src.services.user_service import get_user
from src.services.jwt_service import create_token
from src.models.token_model import Token
from src.services.crypto_service import CryptoService
from src.dependency_injection.containers import Container

crypto_service: CryptoService = Provide[Container.crypto_service]
logger: log2mongo = Provide[Container.logging]

@inject
async def login(username: str, password: str, db, crypto = crypto_service, log = logger):
    try:
        user = await get_user(username, db)
        if user is not None:
            is_password_valid = await crypto.verify_password(password, user.password)
            if not user.email_verified:
                return True, None
            if is_password_valid and not user.disabled:
                token = await create_token({ "sub": user.email, "name": user.name, "roles": user.roles })
                return True, Token(access_token = token, token_type = "bearer")
    except Exception as e:
        log.logger.error(e)
    return False, None

@inject
async def external_login(username: str, issuer: str, db, crypto = crypto_service, log = logger):
    try:
        user = await get_user(username, db)
        if user:
            if user.issuer == issuer:
                token = await create_token({ "sub": user.email, "name": user.name, "roles": user.roles })
                return True, Token(access_token = token, token_type = "bearer")
    except Exception as e:
        log.logger.error(e)
    return False, None
