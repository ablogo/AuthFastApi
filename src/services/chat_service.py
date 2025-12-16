from datetime import datetime
from dependency_injector.wiring import Provide, inject
from pymongo.asynchronous.database import AsyncDatabase
from bson import ObjectId

from src.services.user_service import get_user
from src.services.crypto_service import CryptoService
from src.services.mongodb_service import MongoAsyncService
from src.models.friends_model import Contacts, Contact
from src.models.message_model import Message, MessagesSended
from src.logging.mongo_logging import MongoLogger
from src.dependency_injection.containers import Container

crypto_service: CryptoService = Provide[Container.crypto_service]
db_dependency: MongoAsyncService = Provide[Container.database_client]
logger: MongoLogger = Provide[Container.logging]
    
@inject
async def get_contacts(email: str, db = db_dependency, log = logger) -> list[Contact] | None:
    try:
        contacts = None
        if (contacts_db := await db.database["users.contacts"].find_one({'email': email})) is not None:
            model = Contacts(**contacts_db)
            contacts = model.contacts
    except Exception as e:
        log.logger.error(e)
    finally:
        return contacts
    
@inject
async def get_messages(email: str, db = db_dependency, log = logger) -> list[Message] | None:
    try:
        messages = None
        if (msg_db := await db.database["users.messages"].find({ 'receiver': email, 'sended': False }).to_list()) is not None:
            messages = [Message(**x) for x in msg_db]

    except Exception as e:
        log.logger.error(e)
    finally:
        return messages
    
@inject
async def mark_messages_as_sent(email: str, ids: MessagesSended, db = db_dependency, log = logger) -> bool:
    try:
        result = False
        
        query_filter = {"email": email, "created_at": { '$in': ids  } }
        update_op = {"$set" : {"sended" : True }}
        op_result = await db.database["users.messages"].update_many(query_filter, update_op)
        
        if op_result.modified_count > 0:
            result = True

    except Exception as e:
        log.logger.error(e)
    finally:
        return result
    
@inject
async def add_friend(name: str, email_user: str, email_friend: str, db = db_dependency, log = logger):
    try:
        result = False

        user = await get_user(email_user, db.database)
        friend = await get_user(email_friend, db.database)

        if (friends_db := await db.database["users.contacts"].find_one({'email': email_user })) is None:
            contact = Contact(name= name, email=email_friend, created_at= datetime.now())
            friends = Contacts(
                id = user.id if user != None else None,
                email = email_user,
                contacts = list([contact]),
                created_at= datetime.now())
            op_result = await db.database["users.contacts"].insert_one(friends.model_dump())

            if op_result.inserted_id is not None:
                result = True
        else:
            f = Contacts(**friends_db)
            exist = next((x for x in f.contacts if x.email == email_friend), None)
            if not exist:
                query_filter = {"email": email_user}
                update_op = {"$push": { "contacts": Contact(name= name, email= email_friend, created_at= datetime.now()).model_dump() }}
                updated_result = await db.database["users.contacts"].update_one(query_filter, update_op)
                
                if updated_result.modified_count > 0:
                    result = True
            else:
                result = True
    except Exception as e:
        log.logger.error(e)
    finally:
        return result
    
@inject
async def change_status(status: bool, email: str, db = db_dependency, log = logger) -> bool:
    try:
        result = False
        user_db = await db.database["Users"].find_one({'email': email})

        if user_db != None:
            query_filter = {"email": email}
            update_op = {"$set" : {"online" : status }}
            op_result = await db.database["Users"].update_one(query_filter, update_op)
            
            if op_result.modified_count > 0:
                result = True

    except Exception as e:
        log.logger.error(e)
    finally:
        return result
    
@inject
async def change_status_conversation(status: bool, email: str, email_friend: str, db = db_dependency, log = logger) -> bool:
    try:
        result = False
        user_db = await db.database["users.contacts"].find_one({'email': email})

        if user_db != None:
            query_filter = {
                "email": email,
                "contacts.email": email_friend
                }
            update_op = {"$set": {"contacts.$[elem].has_conversation": status }}
            nested_filter = [{ "elem.email": email_friend }]
            op_result = await db.database["users.contacts"].update_one(query_filter, update_op, array_filters= nested_filter)
            
            if op_result.modified_count > 0:
                result = True

    except Exception as e:
        log.logger.error(e)
    finally:
        return result

@inject
async def remove_friend(email_user: str, email_friend: str, db = db_dependency, log = logger) -> bool:
    try:
        result = False
        query_filter = { "email": email_user }
        update_op = {"$pull": { "contacts": { "email": email_friend } }}
        operation_result = await db.database["users.contacts"].update_one(query_filter, update_op)

        if operation_result.modified_count > 0:
            result = True
            
    except Exception as e:
        log.logger.error(e)
    finally:
        return result
    
@inject
async def save_message(msg: Message, db = db_dependency, log = logger):
    try:
        op_result = await db.database["users.messages"].insert_one(msg.model_dump())
        result = False
        if op_result.inserted_id != None:
            result = True
    except Exception as e:
        log.logger.error(e)
    finally:
        return result

@inject
async def generate_keys(email: str, db = db_dependency, log = logger) -> bool:
    try:
        result = False
        user_db = await db.database["users.messages"].find_one({'email': email})

        if user_db != None:
            query_filter = {"email": email}
            update_op = {"$set" : {"disabled" : False }}
            op_result = await db.database["users.messages"].update_one(query_filter, update_op)
            
            if op_result.modified_count > 0:
                result = True
            
    except Exception as e:
        log.logger.error(e)
    finally:
        return result
