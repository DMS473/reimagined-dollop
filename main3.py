from bson import ObjectId
from fastapi import FastAPI, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from models import Item, ItemInDB
from database import get_database, MongoDB

app = FastAPI()

@app.post("/items/", response_model=ItemInDB)
async def create_item(item: Item, db: MongoDB = Depends(get_database)):
    item_dict = item.dict()
    result = await db.db["items"].insert_one(item_dict)
    item_dict["id"] = str(result.inserted_id)
    return item_dict

@app.get("/items/", response_model=List[ItemInDB])
async def read_items(skip: int = 0, limit: int = 10, db: MongoDB = Depends(get_database)):
    items = await db.db["items"].find().skip(skip).limit(limit).to_list(length=limit)
    for item in items:
        item["id"] = str(item["_id"])
    return items

@app.get("/items/{item_id}", response_model=ItemInDB)
async def read_item(item_id: str, db: MongoDB = Depends(get_database)):
    item = await db.db["items"].find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item["id"] = str(item["_id"])
    return item

@app.put("/items/{item_id}", response_model=ItemInDB)
async def update_item(item_id: str, item: Item, db: MongoDB = Depends(get_database)):
    result = await db.db["items"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    item = await db.db["items"].find_one({"_id": ObjectId(item_id)})
    item["id"] = str(item["_id"])
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: str, db: MongoDB = Depends(get_database)):
    result = await db.db["items"].delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
