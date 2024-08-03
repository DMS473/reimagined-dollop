from fastapi import HTTPException
from database.mongo import portal_collection, raw_data_collection
from utils.raw_data_helper import raw_data_helper
from .portal_crud import retrieve_data

async def store_raw_data_to_db_func(slug: str, web: str, retrieve_data: any):
    try:
        if web == 'gbif' or web == 'wikidata':
            data_to_store = {
                "slug": slug,
                "data": retrieve_data
            }

        elif web == 'bacdive':
            data_to_store = {
                "slug": slug,
                "data": {str(k): v for k, v in retrieve_data.items()}
            }

        await raw_data_collection.update_one(
            {"slug": slug},
            {"$set": data_to_store},
            upsert=True
        )
        
        new_raw_data = await raw_data_collection.find_one({'slug': slug})
        new_raw_data['_id'] = str(new_raw_data['_id'])
        return new_raw_data
            
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

async def store_raw_data_from_portals(species: list):
    try:
        species_for_query = [i for i in species][0][1] 

        portals = await portal_collection.find({'species': {'$in': species_for_query}}).to_list(length=1000)

        for portal in portals:
            return_retrieve_data = await retrieve_data(portal['slug'])
            await store_raw_data_to_db_func(portal['slug'], portal['web'], return_retrieve_data)
            
        return "All data stored successfully."
    
    except Exception as e:
        raise Exception(f"An error occurred while storing data from all portal: {str(e)}")