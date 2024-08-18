from fastapi import HTTPException
import httpx

from utils.decorator.app_log_decorator import log_function
from utils.helper.func_helper import addQueryToURL, portal_exists, run_function_from_module

from database.mongo import client, portal_collection

# Create portal in database
@log_function("Create portal")
async def create_portal(portal_data: dict) -> dict:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                if await portal_exists(portal_data.slug):
                    raise HTTPException(status_code=400, detail="Portal with this slug already exists.")
                
                portal = await portal_collection.insert_one(portal_data.__dict__, session=session)
                new_portal = await portal_collection.find_one({"_id": portal.inserted_id}, {'_id': 0}, session=session)

                return new_portal

            except Exception as e:
                raise Exception(f"An error occurred while creating portal: {str(e)}")

# Update portal in database
@log_function("Update portal")
async def update_portal(slug: str, portal_data: dict) -> dict:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                if not await portal_exists(slug):
                    raise HTTPException(status_code=404, detail="Portal not found.")
                
                updated_portal = await portal_collection.update_one(
                    {"slug": slug},
                    {"$set": portal_data},
                    session=session
                )

                if updated_portal.matched_count > 0:
                    updated_portal = await portal_collection.find_one({'slug': slug}, {'_id': 0}, session=session)
                    return updated_portal
                else:
                    raise HTTPException(status_code=400, detail="Portal update failed.")
                
            except Exception as e:
                raise Exception(f"An error occurred while updating portal: {str(e)}")

# Delete portal from database
@log_function("Delete portal")
async def delete_portal(slug: str) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                if not await portal_exists(slug):
                    raise HTTPException(status_code=404, detail="Portal not found.")
                
                await portal_collection.delete_one(
                    {"slug": slug},
                    session=session
                )
                return "Portal deleted successfully."
            except Exception as e:
                raise Exception(f"An error occurred while deleting portal: {str(e)}")

# Get all portals from database
@log_function("Get portals")
async def get_portals() -> list:
    async with await client.start_session() as session:
        async with session.start_transaction():
            portals = []

            try:
                async for portal in portal_collection.find({}, {'_id': 0}, session=session):
                    portals.append(portal)
                
                return portals

            except Exception as e:
                raise Exception(f"An error occurred while retrieving portals: {str(e)}")
    
# Get portal by slug from database
@log_function("Get portal by slug")
async def get_portal_by_slug(slug: str) -> dict:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                portal = await portal_collection.find_one({'slug': slug}, {'_id': 0}, session=session)
                if not portal:
                    raise HTTPException(status_code=404, detail="Portal not found.")
            
                portal['retrieve_data_url'] = await addQueryToURL(portal)

                return portal
            except Exception as e:
                raise Exception(f"An error occurred while retrieving portal by slug: {str(e)}")

# Retrieve data from portal
@log_function("Retrieve data")
async def retrieve_data(slug: str) -> dict:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                portal = await portal_collection.find_one({'slug': slug}, {'_id': 0}, session=session)
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