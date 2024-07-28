from fastapi import APIRouter, HTTPException, status
from typing import List
from models.portal_model import PortalDB
from crud.portal_crud import get_portals

router = APIRouter()

@router.get("/", response_model=List[PortalDB], status_code=status.HTTP_200_OK)
async def get_portals_route_func():
    try:
        portals = await get_portals()
        return portals
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))