from fastapi import APIRouter, HTTPException, status
from typing import List
from models.portal_model import PortalBaseModel, PortalModel, PortalDetailModel, PortalUpdateModel
from crud.portal_crud import get_portals, get_portal_by_slug, retrieve_data, retrieve_data_params, create_portal, update_portal, delete_portal

router = APIRouter()

@router.get("/", response_model=List[PortalModel], status_code=status.HTTP_200_OK)
async def get_portals_route_func():
    try:
        portals = await get_portals()
        return portals
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{slug}", response_model=PortalDetailModel, status_code=status.HTTP_200_OK)
async def get_portal_by_slug_route_func(slug: str):
    try:
        portal = await get_portal_by_slug(slug)
        return portal
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get('/{slug}/retrieve-data', status_code=status.HTTP_200_OK)
async def retrieve_data_route_func(slug: str):
    try:
        data = await retrieve_data(slug)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get('/{slug}/{params}/retrieve-data', status_code=status.HTTP_200_OK)
async def retrieve_data_by_id_route_func(slug: str, params: str):
    try:
        data = await retrieve_data_params(slug, params)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/', response_model=PortalModel, status_code=status.HTTP_201_CREATED)
async def create_portal_route_func(portal_data: PortalBaseModel):
    try:
        new_portal = await create_portal(portal_data)
        return new_portal
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put('/{slug}', status_code=status.HTTP_200_OK)
async def update_portal_route_func(slug: str, portal_data: PortalUpdateModel):
    try:
        update_data = {k: v for k, v in portal_data.__dict__.items() if v is not None}
        updated_portal = await update_portal(slug, update_data)
        return updated_portal
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.delete('/{slug}', status_code=status.HTTP_200_OK)
async def delete_portal_route_func(slug: str):
    try:
        deleted_portal = await delete_portal(slug)
        return deleted_portal
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))