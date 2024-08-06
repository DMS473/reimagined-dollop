from fastapi import HTTPException
from database.mongo import portal_collection, raw_collection, terms_collection
from .portal_crud import retrieve_data

from operations.wikidata_retrieval import wikidata_data_processing
from operations.ncbi_retrieval import ncbi_data_processing
from operations.gbif_retrieval import gbif_data_processing
from operations.bacdive_retrieval import bacdive_data_processing

async def store_raw_data_to_db_func(slug: str, web: str, species: str, retrieve_data: any):
    try:
        print(retrieve_data)
        if not retrieve_data:
            raise HTTPException(status_code=404, detail="Data not found.")
        
        if not species:
            raise HTTPException(status_code=400, detail="Species not found.")
        
        if not web:
            raise HTTPException(status_code=400, detail="Web not found.")
        
        if not slug:
            raise HTTPException(status_code=400, detail="Slug not found.")

        data_to_store: dict = {}

        if web == 'wikidata':
            data_to_store['data'] = await wikidata_data_processing(retrieve_data)

        elif web == 'ncbi':
            data_to_store['data'] = await ncbi_data_processing(retrieve_data)

        elif web == 'gbif':
            data_to_store['data'] = await gbif_data_processing(retrieve_data)

        elif web == 'bacdive':
            data_to_store['data'] = await bacdive_data_processing(retrieve_data)

        data_to_store['slug'] = slug
        data_to_store['web'] = web
        data_to_store['species'] = species

        await raw_collection.update_one(
            {"slug": slug},
            {"$set": data_to_store},
            upsert=True
        )
        
        new_raw_data = await raw_collection.find_one({'slug': slug}, {'_id': 0})
        return new_raw_data
            
    except Exception as e:
        raise Exception(f"An error occurred while storing data to db: {str(e)}")
    
async def store_raw_data_to_db(slug: str):
    try:
        portal = await portal_collection.find_one({'slug': slug})
        if not portal:
            raise HTTPException(status_code=404, detail="Portal not found.")
        
        return_retrieve_data = await retrieve_data(slug)

        data = await store_raw_data_to_db_func(portal['slug'], portal['web'], portal['species'], return_retrieve_data)

        return data
    
    except Exception as e:
        raise Exception(f"An error occurred while storing data to raw data collection: {str(e)}")

async def store_raw_data_from_portals(species: list):
    try:
        species_for_query = [i for i in species][0][1] 

        portals = await portal_collection.find({'species': {'$in': species_for_query}}).to_list(length=1000)

        for portal in portals:
            return_retrieve_data = await retrieve_data(portal['slug'])
            await store_raw_data_to_db_func(portal['slug'], portal['web'], portal['species'], return_retrieve_data)
            
        return "All data stored successfully."
    
    except Exception as e:
        raise Exception(f"An error occurred while storing data from all portal: {str(e)}")
    
async def store_raw_data_to_terms(species: list):
    try:
        species_for_query = [i for i in species][0][1]

        for species in species_for_query:
            print(species)
            raw_datas = await raw_collection.find({'species': species}).to_list(length=1000)
            terms = await terms_collection.find_one({'species': species})
            if not terms:
                break

            newData: dict = {}

            for raw_data in raw_datas:
                newData[raw_data['web']] = raw_data['data']

            await terms_collection.update_one(
                {"species": species},
                {"$set": {"data": newData}}
            )

        return "All data stored successfully."
    
    except Exception as e:
        raise Exception(f"An error occurred while storing data to terms collection: {str(e)}")
    
async def delete_raw_data_from_db(slug: str):
    try:
        if not await raw_collection.find_one({'slug': slug}):
            raise HTTPException(status_code=404, detail="Raw data not found.")
        
        await raw_collection.delete_one(
            {"slug": slug}
        )

        return "Raw data deleted successfully."
    
    except Exception as e:
        raise Exception(f"An error occurred while deleting raw data: {str(e)}")
    
async def get_raw_data(species: list) -> list:
    try:
        species_for_query = [i for i in species][0][1]
        raw_datas = await raw_collection.find({'species': {'$in': species_for_query}}, {'_id': 0} ).to_list(length=1000)
        return raw_datas

    except Exception as e:
        raise Exception(f"An error occurred while retrieving raw data: {str(e)}")