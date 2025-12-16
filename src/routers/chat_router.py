from typing import Annotated
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide, inject
from fastapi.responses import Response
import json

from src.logging.mongo_logging import MongoLogger
from src.middlewares.auth_jwt import JWTCustom
from src.models.user_model import User
from src.models.message_model import Message, MessagesSended
from src.dependency_injection.containers import Container
from src.services.mongodb_service import MongoAsyncService
import src.services.chat_service as chatSvc

oauth2_scheme = JWTCustom(tokenUrl="/auth/sign-in")
router = APIRouter(tags=["chat"], prefix="/chat")
log_dependency = Annotated[MongoLogger, Depends(Provide[Container.logging])]

@router.get("/get-contacts")
@inject
async def get_contacts(email: Annotated[str, Depends(oauth2_scheme)], log: log_dependency):
    try:
        contacts = await chatSvc.get_contacts(email)
    except Exception as e:
        log.logger.error(e)
    finally:
        if contacts:
            return Response(json.dumps(contacts, default=lambda x: getattr(x, '__dict__', str(x))), status.HTTP_200_OK, media_type="application/json")
        else:
            return Response(status_code= status.HTTP_404_NOT_FOUND)
    
@router.post("/save-message")
@inject
async def save_message(msg: Message, email: Annotated[str, Depends(oauth2_scheme)], log: log_dependency):
    try:
        result = await chatSvc.save_message(msg)
        status_code = status.HTTP_400_BAD_REQUEST
        if result:
            status_code = status.HTTP_200_OK
    except Exception as e:
        log.logger.error(e)
    finally:
        return Response(status_code= status_code)
    
@router.get("/get-messages")
@inject
async def get_messages(email: Annotated[str, Depends(oauth2_scheme)], log: log_dependency):
    try:
        messages = await chatSvc.get_messages(email)
    except Exception as e:
        log.logger.error(e)
    finally:
        if messages:
            return Response(json.dumps(messages, default=lambda x: getattr(x, '__dict__', str(x))), status.HTTP_200_OK, media_type="application/json")
        else:
            return Response(status_code= status.HTTP_404_NOT_FOUND)
        
@router.post("/change-status")
@inject
async def change_status(user_status: bool, email: Annotated[str, Depends(oauth2_scheme)], log: log_dependency):
    try:
        result = await chatSvc.change_status(user_status, email)
        status_code = status.HTTP_400_BAD_REQUEST
        if result:
            status_code = status.HTTP_200_OK
    except Exception as e:
        log.logger.error(e)
    finally:
        return Response(status_code= status_code)
    
@router.post("/change-conversation-status")
@inject
async def change_conversation_status(conversation_status: bool, email_friend, email: Annotated[str, Depends(oauth2_scheme)], log: log_dependency):
    try:
        result = await chatSvc.change_status_conversation(conversation_status, email, email_friend)
        status_code = status.HTTP_400_BAD_REQUEST
        if result:
            status_code = status.HTTP_200_OK
    except Exception as e:
        log.logger.error(e)
    finally:
        return Response(status_code= status_code)
    
@router.post("/mark-as-sended")
@inject
async def mark_messages(ids: MessagesSended, email: Annotated[str, Depends(oauth2_scheme)], log: log_dependency):
    try:
        status_code = status.HTTP_404_NOT_FOUND
        friends = await chatSvc.mark_messages_as_sent(email, ids)
        if friends:
            status_code = status.HTTP_200_OK
    except Exception as e:
        log.logger.error(e)
    finally:
        return Response(json.dumps(friends), status_code)

@router.post("/add-friend")
@inject
async def add_friend(name: str, email_friend: str, email: Annotated[str, Depends(oauth2_scheme)], log: log_dependency):
    try:
        result = await chatSvc.add_friend(name, email, email_friend)
        status_code = status.HTTP_400_BAD_REQUEST
        if result:
            status_code = status.HTTP_200_OK
    except Exception as e:
        log.logger.error(e)
    finally:
        return Response(status_code= status_code)
    
@router.delete("/remove-friend")
@inject
async def remove_friend(email_friend: str, email: Annotated[str, Depends(oauth2_scheme)], log: log_dependency):
    try:
        result = await chatSvc.remove_friend(email, email_friend)
        status_code = status.HTTP_400_BAD_REQUEST
        if result:
            status_code = status.HTTP_200_OK
    except Exception as e:
        log.logger.error(e)
    finally:
        return Response(status_code= status_code)

@router.post("/generate-keys")
@inject
async def generate_keys(email: Annotated[str, Depends(oauth2_scheme)], log: log_dependency):
    try:
        result = await chatSvc.generate_keys(email)
        return result
    except Exception as e:
        log.logger.error(e)
    finally:
        return Response(result, 200)