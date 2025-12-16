from datetime import datetime
from typing import Annotated, Optional
from bson import ObjectId
from pydantic import AfterValidator, BaseModel, PlainValidator, Field

from src.models.pydantic_objects import PyObjectId

def set_id(value) -> ObjectId:
    if value is None:
        return ObjectId()
    return value


class Address(BaseModel):
    id: Annotated[Optional[PyObjectId], PlainValidator(set_id), Field(validate_default=True)] = Field(default=None, validation_alias="_id")
    country: str
    state: str
    colony: str
    street: str
    number: str
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    disabled: bool = False