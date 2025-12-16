from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject

from src.middlewares.auth_jwt import JWTCustom
from src.models.sign_up_model import SignUp
from src.models.user_model import User
from src.services.mongodb_service import MongoAsyncService
from src.dependency_injection.containers import Container
from src.logging.mongo_logging import MongoLogger
from src.services.login_service import login
from src.services.user_service import create_user

router = APIRouter(
    tags=["auth"],
    prefix="/auth"
    )
oauth2_scheme = JWTCustom(tokenUrl="/auth/sign-in")
db_dependency = Annotated[MongoAsyncService, Depends(Provide[Container.database_client])]
log_dependency = Annotated[MongoLogger, Depends(Provide[Container.logging])]

@router.post("/sign-up")
@inject
async def sign_up(model: SignUp, db: db_dependency, log: log_dependency, request: Request):
    try:
        client_host = request.client.host
        log.logger.info(f"{ model.email } sign-up from ip: { client_host }")
        content = ""
        status_code = 0
        user = await create_user(db.database, User(name= model.name, email= model.email, password= model.password, disabled=False))
        if user is not None:
            content = user.model_dump()
            status_code = status.HTTP_200_OK
        else:
            content = "Unable to create user"
            status_code = status.HTTP_400_BAD_REQUEST

    except Exception as e:
        log.logger.error(e)
    finally:
        return JSONResponse(content, status_code)

@router.post("/sign-in")
@inject
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency, log: log_dependency, request: Request):
    try:
        client_host = request.client.host
        log.logger.info(f"{ form_data.username } login from ip: { client_host }")
        content = ""
        status_code = status.HTTP_401_UNAUTHORIZED
        token = await login(form_data.username, form_data.password, db.database)
        if token is not None:
            content = token.model_dump()
            status_code = status.HTTP_200_OK

    except Exception as e:
        log.logger.error(e)
    finally:
        return JSONResponse(content, status_code)
    
@router.post("/validate-token")
@inject
async def validate_token(log: log_dependency, email: Annotated[str, Depends(oauth2_scheme)]):
    try:
        status_code = status.HTTP_401_UNAUTHORIZED
        if email is not None:
            status_code = status.HTTP_200_OK
    except Exception as e:
        log.logger.error(e)
    finally:
        return JSONResponse(email, status_code)