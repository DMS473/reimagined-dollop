from fastapi import HTTPException
from database.mongo import portal_collection, raw_collection, terms_collection
from .portal_crud import retrieve_data

from operations.wikidata_retrieval import wikidata_data_processing
from operations.ncbi_retrieval import ncbi_data_processing
from operations.gbif_retrieval import gbif_data_processing
from operations.bacdive_retrieval import bacdive_data_processing

async def store_raw_data_to_db_func(slug: str, web: str, species: str, retrieve_data: any):
    try:
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
    
async def store_raw_data_from_portals(params: list):
    try:
        if not params.species:
            raise HTTPException(status_code=400, detail="Species not found. Please re-check the species.")
        
        if not params.web:
            raise HTTPException(status_code=400, detail="Web not found. Please re-check the web.")
        
        species_for_query = params.species
        web_for_query = params.web

        portals = await portal_collection.find({
            'species': {'$in': species_for_query},
            'web': {'$in': web_for_query}
        }).to_list(length=1000)

        if not portals:
            raise HTTPException(status_code=404, detail="Portals not found. Please re-check the species and web.")

        for portal in portals:
            return_retrieve_data = await retrieve_data(portal['slug'])
            await store_raw_data_to_db_func(portal['slug'], portal['web'], portal['species'], return_retrieve_data)
            
        return "All data stored successfully."
    
    except Exception as e:
        raise Exception(f"An error occurred while storing data from all portal: {str(e)}")
    
async def store_raw_data_to_terms(params: list):
    try:
        if not params.species:
            raise HTTPException(status_code=400, detail="Species not found. Please re-check the species.")
        
        if not params.web:
            raise HTTPException(status_code=400, detail="Web not found. Please re-check the web.")

        species_for_query = params.species
        web_for_query = params.web

        terms: dict = {}

        for species in species_for_query:
            result = await terms_collection.find_one({'species': species}, {'data': 1, '_id': 0})

            if not result['data']:
                continue
           
            terms[species] = result['data']

        if not terms:
            raise HTTPException(status_code=404, detail="Terms not found. Please re-check the species and web.")

        for species in species_for_query:
            for web in web_for_query:
                raw_data = await raw_collection.find_one({
                    'species': species,
                    'web': web
                })

                if not raw_data:
                    continue

                terms[species][web] = raw_data['data']
        
        for species in species_for_query:
            await terms_collection.update_one(
                {"species": species},
                {"$set": {"data": terms[species]}},
                upsert=True
            )

        return "Data stored to terms successfully."
    
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
    
async def get_raw_data(params: list) -> list:
    try:
        species_for_query = params.species
        web_for_query = params.web

        raw_datas = await raw_collection.find({
            'species': {'$in': species_for_query},
            'web': {'$in': web_for_query}
        }, {'_id': 0} ).to_list(length=1000)

        return raw_datas

    except Exception as e:
        raise Exception(f"An error occurred while retrieving raw data: {str(e)}")