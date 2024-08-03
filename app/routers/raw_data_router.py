from fastapi import APIRouter, status
from crud.raw_data_crud import store_raw_data_to_db, store_raw_data_from_portals
from utils.response_helper import success_response, error_response
from common.message.message_enum import ResponseMessage
from models.raw_data_model import ListOfSpecies

router = APIRouter()    

@router.get('/species/retrieve-data/store/', status_code=status.HTTP_200_OK)
async def store_raw_data_from_all_portal_route_func(species: ListOfSpecies):
    try:
        data = await store_raw_data_from_portals(species)
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
    
@router.get('/{slug}/retrieve-data/store', status_code=status.HTTP_200_OK)
async def store_raw_data(slug: str):
    try:
        data = await store_raw_data_to_db(slug)
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
    
