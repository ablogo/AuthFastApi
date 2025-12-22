from dependency_injector.wiring import Provide, inject
from fastapi import UploadFile
from pymongo.asynchronous.database import AsyncDatabase
from bson import ObjectId, Binary
from dotenv import load_dotenv
import os

from src.services.crypto_service import CryptoService
from src.services.jwt_service import get_email
from src.models.user_picture import UserPicture
from src.models.user_model import User
from src.models.address_model import Address
from src.logging.mongo_logging import MongoLogger
from src.dependency_injection.containers import Container

crypto_service: CryptoService = Provide[Container.crypto_service]
log_service: MongoLogger = Provide[Container.logging]
load_dotenv()
users_collection = str(os.environ["DB_USERS_COLLECTION"])
users_pics_collection = str(os.environ["DB_USERS_PICTURES_COLLECTION"])

@inject
async def get_user(email: str, db: AsyncDatabase, log = log_service) -> User | None:
    try:
        user_db = await db[users_collection].find_one({'email': email})
        if user_db is not None:
            return User(**user_db)
        else:
            return None
    except Exception as e:
        log.logger.error(e)

@inject
async def get_user_picture(email: str, db: AsyncDatabase, log = log_service) -> UserPicture | None:
    try:
        user_db = await db[users_collection].find_one({'email': email})
        if user_db is not None:
            user_picture = await db[users_pics_collection].find_one({'_id': user_db["_id"]})
            if user_db is not None:
                return UserPicture.model_validate(user_picture)
        return None
    except Exception as e:
        log.logger.error(e)
    
@inject
async def get_users(db: AsyncDatabase, log = log_service) -> list[User] | None:
    try:
        users = list()
        if (users_db := await db[users_collection].find({}).to_list()) is not None:
            users = [User(**x) for x in users_db]
            return users
    except Exception as e:
        log.logger.error(e)
    finally:
        return users
    
@inject
async def add_user_picture(file: UploadFile, content_type: str | None, email: str, db: AsyncDatabase, log = log_service) -> bool:
    try:
        result = False
        user_bd = await db[users_collection].find_one({'email': email})
        if user_bd is not None:
            user_pic = UserPicture(
                id = user_bd["_id"],
                content_type = content_type
            )
            img = await file.read()
            user_picture = await db[users_pics_collection].find_one({'_id': user_bd["_id"]})
            
            if user_picture is not None:
                query_filter = {"_id": user_bd["_id"]}
                update_op = {"$set" : {"picture" : Binary(img), "content_type": content_type }}
                op_result = await db[users_pics_collection].update_one(query_filter, update_op)
                
                if op_result.modified_count > 0:
                    result = True
            else:
                user_pic.picture = Binary(img)
                op_result = await db[users_pics_collection].insert_one(user_pic.model_dump(by_alias=True))
                if op_result.inserted_id is not None:
                    result = True
    except Exception as e:
        log.logger.error(e)
    finally:
        return result
    
@inject
async def create_user(db: AsyncDatabase, user: User, crypto = crypto_service, log = log_service) -> User | None:
    try:
        user_bd = await db[users_collection].find_one({'email': user.email})
        if user_bd == None:
            user.password = await crypto.get_psw_hash(user.password)
            result = await db[users_collection].insert_one(user.model_dump(exclude={"id"}))
            us = await db[users_collection].find_one({ '_id': result.inserted_id })
            user = User.model_validate(us)
            return user
        else:
            return None
    except Exception as e:
        log.logger.error(e)

@inject
async def deleted_user(db: AsyncDatabase, email: str, log = log_service) -> bool:
    try:
        result = False
        operation_result = await db[users_collection].delete_one({'email': email})

        if operation_result.deleted_count > 0:
            result = True
            
    except Exception as e:
        log.logger.error(e)
    finally:
        return result

@inject
async def disabled_user(db: AsyncDatabase, email: str, log = log_service) -> bool:
    try:
        result = False
        user_db = await db[users_collection].find_one({'email': email})

        if user_db != None:
            query_filter = {"email": email}
            update_op = {"$set" : {"disabled" : False }}
            op_result = await db[users_collection].update_one(query_filter, update_op)
            
            if op_result.modified_count > 0:
                result = True
            
    except Exception as e:
        log.logger.error(e)
    finally:
        return result

@inject
async def update_user(db: AsyncDatabase, model: User, log = log_service) -> User | None:
    try:
        user_db = await db[users_collection].find_one({'email': model.email})
        user = None

        if user_db is not None:
            m = model.model_dump(exclude={"password"})
            update_fields= {}
            for key, value in m:
                if key in user_db and user_db[key] != value:
                    update_fields[key]= value
                elif key not in user_db:
                    update_fields[key]= value
                    
                if update_fields:
                    update_result = await db[users_collection].update_one({'_id': ObjectId(model.id)}, { "$set": update_fields })
                    if update_result.modified_count > 0:
                        user = User(**user_db)
    except Exception as e:
        log.logger.error(e)
    finally:
        return user

@inject
async def get_user_by_token(db: AsyncDatabase, token: str, log = log_service) -> User | None:
    try:
        email = get_email(token)
        user_bd = await db[users_collection].find_one({'email': email})
        if user_bd is not None:
            return User.model_validate(user_bd)
        else:
            return None
    except Exception as e:
        log.logger.error(e)
    
@inject
async def change_password(db: AsyncDatabase, email: str, new_password: str, crypto = crypto_service, log = log_service) -> bool:
    try:
        result = False
        user_db = await db[users_collection].find_one({'email': email})

        if user_db != None:
            query_filter = {"email": email}
            update_op = {"$set" : {"password" : await crypto.get_psw_hash(new_password) }}

            if (await db[users_collection].update_one(query_filter, update_op)).modified_count > 0:
                result = True
                
    except Exception as e:
        log.logger.error(e)
    finally:
        return result
    
@inject
async def insert_address(db: AsyncDatabase, email: str, address: Address, log = log_service) -> bool:
    try:
        result = False
        user_db = await db[users_collection].find_one({'email': email})

        if user_db is not None:
            query_filter = {"email": email}
            new_address = address.model_dump()
            id = new_address.pop("id")
            new_address.update({ "_id": id })
            update_op = {"$push" : {"address" : new_address }}
            updated_result = await db[users_collection].update_one(query_filter, update_op)

            if updated_result.modified_count > 0:
                result = True

    except Exception as e:
        log.logger.error(e)
    finally:
        return result
    
@inject
async def update_address(db: AsyncDatabase, email: str, address: Address, log = log_service) -> bool:
    try:
        result = False
        user_db = await db[users_collection].find_one(
            {"email": email },
            {"address": { "$elemMatch": { "_id": ObjectId(address.id) } } })

        if user_db is not None:
            user_db = user_db["address"]
            m = address.model_dump(exclude={"id"})
            update_fields= {}
            for key, value in m:
                if key in user_db and user_db[key] != value:
                    update_fields[key]= value
                elif key not in user_db:
                    update_fields[key]= value

            query_filter = {"email": email, "address.id": address.id }
            update_op = {"$set" : {"address" : address.model_dump() }}
            updated_result = await db[users_collection].update_one(query_filter, update_op)

            if updated_result.modified_count > 0:
                result = True

    except Exception as e:
        log.logger.error(e)
    finally:
        return result
