from datetime import datetime
from typing import List, Optional
from pydantic import AfterValidator, BaseModel, PlainValidator, Field

from src.models.pydantic_objects import PyObjectId

class Contact(BaseModel):
    name: str
    email: str
    last_message: Optional[str] = None
    last_message_time: Optional[int] = None
    has_conversation: bool = False
    created_at: datetime

class Contacts(BaseModel):
    id: Optional[PyObjectId] = Field(default= None, validation_alias="_id", serialization_alias="_id")
    email: str
    contacts: List[Contact] = list()
    created_at: datetime
    updated_at: Optional[datetime] = None