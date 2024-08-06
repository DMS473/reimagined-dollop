from fastapi import APIRouter, status
from crud.raw_data_crud import store_raw_data_to_db, store_raw_data_from_portals, store_raw_data_to_terms, delete_raw_data_from_db, get_raw_data
from utils.response_helper import success_response, error_response
from common.message.message_enum import ResponseMessage
from models.raw_data_model import ListOfSpecies
from models.raw_data_model import RawDataModel

router = APIRouter()

@router.get('/species/', response_model=RawDataModel, status_code=status.HTTP_200_OK)
async def get_raw_data_route_func(species: ListOfSpecies):
    try:
        data = await get_raw_data(species)
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

@router.post('/species/store/', response_model=RawDataModel, status_code=status.HTTP_200_OK)
async def store_raw_data_from_all_portal_route_func(species: ListOfSpecies):
    try:
        data = await store_raw_data_from_portals(species)
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

@router.post('/species/store/raw-data-to-terms', status_code=status.HTTP_200_OK)
async def store_raw_data_to_terms_route_func(species: ListOfSpecies):
    try:
        data = await store_raw_data_to_terms(species)
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
    
@router.delete('/{slug}/delete', status_code=status.HTTP_200_OK)
async def delete_raw_data_route_func(slug: str):
    try:
        data = await delete_raw_data_from_db(slug)
        return success_response(data, message=ResponseMessage.OK_DELETE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

@router.post('/{slug}/store', status_code=status.HTTP_200_OK)
async def store_raw_data(slug: str):
    try:
        data = await store_raw_data_to_db(slug)
        return success_response(data, message=ResponseMessage.OK_CREATEORUPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
