from typing import Annotated
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pymongo.asynchronous.database import AsyncDatabase

from src.services.jwt_service import verify_token
from src.services.mongodb_service import MongoService
from src.custom_json import MJSONEncoder
from src.models.product_model import Product
from src.middlewares.auth_jwt import JWTCustom
from src.dependencies import get_db

oauth2_scheme = JWTCustom(tokenUrl="/auth/sign-in")
router = APIRouter(tags=["products"])
db_dependency = Annotated[AsyncDatabase, Depends(get_db)]

# Route to add an item
@router.post("/products/")
async def add_item(product: Product, db: db_dependency):
    
    if product.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")
    
    item_bd = await db["Products"].find_one({'_id': product.name})
    if item_bd == None:
        result = await db["Products"].insert_one(product.model_dump())
        r_product = await db["Products"].find_one({ '_id': result.inserted_id })
        p = Product.model_validate(r_product)

    return p.dict()


# Route to list a specific item by ID
@router.get("/products/{item_id}")
async def list_item(item_id: str, db: db_dependency):
    product = await db["Products"].find_one({'_id': ObjectId(item_id) })
    if product == None:
        raise HTTPException(status_code=404, detail="Item not found.")
    return MJSONEncoder().encode(product)


# Route to list all items
@router.get("/products")
async def list_items(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    products = await db["Products"].find({}).to_list()
    p = [(Product(**x)).dict() for x in products]
    return p

# Route to add an item
@router.put("/products")
async def update_item(product: Product, db: db_dependency):
    
    if product.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")
    
    item_bd = await db["Products"].find_one({'_id': ObjectId(product.id)})
    if item_bd != None:
        update_fields= {}
        for key, value in product:
            if key in item_bd and item_bd[key] != value:
                update_fields[key]= value
            elif key not in item_bd:
                update_fields[key]= value

        if update_fields:
            result = await db["Products"].update_one({'_id': ObjectId(product.id)}, { "$set": update_fields })
        r_product = await db["Products"].find_one({ '_id': ObjectId(product.id) })
        p = Product.model_validate(r_product)

    return p.dict()


# Route to delete a specific item by ID
@router.delete("/products/{item_id}")
async def delete_item(item_id: str, db: db_dependency):
    qf= { "_id": ObjectId(item_id) }
    result = await db["Products"].delete_one(qf)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found.")
    
    return {"result": "Item deleted."}