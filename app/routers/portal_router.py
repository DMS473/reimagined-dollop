from fastapi import APIRouter, status
from typing import List
from models.portal_model import PortalBaseModel, PortalModel, PortalDetailModel, PortalUpdateModel
from crud.portal_crud import get_portals, get_portal_by_slug, retrieve_data, create_portal, update_portal, delete_portal
from utils.response_helper import success_response, error_response
from common.message.message_enum import ResponseMessage

router = APIRouter()

# Create portal
@router.post('/', response_model=PortalModel, status_code=status.HTTP_201_CREATED)
async def create_portal_route_func(portal_data: PortalBaseModel):
    try:
        new_portal = await create_portal(portal_data)
        return success_response(new_portal, message=ResponseMessage.OK_CREATE.value, status_code=201)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Update portal
@router.put('/{slug}', status_code=status.HTTP_200_OK)
async def update_portal_route_func(slug: str, portal_data: PortalUpdateModel):
    try:
        update_data = {k: v for k, v in portal_data.__dict__.items() if v is not None}
        updated_portal = await update_portal(slug, update_data)
        return success_response(updated_portal, message=ResponseMessage.OK_UPDATE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Delete portal
@router.delete('/{slug}', status_code=status.HTTP_200_OK)
async def delete_portal_route_func(slug: str):
    try:
        deleted_portal = await delete_portal(slug)
        return success_response(deleted_portal, message=ResponseMessage.OK_DELETE.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Get all portals
@router.get("/", response_model=List[PortalModel], status_code=status.HTTP_200_OK)
async def get_portals_route_func():
    try:
        portals = await get_portals()
        return success_response(portals, message=ResponseMessage.OK_LIST.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Get detail portal by slug
@router.get("/{slug}", response_model=PortalDetailModel, status_code=status.HTTP_200_OK)
async def get_portal_by_slug_route_func(slug: str):
    try:
        portal = await get_portal_by_slug(slug)
        return success_response(portal, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Retrieve data
@router.get('/{slug}/retrieve-data', status_code=status.HTTP_200_OK)
async def retrieve_data_route_func(slug: str):
    try:
        data = await retrieve_data(slug)
        return success_response(data, message=ResponseMessage.OK.value, status_code=200)
    except Exception as e:
        return error_response(message=str(e), status_code=400)

# Retrieve data by params
# @router.get('/{slug}/{params}/retrieve-data', status_code=status.HTTP_200_OK)
# async def retrieve_data_by_id_route_func(slug: str, params: str):
#     try:
#         data = await retrieve_data_params(slug, params)
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))