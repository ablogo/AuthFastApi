from typing import Annotated
from fastapi import APIRouter, Depends, Response
from pymongo.asynchronous.database import AsyncDatabase
from log2mongo import log2mongo
from dependency_injector.wiring import Provide, inject

from src.models.user_model import User
from src.models.address_model import Address
from src.services.user_service import change_password, get_address, insert_address
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
async def get_user(email: str, db: db_dependency, log: log_dependency, response: Response) -> User | None:
    try:
        user = await uSvc.get_user(email, db)
        if user:
            return user
        response.status_code = 404
    except Exception as e:
        log.logger.error(e)

@router.get("/users")
@inject
async def get_users(db: db_dependency, log: log_dependency, response: Response) -> list[User] | None:
    try:
        users = await uSvc.get_users(db)
        if users:
            return users
        response.status_code = 404
    except Exception as e:
        log.logger.error(e)

@router.post("/users")
@inject
async def create_user(model: User, db: db_dependency, log: log_dependency, response: Response):
    try:
        user = await uSvc.create_user(db, model)
        if user:
            return user
        response.status_code = 400
    except Exception as e:
        log.logger.error(e)

@router.put("/users", response_model_exclude={"created_at"})
@inject
async def update_user(model: User, db: db_dependency, log: log_dependency, response: Response):
    try:
        result = await uSvc.update_user(db, model)
        if result:
            response.status_code = 200
            return
        response.status_code = 400
    except Exception as e:
        log.logger.error(e)

@router.delete("/users")
@inject
async def delete_user(email: str, db: db_dependency, log: log_dependency, response: Response):
    try:
        result = await uSvc.deleted_user(db, email)
        if result:
            response.status_code = 200
            return
        response.status_code = 400
    except Exception as e:
        log.logger.error(e)

@router.post("/user/change-password")
@inject
async def update_password(email: str, password: str, db: db_dependency, log: log_dependency, response: Response):
    try:
        result = await change_password(db, email, password)
        if result:
            response.status_code = 200
            return
        response.status_code = 400
    except Exception as e:
        log.logger.error(e)

@router.post("/users/address")
@inject
async def create_address(email: str, address: Address, db: db_dependency, log: log_dependency):
    try:
        new_address = await insert_address(email, address, db)
        return new_address
    except Exception as e:
        log.logger.error(e)

@router.get("/user/address")
@inject
async def get_addresses(email: str, db: db_dependency, log: log_dependency, response : Response) -> list[Address] | None:
    try:
        addresses = await get_address(db, email)
        if addresses:
            return addresses
        response.status_code = 400
    except Exception as e:
        log.logger.error(e)

@router.put("/user/address")
@inject
async def update_address(email: str, address: Address, db: db_dependency, log: log_dependency, response: Response):
    try:
        result = await uSvc.update_address(db, email, address)
        if result:
            response.status_code = 200
        response.status_code = 404
    except Exception as e:
        log.logger.error(e)