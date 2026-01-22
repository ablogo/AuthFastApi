from typing import Annotated
from fastapi import APIRouter, Depends, Response
from pymongo.asynchronous.database import AsyncDatabase
from log2mongo import log2mongo
from dependency_injector.wiring import Provide, inject

from src.models.user_model import User
from src.models.address_model import Address
from src.services.user_service import change_password, insert_address
from src.dependencies import get_db
from src.middlewares.auth_roles_jwt import JWTCustom
from src.dependency_injection.containers import Container
import src.services.user_service as uSvc

oauth2_scheme = JWTCustom(tokenUrl="/auth/sign-in")
router = APIRouter(
    tags=["admin"],
    dependencies=[Depends(oauth2_scheme)],
    prefix="/admin")
db_dependency = Annotated[AsyncDatabase, Depends(get_db)]
log_dependency = Annotated[log2mongo, Depends(Provide[Container.logging])]

@router.get("/user", response_model=User)
@inject
async def get_user(email: str, db: db_dependency, log: log_dependency):
    try:
        log.logger.info(f"get user: {email}")
        user = await uSvc.get_user(email, db)
        if user:
            return Response(content=user.model_dump_json(), media_type="application/json")
        else:
            return Response(status_code=404)
    except Exception as e:
        log.logger.error(e)

@router.get("/users")
@inject
async def get_users(db: db_dependency, log: log_dependency, response: Response) -> list[User] | None:
    try:
        log.logger.info(f"get users: {db.name}")
        users = await uSvc.get_users(db)
        if users == None:
            response.status_code = 404
        return users
    except Exception as e:
        log.logger.error(e)

@router.post("/users")
@inject
async def create_user(model: User, db: db_dependency, log: log_dependency):
    try:
        user = await uSvc.create_user(db, model)
        if user is not None:
            return user
        
    except Exception as e:
        log.logger.error(e)

@router.put("/users", response_model_exclude={"created_at"})
@inject
async def update_user(model: User, db: db_dependency, log: log_dependency, response: Response):
    try:
        result = await uSvc.update_user(db, model)
        if result:
            response.status_code = 404
    except Exception as e:
        log.logger.error(e)

@router.delete("/users")
@inject
async def delete_user(email: str, db: db_dependency, log: log_dependency):
    try:
        result = await uSvc.deleted_user(db, email)
        if result:
            return True
        
    except Exception as e:
        log.logger.error(e)

@router.get("/change-password")
@inject
async def update_password(email: str, password: str, db: db_dependency, log: log_dependency, response: Response):
    try:
        result = await change_password(db, email, password)
        if not result:
            response.status_code = 400
    except Exception as e:
        log.logger.error(e)

@router.post("/users/address", response_model_by_alias = False)
@inject
async def create_address(email: str, address: Address, db: db_dependency, log: log_dependency):
    try:
        result = await insert_address(db, email, address)
        return result
    except Exception as e:
        log.logger.error(e)

@router.put("/user/address")
@inject
async def update_address(email: str, address: Address, db: db_dependency, log: log_dependency):
    try:
        result = await uSvc.update_address(db, email, address)
        return result
    except Exception as e:
        log.logger.error(e)