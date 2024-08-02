from fastapi import HTTPException
from database.mongo import portal_collection, raw_data_collection
from utils.raw_data_helper import raw_data_helper
from .portal_crud import retrieve_data

async def store_raw_data_to_db_func(slug: str, web: str, retrieve_data: any):
    try:
        if web == 'gbif':
            data_to_store = {
                "slug": slug,
                "data": retrieve_data
            }

        else:
            pass

        raw_data = await raw_data_collection.find_one_and_update(
            {"slug": slug},
            {"$set": data_to_store},
            upsert=True
        )

        return raw_data_helper(raw_data)
            
    except Exception as e:
        raise Exception(f"An error occurred while storing data to db: {str(e)}")
    
async def store_raw_data_to_db(slug: str):
    try:
        portal = await portal_collection.find_one({'slug': slug})
        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        return_retrieve_data = await retrieve_data(slug)

        data = await store_raw_data_to_db_func(portal['slug'], portal['web'], return_retrieve_data)

        return data
    
    except Exception as e:
        raise Exception(f"An error occurred while storing data: {str(e)}")