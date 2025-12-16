from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from src.models.user_model import PyObjectId

class Product(BaseModel):
    id: Optional[PyObjectId] = Field(validation_alias= "_id", default= None)
    name: str
    quantity: int
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None

    def dict(self, **args):
        output = super().model_dump(**args)
        for k,o in output.items():
            if isinstance(o, ObjectId):
                output[k] = str(o)
            if isinstance(o, datetime):
                output[k] = o.isoformat()
        return output