from fastapi import APIRouter, status
from crud.term_crud import get_terms, search_terms
from utils.response_helper import success_response, error_response
from common.message.message_enum import ResponseMessage
from models.term_model import TermModel, ListOfParams, searchParams
router = APIRouter()

@router.get('/', response_model=TermModel, status_code=status.HTTP_200_OK)
async def get_term_route_func(params: ListOfParams):
    try:
        data = await get_terms(params)
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)
    
@router.get('/search', status_code=status.HTTP_200_OK)
async def search_term_route_func(params: searchParams):
    try:
        data = await search_terms(params)
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)