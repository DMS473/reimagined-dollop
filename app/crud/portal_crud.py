from fastapi import HTTPException
from database.mongo import portal_collection
from urllib.parse import quote
import httpx
from common.message.message_enum import ResponseMessage

from operations.wikidata_retrieval import wikidata_retrieve
from operations.ncbi_retrieval import ncbi_retrieve
from operations.gbif_retrieval import gbif_retrieve
from operations.bacdive_retrieval import bacdive_retrieve

# pre-process url to handle special characters
async def pre_process_url(url: str) -> str:
    try:
        result = quote(url, safe=':/?=&')
        result = str(result)
        return result

    except Exception as e:
        raise Exception(f"An error occurred while pre-processing url: {str(e)}")

# add query to url if query exists
async def addQueryToURL(portal: dict) -> str:
    try:
        if len(portal['query']) == 0:
            return portal['base_url']
        
        query_str: str = ''
        
        for key in portal['query']:
            return_pre_process_url = await pre_process_url(portal['query'][key])
            query_str += f"{key}={return_pre_process_url}&"
        
        query_str = query_str[:-1]

        return f"{portal['base_url']}?{query_str}"
    
    except Exception as e:
        raise Exception(f"An error occurred while adding query to url: {str(e)}")
    
# Check if portal exists
async def portal_exists(slug: str) -> bool:
    portal = await portal_collection.find_one({"slug": slug})
    return portal

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
    
async def delete_portal(slug: str) -> dict:
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

async def retrieve_data(slug: str):
    try:
        portal = await portal_collection.find_one({'slug': slug})
        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")

        if portal['web'] == 'bacdive':
            return await bacdive_retrieve(portal['query']['name'])
        
        url: str = await addQueryToURL(portal)

        if portal['web'] == 'wikidata':
            return await wikidata_retrieve(url)

        elif portal['web'] == 'ncbi':
            return await ncbi_retrieve(url)

        elif portal['web'] == 'gbif':
            return await gbif_retrieve(url)
        
        else:
            return "No data found."
    
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