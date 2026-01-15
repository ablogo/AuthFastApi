from datetime import datetime
from typing import Annotated, List, Optional
from bson import ObjectId
from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, Field, field_validator

from src.models.address_model import Address
from src.models.pydantic_objects import PyObjectId

def validate_email(value: str) -> str:
    cleaned= value.strip().lower()
    if cleaned is False:
        raise ValueError("Email cannot be empty")
    return cleaned

def to_iso_format(value: datetime) -> str:
    if value is not None:
        return value.isoformat()
    return value

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default= None, validation_alias="_id")
    name: str
    last_name: Optional[str] = None
    email: Annotated[str, BeforeValidator(validate_email)]
    email_verified: bool = False
    password: str
    twofactor_enabled: bool = False
    roles: Optional[List[str]] = list()
    address: Optional[List[Address]] = list()
    online: bool = False
    disabled: bool = False
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

    #model_config = ConfigDict(arbitrary_types_allowed=True)

    def dict(self, **args):
        output = super().model_dump(**args)
        for k,o in output.items():
            if isinstance(o, ObjectId):
                output[k] = str(o)
            if isinstance(o, datetime):
                output[k] = o.isoformat()
        return output
    
    @field_validator('name', mode='before')
    @classmethod
    def capitalize(cls, value: str) -> str:
        return value.capitalize()
    
    # @field_validator('id', mode='after')
    # @classmethod
    # def get_object_id_value(cls, value: ObjectId) -> str:
    #     return value.__str__()