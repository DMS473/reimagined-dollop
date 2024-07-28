from database.mongo import item_collection
from utils.item_helper import item_helper
from bson import ObjectId

async def create_item(item_data: dict) -> dict:
    try:
        item = await item_collection.insert_one(item_data)
        new_item = await item_collection.find_one({"_id": item.inserted_id})
        return item_helper(new_item)
    except Exception as e:
        raise Exception(f"An error occurred while creating the item: {str(e)}")

async def get_items() -> list:
    items = []
    try:
        async for item in item_collection.find({}):
            items.append(item_helper(item))
        return items
    except Exception as e:
        raise Exception(f"An error occurred while retrieving items: {str(e)}")

async def get_item(id: str) -> dict:
    try:
        item = await item_collection.find_one({"_id": ObjectId(id)})
        if item:
            return item_helper(item)
        return None
    except Exception as e:
        raise Exception(f"An error occurred while retrieving the item: {str(e)}")

async def update_item(id: str, data: dict):
    try:
        await item_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        updated_item = await item_collection.find_one({"_id": ObjectId(id)})
        return item_helper(updated_item)
    except Exception as e:
        raise Exception(f"An error occurred while updating the item: {str(e)}")

async def delete_item(id: str) -> dict:
    try:
        item = await item_collection.find_one({"_id": ObjectId(id)})
        if item:
            await item_collection.delete_one({"_id": ObjectId(id)})
            return item_helper(item)
        return None
    except Exception as e:
        raise Exception(f"An error occurred while deleting the item: {str(e)}")
