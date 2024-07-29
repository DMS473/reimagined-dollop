from fastapi import HTTPException
from database.mongo import portal_collection
from utils.portal_helper import portal_helper, portal_detail_helper
from bson import ObjectId
from urllib.parse import quote
import httpx

def pre_process_url(url: str) -> str:
    try:
        result = quote(url, safe=':/?=&')
        result = str(result)
        return result

    except Exception as e:
        raise Exception(f"An error occurred while pre-processing url: {str(e)}")
    
def addQueryToURL(portal: dict) -> str:
    if len(portal['query']) == 0:
        return ""
    
    query_str: str = ''
    
    for key in portal['query']:
        query_str += f"{key}={pre_process_url(portal['query'][key])}&"
    
    query_str = query_str[:-1]

    return f"{portal['base_url']}?{query_str}"

async def get_portals() -> list:
    # portals = [{
    #     "id": "66a6637243bf293120541f9f",
    #     "name": "WikiData-get-by-id",
    #     "base_url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
    #     "query": {
    #         "db": "taxonomy",
    #         "term": "Achromobacter"
    #     },
    # }]

    portals = []

    try:
        async for portal in portal_collection.find({}):
            portals.append(portal_helper(portal))
        return portals
    except Exception as e:
        raise Exception(f"An error occurred while retrieving portals: {str(e)}")
    
async def get_portal_by_slug(slug: str) -> dict:
    try:
        portal = await portal_collection.find_one({'slug': slug})
        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        portal['retrieve_data_url'] = addQueryToURL(portal)

        return portal_detail_helper(portal)
    except Exception as e:
        raise Exception(f"An error occurred while retrieving portal by slug: {str(e)}")
    
async def retrieve_data(slug: str):
    try:
        portal = await portal_collection.find_one({'slug': slug})
        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")

        url: str = addQueryToURL(portal)

        # return url

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        return data

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    

async def retrieve_data_params(slug: str, params: str):
    try:
        portal = await portal_collection.find_one({'slug': slug})
        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        url: str = portal['base_url']

        url += '/' + params
        
        url += addQueryToURL(portal)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        return data
    
    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    
async def create_portal(portal_data: dict) -> dict:
    try:
        if await portal_collection.find_one({"slug": portal_data.slug}):
            raise HTTPException(status_code=400, detail="Portal with this slug already exists.")
        
        portal = await portal_collection.insert_one(portal_data.__dict__)
        new_portal = await portal_collection.find_one({"_id": portal.inserted_id})

        return portal_helper(new_portal)
    except Exception as e:
        raise Exception(f"An error occurred while creating portal: {str(e)}")
    
async def update_portal(slug: str, portal_data: dict) -> dict:
    try:
        portal = await portal_collection.find_one({'slug': slug})
        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        updated_portal = await portal_collection.update_one(
            {"slug": slug},
            {"$set": portal_data}
        )

        if updated_portal.modified_count == 1:
            updated_portal = await portal_collection.find_one(
                {"slug": slug}
            )

            return portal_helper(updated_portal)
        else:
            raise HTTPException(status_code=400, detail="An error occurred while updating portal.")
        
    except Exception as e:
        raise Exception(f"An error occurred while updating portal: {str(e)}")
    
async def delete_portal(slug: str) -> dict:
    try:
        portal = await portal_collection.find_one(
            {"slug": slug}
        )

        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        await portal_collection.delete_one(
            {"slug": slug}
        )
        return "Portal deleted successfully."
    except Exception as e:
        raise Exception(f"An error occurred while deleting portal: {str(e)}")