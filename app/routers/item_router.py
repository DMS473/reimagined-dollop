from fastapi import APIRouter, HTTPException, status
from typing import List
from models.item_model import ItemModel, ItemDB
from crud.item_crud import create_item, get_items, get_item, update_item, delete_item

router = APIRouter()

@router.get("/", response_model=List[ItemDB], status_code=status.HTTP_200_OK)
async def get_items_endpoint():
    try:
        items = await get_items()
        return items
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", response_model=ItemDB, status_code=status.HTTP_200_OK)
async def get_item_endpoint(id: str):
    try:
        item = await get_item(id)
        if item:
            return item
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/", response_model=ItemDB, status_code=status.HTTP_201_CREATED)
async def create_item_endpoint(item: ItemModel):
    try:
        item_data = item.dict()
        new_item = await create_item(item_data)
        return new_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id}", response_model=ItemDB, status_code=status.HTTP_200_OK)
async def update_item_endpoint(id: str, item: ItemModel):
    try:
        updated_item = await update_item(id, item.dict())
        if updated_item:
            return updated_item
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}", response_model=ItemDB, status_code=status.HTTP_200_OK)
async def delete_item_endpoint(id: str):
    try:
        deleted_item = await delete_item(id)
        if deleted_item:
            return deleted_item
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
