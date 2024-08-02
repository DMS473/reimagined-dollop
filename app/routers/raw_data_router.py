from fastapi import APIRouter, status
from crud.raw_data_crud import store_raw_data_to_db
from utils.response_helper import success_response, error_response
from common.message.message_enum import ResponseMessage

router = APIRouter()

@router.get('/{slug}/retrieve-data/store', status_code=status.HTTP_200_OK)
async def store_raw_data(slug: str):
    try:
        data = await store_raw_data_to_db(slug)
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
    

