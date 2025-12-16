from datetime import datetime, timezone
from typing import Annotated, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from time import time

from src.models.pydantic_objects import PyObjectId

def set_id(value) -> ObjectId:
    if value is None:
        return ObjectId()
    return value


class Message(BaseModel):
    #id: Annotated[Optional[PyObjectId], PlainValidator(set_id), Field(validate_default=True)] = Field(default=None, validation_alias="_id")
    sender: str
    receiver: str
    message: str
    created_at: int = int(time() * 1000)
    sended: Optional[bool] = False
    #updated_at: Optional[datetime] = None

class MessagesSended(BaseModel):
    ids: list[str]