from fastapi import APIRouter, HTTPException, status
from crud.raw_data_crud import store_raw_data_to_db
from utils.response_helper import response_helper

router = APIRouter()

@router.get('/{slug}/retrieve-data/store', status_code=status.HTTP_200_OK)
async def store_raw_data(slug: str):
    try:
        data = await store_raw_data_to_db(slug)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))