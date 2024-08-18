from database.mongo import terms_collection, raw_collection

from utils.func_helper import combined_index_object

async def get_terms(params: list) -> list:
    try:        
        species_for_query = params.species

        terms = await terms_collection.find({
            'species': {'$in': species_for_query},
        }, {'_id': 0} ).to_list(length=1000)

        return terms

    except Exception as e:
        raise Exception(f"An error occurred while retrieving terms data: {str(e)}")
    
async def search_terms(params: list) -> list:
    try:

        # await terms_collection.update_many(
        #     { "language": "zh" },
        #     { "$unset": { "language": "" } }
        # )

        # indexes = await terms_collection.index_information()
        # print(indexes)

        # await terms_collection.create_index(
        #     { "$**": "text" },
        #     language_override='none',
        #     default_language='en',
        # )

        # await terms_collection.create_index(
        #     {   "data.gbif.usageKey": "text" ,
        #         "data.gbif.scientificName": "text",
        #         "data.gbif.canonicalName": "text",
        #         "data.gbif.rank": "text",
        #         "data.gbif.status": "text",
        #         "data.gbif.confidence": "text",
        #         "data.gbif.matchType": "text",
        #         "data.gbif.kingdom": "text",
        #         "data.gbif.phylum": "text",
        #         "data.gbif.order": "text",
        #         "data.gbif.family": "text",
        #         "data.gbif.genus": "text",
        #         "data.gbif.species": "text",
        #         "data.gbif.kingdomKey": "text",
        #         "data.gbif.phylumKey": "text",
        #         "data.gbif.classKey": "text",
        #         "data.gbif.orderKey": "text",
        #         "data.gbif.familyKey": "text",
        #         "data.gbif.genusKey": "text",
        #         "data.gbif.speciesKey": "text",
        #         "data.gbif.synonym": "text",
        #         "data.gbif.class": "text"
        #     },
        #     name= 'testing',
        #     language_override='none',
        #     default_language='en',
        # )

        
        
        # await terms_collection.drop_index('data.gbif.usageKey_text_data.gbif_text')

        # search = params.search

        # await raw_collection.create_index(
        #     { "$**": "text" },
        #     language_override='none',
        #     default_language='en',
        # )

        projection = {
            '_id': 0,
            **combined_index_object  # Unpacking combined_index_object into the projection
        }

        print(projection)

        result = await raw_collection.find(
            { '$text': { '$search': params.search }},
            projection
        ).to_list(1000)

        # result = await terms_collection.find({
        #     '$text': { '$search': params.search }
        # }, {'_id': 0}).to_list(length=1000)

        return result

    except Exception as e:
        raise Exception(f"An error occurred while retrieving terms data: {str(e)}")