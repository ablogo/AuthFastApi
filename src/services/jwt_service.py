from datetime import datetime, timedelta, timezone
from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException, Request
from dotenv import load_dotenv
import os, jwt

from src.services.crypto_service import CryptoService
from src.logging.mongo_logging import MongoLogger
from src.dependency_injection.containers import Container

crypto_service: CryptoService = Provide[Container.crypto_service]
log_service: MongoLogger = Provide[Container.logging]
load_dotenv()

@inject
async def create_token(data: dict, expire_time: timedelta = timedelta(minutes=int(str(os.environ["JWT_EXPIRE_MINUTES"]))), crypto = crypto_service, log = log_service):
    try:
        for item in data:
             data[item] = await crypto.encrypt_text(data[item])
             
        expire = datetime.now(timezone.utc) + expire_time
        data.update({ "exp": expire })
        encode_jwt = jwt.encode(data, str(os.environ["JWT_SECRET_KEY"]), algorithm= os.environ["JWT_ALGORITHM"])
        return encode_jwt
    except Exception as e:
        log.logger.error(e)
        raise e
    
@inject
async def verify_token(token: str, crypto = crypto_service, log = log_service):
        try:
            payload = await verify(token)
            email = await crypto.decrypt_text(payload.get("sub"))
            return email
        except Exception as e:
             log.logger.error(e)
             raise e
    
#async def verify_token(Authorization: str = Header(...)) -> bool:
async def verify_token_from_requests(request: Request):
        try:
            email = ""
            if(request_token := request.headers.get("Authorization")) is not None:
                request_token = request_token.replace("Bearer ", "")
                payload = await verify(request_token)
                email = await crypto_service.decrypt_text(payload.get("sub"))
            return email
            
        except Exception as e:
             #log.logger.error(e)
             raise e
        
@inject
async def verify(request_token: str, log = log_service):
        try:
            payload = jwt.decode(request_token, str(os.environ["JWT_SECRET_KEY"]), os.environ["JWT_ALGORITHM"])
            return payload
        except jwt.ExpiredSignatureError as e:
            log.logger.error(e)
            raise HTTPException(status_code=401, detail="Invalid credentials")
        except jwt.InvalidTokenError as e:
            log.logger.error(e)
            raise HTTPException(status_code=401, detail="Invalid credentials")
        except Exception as e:
             log.logger.error(e)
             raise e

@inject
async def get_email(token, crypto = crypto_service, log = log_service):
    try:
        payload = jwt.decode(token, str(os.environ["JWT_SECRET_KEY"]), os.environ["JWT_ALGORITHM"])
        email = await crypto.decrypt_text(payload.get("sub"))
        if email is None:
            return None
    except Exception as e:
         log.logger.error(e)
    else:
        return email