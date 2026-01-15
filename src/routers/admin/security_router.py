from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Response
from dependency_injector.wiring import Provide, inject

from src.dependency_injection.containers import Container
from src.middlewares.auth_roles_jwt import JWTCustom
import src.services.totp_service as securitySvc

oauth2_scheme = JWTCustom(tokenUrl="/auth/sign-in")
router = APIRouter(
    tags=["security"],
    dependencies=[Depends(oauth2_scheme)],
    prefix="/security")
totp_dependency = Annotated[securitySvc.TOTP, Depends(Provide[Container.totp])]

@router.get("/2fa-now")
@inject
async def get_2f_code(totp: totp_dependency, email: Optional[str] = None):
    totp_code = await totp.now(email)
    if totp_code:
        return Response(content=totp_code, media_type="plain/text")
    else:
        return Response(status_code=404)

@router.get("/2fa-at")
@inject
async def get_2f_code_at(time: int, totp: totp_dependency, email: Optional[str] = None):
    otp_code = await totp.at(time, email)
    if otp_code:
        return Response(content=otp_code, media_type="plain/text")
    else:
        return Response(status_code=404)

@router.get("/2fa-verify")
@inject
async def get_2f_code_verify(code: str, totp: totp_dependency, email: Optional[str] = None):
    result = await totp.verify(code, email)
    if result:
        return Response(status_code=200)
    else:
        return Response(status_code=401)