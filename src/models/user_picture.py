from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import base64

from src.models.pydantic_objects import PyObjectId

class UserPicture(BaseModel):
    id: Optional[PyObjectId] = Field(default= None, serialization_alias="_id")
    content_type: str | None = None
    picture: Optional[bytes] = None
    picture_url: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

    #@field_validator('picture', mode='after')
    #@classmethod
    #def convert_to_b64(cls, value: bytes) -> str:
    #    encoded_bytes = base64.b64encode(value)
    #    base64_string = encoded_bytes.decode('utf-8')
    #    return base64_string
    