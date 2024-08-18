from fastapi import HTTPException
import httpx

from common.message.message_enum import ResponseMessage
from utils.func_helper import addQueryToURL, portal_exists, run_function_from_module

from database.mongo import portal_collection

# Create portal in database
async def create_portal(portal_data: dict) -> dict:
    try:
        if await portal_exists(portal_data.slug):
            raise HTTPException(status_code=400, detail="Portal with this slug already exists.")
        
        portal = await portal_collection.insert_one(portal_data.__dict__)
        new_portal = await portal_collection.find_one({"_id": portal.inserted_id}, {'_id': 0})

        return new_portal
    except Exception as e:
        raise Exception(f"An error occurred while creating portal: {str(e)}")

# Update portal in database
async def update_portal(slug: str, portal_data: dict) -> dict:
    try:
        if not await portal_exists(slug):
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        updated_portal = await portal_collection.update_one(
            {"slug": slug},
            {"$set": portal_data}
        )

        if updated_portal.matched_count > 0:
            updated_portal = await portal_collection.find_one({'slug': slug}, {'_id': 0})
            return updated_portal
        else:
            raise HTTPException(status_code=400, detail="Portal update failed.")
        
    except Exception as e:
        raise Exception(f"An error occurred while updating portal: {str(e)}")
    
async def delete_portal(slug: str) -> str:
    try:
        if not await portal_exists(slug):
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        await portal_collection.delete_one(
            {"slug": slug}
        )
        return "Portal deleted successfully."
    except Exception as e:
        raise Exception(f"An error occurred while deleting portal: {str(e)}")

async def get_portals() -> list:
    portals = []

    try:
        async for portal in portal_collection.find({}, {'_id': 0}):
            portals.append(portal)
        
        return portals

    except Exception as e:
        raise Exception(f"An error occurred while retrieving portals: {str(e)}")
    
async def get_portal_by_slug(slug: str) -> dict:
    try:
        portal = await portal_collection.find_one({'slug': slug}, {'_id': 0})
        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        if portal['web'] == 'bacdive':
            portal['retrieve_data_url'] = ResponseMessage.NO_DATA.value
        else:
            portal['retrieve_data_url'] = await addQueryToURL(portal)

        return portal
    except Exception as e:
        raise Exception(f"An error occurred while retrieving portal by slug: {str(e)}")

async def retrieve_data(slug: str) -> dict:
    try:
        portal = await portal_collection.find_one({'slug': slug})
        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        result = await run_function_from_module(portal['web'], "retrieve", portal)
        return result
    
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    

# async def retrieve_data_params(slug: str, params: str):
#     try:
#         portal = await portal_collection.find_one({'slug': slug})
#         if not portal:
#             raise HTTPException(status_code=404, detail="Portal not found.")
        
#         url: str = portal['base_url']

#         url += '/' + params
        
#         return_add_query_to_url = await addQueryToURL(portal)

#         url += return_add_query_to_url

#         async with httpx.AsyncClient() as client:
#             response = await client.get(url)
#             response.raise_for_status()
#             data = response.json()
#         return data
    
#     except httpx.HTTPError as e:
#         raise HTTPException(status_code=e.response.status_code, detail=str(e))