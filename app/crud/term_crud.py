from utils.decorator.app_log_decorator import log_function
from database.mongo import client, terms_collection, raw_collection

from utils.helper.func_helper import combined_index_object

# Retrieve terms data from database
@log_function("Retrieve terms data")
async def get_terms(params: list) -> list:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:        
                species_for_query = params.species

                terms = await terms_collection.find({
                    'species': {'$in': species_for_query},
                }, {'_id': 0}, session=session ).to_list(length=1000)

                return terms

            except Exception as e:
                raise Exception(f"An error occurred while retrieving terms data: {str(e)}")

# Search terms data from database
@log_function("Search terms data")
async def search_terms(params: list) -> list:
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:

                # indexes = await raw_collection.index_information()
                # print(indexes)

                # await raw_collection.create_index(
                #     { "$**": "text" },
                #     name='search_index',
                #     weights={
                #         "web": 10,
                #         "species": 10,
                #         "slug": 8,
                #         "data": 7
                #     },
                #     language_override='none',
                #     default_language='en',
                # )

                projection = {
                    '_id': 0,
                    'web': 1,
                    'species': 1,
                    **combined_index_object  # Unpacking combined_index_object into the projection
                }

                result = await raw_collection.find(
                    { '$text': { '$search': params.search }},
                    projection,
                    session=session
                ).to_list(1000)

                def flatten_nested_objects(data):
                    def flatten(d):
                        if isinstance(d, dict):
                            # If the dictionary has only one key and its value is another dictionary
                            if len(d) == 1:
                                key = list(d.keys())[0]
                                value = d[key]
                                if isinstance(value, dict):
                                    # Flatten the nested dictionary
                                    flattened_value = flatten(value)
                                    # Replace the current dictionary with the flattened value
                                    return flattened_value
                            # Apply flattening recursively to all dictionary values
                            return {k: flatten(v) for k, v in d.items()}
                        elif isinstance(d, list):
                            # Apply the flattening function to each item in the list
                            return [flatten(item) for item in d]
                        else:
                            return d

                    # Apply the flattening function to each item in the list
                    return [flatten(item) for item in data]
            
                return flatten_nested_objects(result)
                
            except Exception as e:
                raise Exception(f"An error occurred while retrieving terms data: {str(e)}")