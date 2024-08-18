from fastapi import HTTPException
from utils.decorator.app_log_decorator import log_function
from utils.helper.func_helper import check_params, run_function_from_module
from database.mongo import client, portal_collection, raw_collection, terms_collection
from .portal_crud import retrieve_data

# Store raw data from portals to raw collection
@log_function("Store raw data from portals")
async def store_raw_data_from_portals(params: list) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                await check_params(params)
                
                species_for_query = params.species
                web_for_query = params.web

                portals = await portal_collection.find({
                    'species': {'$in': species_for_query},
                    'web': {'$in': web_for_query}
                }, {'_id': 0,}, session=session).to_list(length=1000)

                if not portals:
                    raise HTTPException(status_code=404, detail="Portals not found. Please re-check the species and web.")

                for portal in portals:
                    retrieved_data = await retrieve_data(portal['slug'])

                    data_to_store: dict = {}
                    data_to_store['slug'] = portal['slug']
                    data_to_store['web'] = portal['web']
                    data_to_store['species'] = portal['species']
                    data_to_store['data'] = await run_function_from_module(portal['web'], "data_processing", retrieved_data)
                    
                    await raw_collection.update_one(
                        {"slug": portal['slug']},
                        {"$set": data_to_store},
                        upsert=True,
                        session=session
                    )
                    
                return "All data stored successfully."
            
            except Exception as e:
                raise Exception(f"An error occurred while storing data from all portal: {str(e)}")

# Store raw data from portals to raw collection
@log_function("Store raw data from portals")
async def store_raw_data_to_terms(params: list) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                await check_params(params)

                species_for_query = params.species
                web_for_query = params.web

                terms: dict = {}

                for species in species_for_query:
                    result = await terms_collection.find_one({'species': species}, {'data': 1, '_id': 0}, session=session)

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
                        }, {'data': 1, '_id': 0}, session=session)

                        if not raw_data:
                            continue

                        terms[species][web] = raw_data['data']
                
                for species in species_for_query:
                    await terms_collection.update_one(
                        {"species": species},
                        {"$set": {"data": terms[species]}},
                        upsert=True,
                        session=session
                    )

                return "Data stored to terms successfully."
            
            except Exception as e:
                raise Exception(f"An error occurred while storing data to terms collection: {str(e)}")

# Delete raw data from raw collection
@log_function("Delete raw data from raw collection")
async def delete_raw_data_from_db(params: list) -> str:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                await check_params(params)
                
                species_for_query = params.species
                web_for_query = params.web

                deleted = await raw_collection.delete_many({
                    'species': {'$in': species_for_query},
                    'web': {'$in': web_for_query}
                }, session=session)

                if deleted.deleted_count == 0:
                    raise HTTPException(status_code=404, detail="Raw data not found. Please re-check the species and web.")

                return "Raw data deleted successfully."
            
            except Exception as e:
                raise Exception(f"An error occurred while deleting raw data: {str(e)}")

# Get raw data from raw collection
@log_function("Get raw data from raw collection")
async def get_raw_data(params: list) -> list:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                await check_params(params)
                
                species_for_query = params.species
                web_for_query = params.web

                raw_datas = await raw_collection.find({
                    'species': {'$in': species_for_query},
                    'web': {'$in': web_for_query}
                }, {'_id': 0}, session=session ).to_list(length=1000)

                return raw_datas

            except Exception as e:
                raise Exception(f"An error occurred while retrieving raw data: {str(e)}")