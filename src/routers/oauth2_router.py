from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from dependency_injector.wiring import Provide, inject
from log2mongo import log2mongo

from src.middlewares.auth_jwt import JWTCustom
from src.models.user_model import User
from src.services.jwt_service import get_token_claims_unverify_signature
from src.services.mongodb_service import MongoAsyncService
from src.dependency_injection.containers import Container
from src.services.login_service import external_login
from src.services.oauth_google_service import get_auth_url, get_auth_response
from src.services.user_service import add_user_picture, create_user, get_user

router = APIRouter(
    tags=["OAuth2"],
    prefix="/oauth"
)
oauth2_scheme = JWTCustom(tokenUrl="/auth/sign-in")
db_dependency = Annotated[MongoAsyncService, Depends(Provide[Container.database_client])]
log_dependency = Annotated[log2mongo, Depends(Provide[Container.logging])]
    
@router.get("/google-url")
@inject
async def get_google_url(db: db_dependency, log: log_dependency, request: Request):
    try:
        log.logger.info(f" sign-up from ip: { request.client.host }") # type: ignore
        content = ""
        status_code = 0
        auth_url = await get_auth_url()
        if auth_url:
            content = auth_url
            status_code = status.HTTP_307_TEMPORARY_REDIRECT
        else:
            content = "Unable to create user"
            status_code = status.HTTP_400_BAD_REQUEST

    except Exception as e:
        log.logger.error(e)
    finally:
        if status_code == status.HTTP_307_TEMPORARY_REDIRECT:
            return RedirectResponse(content)
        else:
            return Response(content, status_code)
    
@router.get("/google-response")
@inject
async def get_google_response(db: db_dependency, log: log_dependency, request: Request):
    try:
        log.logger.info(f"Google sign-up from ip: { request.client.host }") # type: ignore
        content = ""
        status_code = status.HTTP_401_UNAUTHORIZED
        google_token = await get_auth_response(request.url.__str__())
        
        if google_token:
            token_data = await get_token_claims_unverify_signature(google_token.id_token.__str__()) # type: ignore
            user = await get_user(token_data['email'], db.get_db())

            if user is None:
                user = await create_user(db.database, User(
                    name = token_data['given_name'],
                    last_name = token_data['family_name'],
                    email= token_data['email'],
                    email_verified = True,
                    password= token_data['at_hash'],
                    issuer = token_data['iss'],
                    disabled=False))
                
                if user:
                    result = await add_user_picture(token_data['email'], db.get_db(), pic_url = token_data["picture"])

            if user:
                result, token = await external_login(user.email, token_data['iss'], db.database)

                if token:
                    content = token.model_dump()
                    status_code = status.HTTP_200_OK

    except Exception as e:
        log.logger.error(e)
    finally:
        if status_code == status.HTTP_200_OK:
            return JSONResponse(content, status_code)
        else:
            return Response(status_code = status_code)
