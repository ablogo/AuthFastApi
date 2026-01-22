from typing import Annotated
from fastapi import APIRouter, Depends, Response, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from dependency_injector.wiring import Provide, inject
import io

from src.middlewares.auth_jwt import JWTCustom
from src.models.user_model import User
from src.models.address_model import Address
from src.dependency_injection.containers import Container
from src.services.mongodb_service import MongoAsyncService
from src.services.user_service import change_password, insert_address
from src.services.jwt_service import verify_token_from_requests
from src.services.totp_service import TOTP
import src.services.user_service as uSvc
from src.dependencies import get_db

oauth2_scheme = JWTCustom(tokenUrl="/auth/sign-in")
router = APIRouter(tags=["users"], dependencies=[Depends(oauth2_scheme)])
#db_dependency = Annotated[AsyncDatabase, Depends(get_db)]
db_dependency = Annotated[MongoAsyncService, Depends(Provide[Container.database_client])]
totp_dependency = Annotated[TOTP, Depends(Provide[Container.totp])]

# Route to add an users
@router.get("/user", response_model_by_alias = False)
@inject
async def get_user(db: db_dependency, email: Annotated[str, Depends(verify_token_from_requests)]) -> User | None:
    user = await uSvc.get_user(email, db.get_db())
    return user

@router.post("/user/img", response_model_by_alias = False)
@inject
async def add_user_image(file: UploadFile, db: db_dependency, email: Annotated[str, Depends(verify_token_from_requests)]):
    result = await uSvc.add_user_picture(file, file.content_type, email, db.get_db())
    if result:
        return JSONResponse("", status.HTTP_200_OK)
    else:
        return JSONResponse(None, status.HTTP_400_BAD_REQUEST)
    
@router.get("/user/img", response_model_by_alias = False)
@inject
async def get_user_image(db: db_dependency, email: Annotated[str, Depends(verify_token_from_requests)]):
    result = await uSvc.get_user_picture(email, db.get_db())
    if result and result.picture:
        return StreamingResponse(io.BytesIO(result.picture), media_type= result.content_type)
    else:
        return JSONResponse("", status.HTTP_400_BAD_REQUEST)

@router.put("/user")
@inject
async def update_user(db: db_dependency, model: User, email: Annotated[str, Depends(oauth2_scheme)]):
    result = await uSvc.update_user(db.get_db(), model)
    return result

@router.get("/user/change-password")
@inject
async def update_password(db: db_dependency, password: str, email: Annotated[str, Depends(oauth2_scheme)]):
    result = await change_password(db.get_db(), email, password)
    return result

@router.get("/user/2fa")
@inject
async def get_2f_code(email: Annotated[str, Depends(oauth2_scheme)], totp: totp_dependency):
    totp_code = await totp.now(email, is_value_ascii = True)
    if totp_code:
        return Response(content=totp_code, media_type="plain/text")
    else:
        return Response(status_code=404)

@router.get("/user/2fa-verify")
@inject
async def get_2f_code_verify(code: str, email: Annotated[str, Depends(oauth2_scheme)], totp: totp_dependency):
    if await totp.verify(code, email, is_value_ascii = True):
        return Response(status_code=200)
    else:
        return Response(status_code=401)

@router.post("/user/address")
@inject
async def create_address(db: db_dependency, address: Address, email: Annotated[str, Depends(oauth2_scheme)]):
    result = await insert_address(db.get_db(), email, address)
    return result

@router.put("/user/address")
@inject
async def update_address(db: db_dependency, address: Address, email: Annotated[str, Depends(oauth2_scheme)]):
    result = await uSvc.update_address(db.get_db(), email, address)
    return result

@router.post("/user/change-status")
@inject
async def change_status(db: db_dependency, user_status: bool, email: Annotated[str, Depends(verify_token_from_requests)]):
        result = await uSvc.change_status(user_status, email, db.get_db())
        if result:
            return Response(status_code = status.HTTP_200_OK)
        else:
            return Response(status_code = status.HTTP_412_PRECONDITION_FAILED)